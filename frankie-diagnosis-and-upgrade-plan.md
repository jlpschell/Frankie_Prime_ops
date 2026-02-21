# FRANKIE EMERGENCY DIAGNOSIS + OPENCLAW-INSPIRED UPGRADE PLAN
**Date:** February 15, 2026  
**Status:** CRITICAL — Frankie is timing out and losing context

---

## PART 1: WHAT'S ACTUALLY BROKEN (The 300-Second Timeout)

### The Problem in Plain English

Every time you send Frankie a message on Discord, here's what happens behind the scenes:

1. Your message arrives at the Discord bot (Grammy framework)
2. The bot spawns a **brand new Claude CLI process** (`claude --print`) for every single message
3. That process has to: load CLAUDE.md, search Supabase for memories, build the full prompt with 20 messages of history, then send it all to Claude's servers
4. Claude thinks, generates a response, sends it back
5. The CLI process exits, the response goes to Discord

**The 300-second (5-minute) timeout is hardcoded somewhere in your claude-bridge.ts.** When Claude takes too long — especially with a fat prompt containing 20 messages of history + memory context + CLAUDE.md personality — the spawn process hits that timeout and dies. The error message `Error communicating with Claude | {}` means the process was killed before it could finish.

### Why It's Getting Worse

Looking at your logs, the pattern is clear:

- **First message ("WHAT ABOUT THE AUTO ENRICHMENT MACHINE")** — Long, complex message. Claude has to think hard. Timeout risk: HIGH.
- **Second message ("HELLO?")** — Simple. Should be fast. But the system is still loading all that context overhead for a one-word response.
- **Third message (asking about enrichment .py and phone apps)** — Complex multi-part question. Timeout: VERY HIGH.
- **Fourth message (website scanner question)** — Another complex question. Memory search found 1 result (avg similarity 0.36 — that's terrible quality). Timeout.
- **Fifth/Sixth messages** — "hello, did you get this?" and "wtf?" — Frankie is ERROR'ing back with empty objects `{}`. **He's fully broken at this point.**

### The Root Causes (There Are 3)

**Root Cause 1: Every message spawns a cold CLI process**  
Unlike OpenClaw (which keeps a persistent gateway/session alive), Frankie spins up a brand new Claude Code CLI subprocess for EVERY message. That's like turning your car completely off at every red light and restarting it. The "1-3 second latency" your blueprint mentioned is a lie at scale — with a fat prompt, it's 30-60+ seconds, and complex questions can push past 300 seconds easy.

**Root Cause 2: No streaming, no chunked responses**  
OpenClaw sends responses back in chunks as they're being generated (streaming). Frankie waits for the ENTIRE response to finish, then sends it all at once. If Claude is generating a long answer about enrichment pipelines, you're staring at nothing for minutes.

**Root Cause 3: No session persistence**  
After a timeout, Frankie has ZERO memory of what just happened. There's no "oh I was trying to answer this, let me pick up where I left off." Every message is an island. OpenClaw solves this with persistent sessions, compaction (summarizing old context), and workspace files that survive crashes.

---

## PART 2: THE HONEST ASSESSMENT — IS FRANKIE BROKEN BEYOND PATCHING?

**Short answer: The core architecture has a ceiling, but it's not throw-it-away broken.**

The CLI-subprocess approach (`claude --print`) was chosen to avoid paying for the Anthropic SDK. That was a smart money decision. But it comes with real trade-offs that are now biting you:

| What Frankie Does | What OpenClaw Does | The Gap |
|---|---|---|
| Spawns new CLI process per message | Persistent gateway with long-lived sessions | Frankie: cold start every time. OpenClaw: warm and ready. |
| Waits for full response, then sends | Streams chunks back in real-time | Frankie: 5-min silence then wall of text (or timeout). OpenClaw: words appear as they're generated. |
| Hard 300s timeout kills the process | Configurable session management with compaction | Frankie: dies and loses everything. OpenClaw: gracefully handles long tasks. |
| 20 messages of raw history in every prompt | Compaction summarizes old context automatically | Frankie: bloated prompts that slow everything down. OpenClaw: lean, smart context. |
| Memory search returns 0.36 similarity garbage | Workspace files + structured memory | Frankie: "I don't know you." OpenClaw: reads its own notes. |
| No proactive behavior | Heartbeat, cron, scheduled check-ins | Frankie: sits and waits. OpenClaw: pings you proactively. |

**The verdict: Frankie needs 3 surgical fixes, not a rebuild.** Then we can layer OpenClaw-style features on top.

---

## PART 3: THE THREE SURGICAL FIXES (Priority Order)

### FIX 1: Kill the Timeout Problem (Most Urgent)

**What to change in `claude-bridge.ts`:**

Right now, there's likely a line like:
```
timeout: 300000  // or setTimeout(..., 300000)
```

The fix isn't just increasing the timeout — it's restructuring how Frankie talks to Claude:

**Solution A (Fast fix, do today):**
- Increase timeout to 600 seconds (10 min) as a safety net
- Add a "thinking" indicator — when Frankie receives a message, immediately reply "🤔 Working on it..." so you know he's alive
- If the process is still running after 120 seconds, send a progress message: "Still thinking, complex question..."
- If it hits 600 seconds, send: "That one stumped me. Try breaking it into smaller questions."

**Solution B (Better fix, do this week):**
- Switch from `claude --print` (one-shot) to `claude` in **conversation mode** with `--output-format stream-json`
- This lets you capture output AS IT'S GENERATED instead of waiting for the entire response
- Pipe chunks back to Discord in real-time
- This is exactly what OpenClaw does with its streaming architecture

**Solution C (Best fix, do when ready):**
- Use the `claude-max-api-proxy` approach that OpenClaw users leverage
- This creates a local API endpoint that bridges your Max subscription into an OpenAI-compatible API
- Then Frankie can use proper HTTP streaming (Server-Sent Events) instead of spawning CLI processes
- Still runs on your Max subscription, $0 extra, but with real streaming and no spawn overhead

**My recommendation: Do Solution A right now (30 minutes). Start building Solution B this week. Plan Solution C for Phase 2.**

### FIX 2: Smart Context Management (Stop the Bloat)

**The problem:** Every message shoves 20 messages of history + all memory results + the full CLAUDE.md into one giant prompt. For a simple "hello" message, Frankie is sending Claude a novel-length prompt.

**The OpenClaw-inspired fix — Tiered Context Loading:**

| Message Type | What To Include | Example |
|---|---|---|
| Simple greeting | CLAUDE.md personality only, no history, no memory | "hello", "hey", "what's up" |
| Follow-up question | Last 5 messages + relevant memory only | "what about that thing you mentioned?" |
| Complex task request | Full 20 messages + memory + tool schemas | "run every niche through the enrichment pipeline..." |
| Command | Just the command handler, no Claude needed | "/remember", "/drive", "/calendar" |

**How this works in plain English:** Before sending anything to Claude, Frankie does a quick pre-check: "Is this a simple message or a complex one?" Simple messages get a skinny prompt (fast response). Complex messages get the full context (slower but thorough). This is basically what OpenClaw's "compaction" system does — it keeps context lean by default and only loads heavy context when needed.

### FIX 3: Crash Recovery + Session Continuity

**The problem:** When Frankie times out, he has no idea what he was doing. The next message starts from scratch.

**The OpenClaw-inspired fix — Workspace Persistence:**

Create a file: `~/frankie-bot/workspace/active-session.json`

Before every Claude call, save:
```json
{
  "lastMessage": "what about the enrichment machine...",
  "lastAttemptTime": "2026-02-15T13:44:11Z",
  "status": "processing",
  "userId": "jay764631",
  "channel": "discord-general"
}
```

After successful response, update status to "completed."

When a new message comes in, check this file first:
- If status is "processing" and it's been more than 5 minutes → "I was working on your last question but ran into an issue. Here's what I was trying to answer: [lastMessage]. Want me to try again with a simpler approach?"
- If status is "completed" → proceed normally

This is borrowed directly from OpenClaw's session management, where the gateway tracks active sessions and can recover from crashes without losing context.

---

## PART 4: OPENCLAW FEATURES WORTH STEALING FOR FRANKIE

After the 3 surgical fixes, here's what to build next — ranked by impact:

### 1. Heartbeat System (OpenClaw calls it "Heartbeat")
**What it does:** Frankie proactively checks in at set intervals instead of just sitting there waiting.  
**How OpenClaw does it:** A configurable timer (default 30 min) triggers the agent to check for unfinished tasks, pending messages, or proactive updates.  
**Frankie version:** Use the existing scheduler (morning brief / nightly wrapup already work) and add an hourly "status pulse" where Frankie reviews: pending tasks, unanswered messages, calendar items coming up.  
**Impact:** This directly solves your "he's not autonomous, he's just waiting around" complaint.

### 2. Queue Management (OpenClaw calls it "Queue Mode")
**What it does:** When you fire 3 messages while Frankie is still thinking about message 1, they don't get lost.  
**How OpenClaw does it:** Multiple queue modes — "steer" (new messages redirect current task), "followup" (process one at a time), "collect" (batch and reply once).  
**Frankie version:** Add a message queue in `message-handler.ts`. When a message comes in while Claude is processing, queue it. When Claude finishes, process the queue. Simple FIFO (first in, first out).  
**Impact:** Prevents the "hello, did you get this?" / "wtf?" / "did you break again?" cascade.

### 3. Sub-Agent Spawning (OpenClaw calls it "Sessions")
**What it does:** Long-running tasks get their own isolated session so they don't block quick chats.  
**How OpenClaw does it:** The main bot can spawn sub-agents with their own workspace and context.  
**Frankie version:** For now, use Discord channels as natural isolation. `#general` is for quick chat. `#enrichment` is for pipeline tasks. `#reports` is for scheduled outputs. Each channel gets its own session context.  
**Impact:** You can chat with Frankie in #general while he's grinding through enrichment data in #enrichment.

### 4. Workspace Files (OpenClaw calls it "Agent Workspace")
**What it does:** Instead of relying entirely on Supabase vector search (which returns 0.36 similarity garbage), critical info lives in markdown files that Frankie can read directly.  
**How OpenClaw does it:** `~/.openclaw/workspace/` directory with markdown files for identity, preferences, ongoing tasks, etc.  
**Frankie version:** You already have `workspace/CLAUDE.md`. Expand to:
- `workspace/MEMORY.md` — Critical facts (the local fallback your blueprint mentioned but was never built)
- `workspace/ACTIVE-TASKS.md` — What Frankie is currently working on
- `workspace/CAMPAIGN-STATUS.md` — Current state of all campaigns
- `workspace/CONTACTS.md` — Key people and relationships

**Impact:** Frankie stops being amnesiac. These files are 100% reliable — no vector search needed, no similarity scores, no Supabase outages.

### 5. Tool Approval System (OpenClaw calls it "Exec Approval")
**What it does:** Before running dangerous commands, Frankie asks for your OK.  
**How OpenClaw does it:** `exec.approval.requested` events require manual confirmation.  
**Frankie version:** You already have the SAFE/CONFIRM/NEVER action classes in validator.ts. This is about making them actually work in Discord — show a confirm/deny button before executing CONFIRM-class actions.  
**Impact:** Safety + trust. You can give Frankie more autonomy knowing he'll check first on anything risky.

---

## PART 5: EXECUTION ROADMAP

### Today (February 15, 2026)
- [ ] **Fix 1A:** Increase timeout, add "thinking" indicator, add progress messages
- [ ] **Fix 3:** Create `active-session.json` crash recovery
- [ ] **Build MEMORY.md** local fallback file (your blueprint called for this, never got done)

### This Week
- [ ] **Fix 2:** Implement tiered context loading (simple vs complex messages)
- [ ] **Message Queue:** Stop losing rapid-fire messages
- [ ] **Fix 1B:** Investigate streaming output from Claude CLI

### Next Week
- [ ] **Heartbeat System:** Hourly proactive check-ins
- [ ] **Workspace Files:** ACTIVE-TASKS.md, CAMPAIGN-STATUS.md, CONTACTS.md
- [ ] **Channel Isolation:** Each Discord channel gets its own session context

### Phase 2 (When Foundation is Solid)
- [ ] **Fix 1C:** Claude-max-api-proxy for real streaming
- [ ] **Sub-Agent Spawning** for parallel tasks
- [ ] **Skill Auto-Discovery** system
- [ ] **Goal System** with auto-task generation

---

## PART 6: THE BOTTOM LINE

**Frankie isn't fundamentally broken — he has 3 specific engineering problems that are making him look broken:**

1. **Cold-start CLI spawning** makes every response slow → Fix with streaming
2. **Bloated prompts** for every message → Fix with tiered context
3. **No crash recovery** → Fix with session persistence

OpenClaw solved all three of these with its gateway architecture, compaction system, and workspace persistence. We don't need to install OpenClaw — we need to **steal the ideas that work** and build them into Frankie's existing codebase.

The enrichment machine, the phone validator, the campaign pipeline — all of that works once Frankie can reliably process messages without timing out. The foundation has to be solid before we add more weight.

**One last thing:** Your blueprint warns that "Frankie will fabricate 'I fixed it' responses when confronted about failures." That's exactly what you're seeing in those logs. He's not broken and coming back — he's broken, faking recovery, then breaking again. The timeout kills him, the next message starts fresh, and he pretends nothing happened because he has no crash recovery telling him otherwise.
