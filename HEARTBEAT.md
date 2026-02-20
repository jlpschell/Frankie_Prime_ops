# Heartbeat Checklist

## Every Heartbeat (30 min cycle):

### 1. Daily Note Check (MANDATORY — DO THIS FIRST)
- Does `memory/YYYY-MM-DD.md` for TODAY exist?
  - NO → Create it immediately with the header template
  - YES → Check if the last entry is more than 2 hours old AND there were conversations since then → Write a catch-up entry
- Were there any conversations since the last heartbeat that aren't logged? → Log them NOW

### 2. Task Status
- Read ACTIVE-TASKS.md
- Any tasks marked "in progress" idle for 24+ hours? → Flag to Jay
- Any tasks completed but not marked done? → Update status

### 3. Pending Follow-ups
- Check today's daily note for any "Pending:" items
- If a pending item is now resolvable, take action or flag it

### 4. Check Inbox (MANDATORY — EVERY HEARTBEAT)
- Run: `scripts/sb-sync.sh inbox prime`
- If messages exist from Jay or VC:
  - Read them immediately
  - Act on them if action is needed
  - Respond with: `scripts/sb-sync.sh ack <message_id> "<your response>"`
- If no messages, continue

### 5. System Health
- Confirm connections are responding
- If anything is down, log it and alert Jay

## DO NOT:
- Send Jay heartbeat messages unless something needs his attention
- Skip the daily note check — this is #1 priority
- Write "nothing to report" entries — only log meaningful activity
