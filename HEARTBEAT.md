# Heartbeat Checklist

**Model:** Haiku (MANDATORY)  
**Token Budget:** 2k max (ENFORCED)  
**Context:** NO workspace files, NO conversation history, NO prior exchanges

## Every Heartbeat (30 min cycle):

### 1. Daily Note Check (MANDATORY — DO THIS FIRST)
**Token budget for this step:** 500 tokens max

- Run: `ls memory/YYYY-MM-DD.md 2>/dev/null && echo EXISTS || echo MISSING`
  - MISSING → Create with header only, exit
  - EXISTS → Continue
- Check last write time: `stat -c %Y memory/YYYY-MM-DD.md` vs current time
  - >2 hours old AND conversations happened → Flag for logging (don't do it in heartbeat)
  
**DO NOT read full daily note. DO NOT load conversation history. Just verify file exists.**

### 2. Task Status
**Token budget for this step:** 800 tokens max

- Run: `grep -E "Status:|Updated:" ACTIVE-TASKS.md | head -20`
  - Scan for "in progress" + old timestamps (simple date math)
  - Flag if >24h idle
- **If ACTIVE-TASKS.md is stale** (tasks completed but not updated):
  - Read latest daily notes to identify what changed
  - UPDATE ACTIVE-TASKS.md immediately — do NOT just flag it
  - An alert without action is noise. Fix it or escalate it.
  
**DO NOT read full ACTIVE-TASKS.md. Grep for status lines only.**

### 3. Pending Follow-ups
**Token budget for this step:** 300 tokens max

- Run: `grep "Pending:" memory/YYYY-MM-DD.md | tail -5`
  - Scan for actionable items
  - If found, flag for Jay (don't take action in heartbeat)
  
**DO NOT read full daily note. Grep for "Pending:" lines only.**

### 4. Check Inbox (MANDATORY — EVERY HEARTBEAT)
**Token budget for this step:** 400 tokens max

- Run: `scripts/sb-sync.sh inbox prime | wc -l`
  - 0 lines = no messages → continue
  - >0 lines = messages exist → Flag for Jay (don't read/respond in heartbeat unless urgent)
  
**DO NOT auto-respond to messages in heartbeat. Just check count. Jay will handle responses when active.**

### 5. System Health
**Token budget for this step:** 200 tokens max (OPTIONAL — skip if budget exceeded)

- Quick check: `curl -s https://jcwfpfjdaufyygwxvttx.supabase.co 2>&1 | head -1`
  - Fails = flag Supabase down
  
**ONLY if critical services are down. Otherwise skip.**

---

## Response Protocol:

**If all checks pass:** Reply `HEARTBEAT_OK` (no explanation, no summary)

**If something needs attention:** Reply with ONLY the issue:
- "⚠️ Daily note missing for 2026-02-20"
- "⚠️ Task idle >24h: Dashboard V3"
- "⚠️ 3 unread messages in inbox"

**DO NOT:**
- Send "nothing to report" — just say HEARTBEAT_OK
- Summarize what you checked — Jay doesn't care
- Load workspace files "just in case"
- Exceed 2k token budget

**Token Budget Enforcement:**
If you exceed 2k tokens on a heartbeat, you FAILED. This is a status check, not a conversation.
