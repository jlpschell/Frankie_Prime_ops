# FRANKIE 3.0 — PRODUCT REQUIREMENTS DOCUMENT
## From Reactive Chatbot to Autonomous Business Manager

**Owner:** Jay Schell
**Architect:** Claude Opus 4.6 (this document)
**Builder:** Frankie (Claude Code) + assigned build tool
**Date:** February 13, 2026
**Status:** DRAFT — Awaiting Jay + Frankie review

---

## EXECUTIVE SUMMARY

Frankie is a Telegram-based AI assistant running on a Dell Precision 5810 in WSL (Ubuntu). He uses Claude CLI as his brain (`claude -p` on Jay's Max subscription), Supabase for vector memory, Google APIs for email/calendar/drive, and Grammy for Telegram.

**The problem:** Frankie has been running with partial amnesia. Only 2 of 4 memory files auto-inject. The Telegram bot and Claude Code terminal are separate runtimes with different memory paths. Google auth is split across two Cloud projects with incomplete scopes. Memory write-back (learning from conversations) was designed but never confirmed working. Frankie sits idle waiting for input instead of proactively managing Jay's businesses.

**The solution:** Three phases that each deliver working, testable functionality before the next begins. Phase 0 fixes the foundation. Phase 1 makes Frankie proactive. Phase 2 scales him with sub-agents and business tools.

---

## CRITICAL RULES (CARRY FORWARD FROM ALL PRIOR DOCS)

These are NON-NEGOTIABLE. Every builder must follow them.

1. **Claude CLI only.** Use `claude -p` via Max subscription. NEVER use `@anthropic-ai/sdk`. Never pay twice.
2. **Google APIs direct.** `googleapis` npm package. No AI middleman for tool execution.
3. **Validator always.** SAFE/CONFIRM/NEVER action classes on every tool call. 8-call limit per message.
4. **Working directory:** `~/frankie-bot/` in WSL. All work happens here. No new projects.
5. **Runtime:** Bun (not Node). Already configured.
6. **Trust but verify.** If Frankie claims "I fixed it," check actual files and logs. He CANNOT edit his own running code.
7. **Local files are source of truth.** Supabase accelerates search — it doesn't own the data.
8. **No building without passing prior phase tests.** Phase 1 doesn't start until Phase 0 tests all pass.

---

## TWO RUNTIMES — THE CRITICAL DISTINCTION

Frankie operates in two completely different environments. Any memory/context solution MUST work in both.

### Runtime 1: Claude Code (Terminal)
- **Where:** WSL terminal, launched by Jay or build tools
- **Brain:** Claude Code's built-in AI
- **Auto-injected files:** CLAUDE.md (from working directory) + MEMORY.md (from `.claude/projects/.../memory/`)
- **NOT auto-injected:** SOUL.md, HEARTBEAT.md, contacts.md, projects.md (just files on disk)
- **Memory persistence:** Claude Code's auto-memory system (`.claude/` directory)
- **Used for:** Building, debugging, file operations, architecture work

### Runtime 2: Telegram Bot
- **Where:** `bun run src/relay.ts` — the bot Jay talks to daily
- **Brain:** Claude CLI via `claude -p` subprocess (spawned per message)
- **Prompt construction:** `src/claude-bridge.ts` builds the prompt manually
- **Memory injection:** Whatever claude-bridge.ts explicitly loads — currently: CLAUDE.md + Supabase vector search results + session history (last 20 messages)
- **NOT loaded:** SOUL.md, HEARTBEAT.md, MEMORY.md, contacts.md, projects.md (unless claude-bridge.ts is modified to load them)
- **Used for:** Daily operations, the actual Frankie Jay talks to

### What This Means
If we only fix memory for Claude Code, Telegram Frankie still has amnesia. The PRD must solve both or explicitly state which phase covers which runtime.

---

## CURRENT STATE (Verified February 13, 2026)

### What Works
| Component | Status | Runtime |
|-----------|--------|---------|
| Telegram relay (Grammy/Bun) | ✅ Working | Telegram |
| Claude CLI brain (`claude -p`) | ✅ Working | Telegram |
| Supabase vector search (`match_memories()` RPC) | ✅ Working (5 results, 0.51 avg similarity) | Both |
| OpenAI embeddings | ✅ Working | Both |
| CLAUDE.md auto-injection | ✅ Working | Both (different mechanisms) |
| MEMORY.md auto-injection | ✅ Working | Claude Code only |
| Scheduler (fires on time) | ✅ Working | Telegram |
| Validator layer | ✅ Working | Telegram |
| 44 skill files | ✅ Exist on disk | Neither (not wired for auto-discovery) |

### What's Broken or Missing
| Component | Status | Impact |
|-----------|--------|--------|
| SOUL.md injection | ❌ Not auto-loaded | Identity/goals not in every prompt |
| HEARTBEAT.md injection | ❌ Not auto-loaded | Proactive behavior not triggered |
| contacts.md / projects.md injection | ❌ Not auto-loaded in Telegram | Telegram Frankie doesn't know contacts |
| Memory auto-extraction (write-back) | ❓ Designed, never confirmed | Frankie can't learn from conversations |
| Session history in Telegram | ❓ Designed, unconfirmed | May not remember same-session context |
| `public.library` table | ❌ Missing | Error fires every message |
| Google auth — scopes | ⚠️ Split across 2 projects | Calendar/Gmail limited on workspace tools |
| Google auth — accounts | ⚠️ humanledai@gmail.com has Drive access but isn't authed | Files land in wrong account |
| Skill auto-discovery | ❌ Not wired | Skills exist but never load automatically |
| Heartbeat runner | ❌ Not built | Frankie waits for input |
| Sub-agent spawning | ❌ Not built | Everything runs through one brain |
| Goal system | ❌ Not built | No proactive task generation |
| GHL deep integration | ⚠️ API key exists, not wired | Can't manage CRM/pipelines |
| Duplicate memories | ⚠️ ~100 in Supabase, should be 17 | Wastes context, potential confusion |
| Similarity threshold | ⚠️ Set to 0.1 (too low) | Returns junk results |
| Old OAuth Drive sync | ⚠️ Logging 403 errors | Noise in logs |

### File System (Verified by Frankie)
```
~/frankie-bot/
├── src/                          ← Core bot code
│   ├── relay.ts                  ← Main bot server (Grammy/Telegram)
│   ├── claude-bridge.ts          ← Brain: spawns Claude CLI, builds prompts
│   ├── message-handler.ts        ← Command routing (/help, /remember, etc.)
│   ├── session-manager.ts        ← In-memory conversation store
│   ├── validator.ts              ← SAFE/CONFIRM/NEVER tool safety
│   ├── db/
│   │   ├── memory-manager.ts     ← searchMemories(), storeMemory(), vector search
│   │   └── supabase-client.ts    ← DB connection
│   ├── memory/
│   │   └── seed-memories.ts      ← 17 foundational memories
│   ├── google/
│   │   ├── google-api.ts         ← Direct Google API functions
│   │   └── gemini-bridge.ts      ← Stripped to utility (NotebookLM, YouTube, search)
│   └── scheduler/
│       ├── scheduler-service.ts  ← Cron engine
│       ├── morning-brief.ts      ← 5:30 AM daily summary
│       └── nightly-wrapup.ts     ← 9:30 PM daily recap
├── workspace/
│   ├── CLAUDE.md                 ← Frankie personality + behavior (AUTO-INJECTED)
│   ├── CLAUDE.md.backup          ← Pre-upgrade backup
│   ├── SOUL.md                   ← Jay's identity (ON DISK ONLY)
│   ├── HEARTBEAT.md              ← Proactive checklist (ON DISK ONLY)
│   ├── memory/                   ← Daily logs directory
│   ├── skills/                   ← Consolidated skill files
│   ├── knowledge/                ← Reference material (GHL, YouTube, NotebookLM)
│   └── credentials/              ← OAuth tokens, configs
├── .claude/projects/.../memory/
│   ├── MEMORY.md                 ← Auto-memory: quick reference (AUTO-INJECTED in CC)
│   ├── contacts.md               ← Contact list (AUTO-INJECTED in CC)
│   └── projects.md               ← Active projects (AUTO-INJECTED in CC)
├── .env                          ← All API keys and tokens
├── portal/                       ← Windows/WSL shared folder (symlink)
└── logs/                         ← Runtime logs
```

### Google Auth State
| Token Set | Cloud Project | Account | Scopes | Used By |
|-----------|--------------|---------|--------|---------|
| workspace/google_tokens.json | humanledai-485503 | jlpschell@gmail.com | Gmail R/W, Calendar R, Drive R, YouTube R | Telegram bot (Gemini bridge) |
| workspace/credentials/token.json | frankie1-486714 | jlpschell@gmail.com | Sheets full, Drive full | Workspace tools (direct API) |
| (not authed) | — | humanledai@gmail.com | Has Drive access (granted manually) | Not connected |
| (not authed) | — | jason@humanledai.net | Inside humanledai.net Workspace | Not connected |

**Known issue:** Sheets created via workspace tools land in humanledai@gmail.com despite jlpschell credentials. The humanledai-485503 project may be routing to that account.

---

## PHASE 0: FOUNDATION
**Goal:** Make memory bulletproof across both runtimes. Fix auth. Clean up debt.
**Timeline:** Complete before any other work.
**Builder:** Claude Code (Frankie) — he knows his own codebase best.

### 0.1 — Clean Supabase
**What:** Remove duplicate memories, create missing library table.
**Why:** 100 duplicates waste context. Library table error fires every message.

**Steps:**
1. Run dedup SQL in Supabase SQL Editor:
```sql
DELETE FROM memories a USING memories b
WHERE a.content = b.content AND a.created_at < b.created_at;
```
2. Create library table:
```sql
CREATE TABLE IF NOT EXISTS public.library (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content TEXT NOT NULL,
  source_type TEXT NOT NULL,
  source_path TEXT,
  category TEXT,
  embedding vector(1536),
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS library_embedding_idx ON library
USING hnsw (embedding vector_cosine_ops);
```
3. Raise similarity threshold:
```bash
sed -i 's/match_threshold: 0.1,/match_threshold: 0.35,/' ~/frankie-bot/src/db/memory-manager.ts
```

**TEST 0.1:**
- `SELECT COUNT(*) FROM memories;` → Should be ~17 (not 100)
- `SELECT COUNT(*) FROM library;` → Should return 0 (no error)
- Send Frankie "Who is Benso?" → Returns cat info (not junk)

---

### 0.2 — Consolidate Memory Files for Telegram Runtime
**What:** Modify `claude-bridge.ts` to load ALL memory files into every Telegram prompt.
**Why:** Right now Telegram Frankie only gets CLAUDE.md + Supabase results. He doesn't see SOUL.md, HEARTBEAT.md, contacts, or projects.

**What claude-bridge.ts must do (in order) when building a prompt:**
```
ALWAYS LOADED (local files — guaranteed to work):
1. Read workspace/CLAUDE.md           → Personality & behavior rules
2. Read workspace/SOUL.md             → Jay's identity, goals, communication style
3. Read workspace/MEMORY.md*          → Curated critical facts
4. Read workspace/memory/[today].md   → Today's session log (if exists)
5. Read workspace/memory/[yesterday].md → Yesterday's log (if exists)

LOADED WHEN AVAILABLE (cloud — graceful failure):
6. Search Supabase via match_memories() → Semantic vector search for message-relevant memories
   └── If Supabase fails → Log warning, continue without (local files cover baseline)

ALWAYS LOADED (session):
7. Last 20 messages from session-manager.ts → Conversation context
```

*Note: MEMORY.md currently lives in `.claude/projects/.../memory/`. For Telegram runtime, create a copy/symlink at `workspace/MEMORY.md` or have claude-bridge.ts read from both locations. The `.claude/` path is for Claude Code auto-injection; the `workspace/` path is for Telegram.*

**Implementation notes:**
- Read files with try/catch — if any file is missing, log a warning and continue
- Format injected content with clear XML-style tags so Claude can distinguish sources:
  ```
  <personality>
  [CLAUDE.md contents]
  </personality>
  <identity>
  [SOUL.md contents]
  </identity>
  <long_term_memory>
  [MEMORY.md contents]
  </long_term_memory>
  <today_log>
  [today's daily log]
  </today_log>
  <relevant_memories>
  [Supabase search results]
  </relevant_memories>
  <conversation_history>
  [last 20 messages]
  </conversation_history>
  ```
- Total injected context should stay under 8,000 tokens to leave room for Claude's response
- If total exceeds limit, trim daily logs first, then reduce Supabase results count

**TEST 0.2:**
```
1. Restart Frankie: pkill -f bun && cd ~/frankie-bot && bun run src/relay.ts
2. Send in Telegram: "What are my 12-month goals?"
   → Must answer with goals from SOUL.md (not generic response)
3. Send: "Who is Patti Baker?"
   → Must answer "GAIG account manager" (from Supabase + MEMORY.md)
4. Send: "What's my cat's name?"
   → Must answer "Benso/Benson, tuxedo cat"
5. Check logs for: lines showing each file was loaded
   → Must see: "Loaded CLAUDE.md", "Loaded SOUL.md", "Loaded MEMORY.md"
   → If any file missing, must see: "WARNING: [file] not found, skipping"
```

---

### 0.3 — Confirm Session History Works
**What:** Verify that session-manager.ts is actually passing the last 20 messages to claude-bridge.ts.
**Why:** If this isn't working, Frankie can't remember what you said 2 minutes ago in Telegram.

**Steps:**
1. Read `src/session-manager.ts` — confirm it stores messages per user
2. Read `src/claude-bridge.ts` — confirm it calls session-manager to get history
3. Add logging: `console.log("SESSION HISTORY: " + messages.length + " messages included")`

**TEST 0.3:**
```
1. Send Frankie: "My brother's name is Ryan"
2. Wait for response
3. Send Frankie: "What's my brother's name?"
4. Frankie MUST answer "Ryan" (same session, no restart)
5. Check logs for: "SESSION HISTORY: 2 messages included" (or similar)
```

---

### 0.4 — Confirm Memory Write-Back (Auto-Extraction)
**What:** When Jay tells Frankie a fact, it must actually get stored in Supabase — not just acknowledged.
**Why:** This was designed in every planning doc but never confirmed working. It's the difference between Frankie learning and Frankie pretending to learn.

**How it should work:**
1. Jay sends a message, Claude responds
2. AFTER the response, a SEPARATE extraction step runs
3. Extraction prompt: "Extract any new facts about Jay from this exchange. Return JSON: [{content, category}]. Categories: fact, preference, decision, goal, person. Empty array if none."
4. For each extracted fact: generate embedding via OpenAI → insert into Supabase `memories` table
5. Append fact to today's daily log file (`workspace/memory/YYYY-MM-DD.md`)
6. Only say "filed away" AFTER confirming Supabase write succeeded
7. If write fails, say "I tried to remember that but had a database issue"

**If extraction code doesn't exist yet**, it must be built in `claude-bridge.ts` as a post-response step.

**TEST 0.4 (THE BISCUIT TEST):**
```
1. Send Frankie: "Remember that my dog's name is Biscuit"
2. Wait for response — should confirm memory stored
3. Check logs for: "MEMORY EXTRACTED: 1 new facts stored"
4. Kill bot: pkill -f bun
5. Wait 5 seconds
6. Restart: cd ~/frankie-bot && bun run src/relay.ts
7. Send Frankie: "What's my dog's name?"
8. Frankie MUST answer "Biscuit"
9. If he does → memory write-back is working
10. If he doesn't → extraction pipeline is broken, debug before moving on
```

---

### 0.5 — Google Auth Consolidation
**What:** Map all three accounts, consolidate scopes, ensure Frankie can access everything he needs.
**Why:** Split auth means split capabilities. Calendar works on one token, Drive on another, and humanledai@gmail.com isn't connected at all.

**Target state:**

| Account | Scopes Needed | Purpose |
|---------|--------------|---------|
| jlpschell@gmail.com | Gmail R/W, Calendar R/W, Drive full, Sheets full, YouTube R | Jay's personal — email, calendar, drive |
| humanledai@gmail.com | Gmail R/W, Calendar R/W, Drive full, Sheets full | Business — Frankie manages this semi-autonomously |
| jason@humanledai.net | Gmail R/W, Calendar R/W | Workspace account — future use, basic access now |

**Steps (Jay does these — requires browser auth):**
1. Decide: consolidate to ONE Google Cloud project or keep two?
   - Recommendation: Use `frankie1-486714` for everything (it already has broader scopes)
   - Add all three accounts as authorized users
2. For each account, run OAuth flow to get a refresh token with ALL needed scopes
3. Store in `.env` with clear naming:
```
# Personal
GOOGLE_PERSONAL_CLIENT_ID=...
GOOGLE_PERSONAL_CLIENT_SECRET=...
GOOGLE_PERSONAL_REFRESH_TOKEN=...

# Business (humanledai@gmail.com)
GOOGLE_BUSINESS_CLIENT_ID=...
GOOGLE_BUSINESS_CLIENT_SECRET=...
GOOGLE_BUSINESS_REFRESH_TOKEN=...

# Workspace (jason@humanledai.net)
GOOGLE_WORKSPACE_CLIENT_ID=...
GOOGLE_WORKSPACE_CLIENT_SECRET=...
GOOGLE_WORKSPACE_REFRESH_TOKEN=...
```
4. Update `google-api.ts` to accept an `account` parameter so Frankie can specify which account to use for each operation

**TEST 0.5:**
```
1. Send Frankie: "Search my personal Drive for claims" → Returns results from jlpschell
2. Send Frankie: "Check the humanledai inbox" → Returns recent emails from humanledai@gmail.com
3. Send Frankie: "What's on my calendar tomorrow?" → Returns events from personal calendar
4. All three must return real data, no 401/403 errors
```

---

### 0.6 — Disable Old OAuth Drive Sync + Clean Logs
**What:** Stop the old Drive sync that's spamming 403 errors.
**Why:** Noise in logs makes real errors hard to find.

```bash
grep -rn "drive-sync\|drivesync\|DriveSync\|ACCESS_TOKEN_SCOPE" src/
```

Find and disable the interval/cron that triggers it. Don't delete files — just stop execution.

**TEST 0.6:**
```
1. Restart Frankie
2. Watch logs for 5 minutes
3. "ACCESS_TOKEN_SCOPE_INSUFFICIENT" error must NOT appear
```

---

### PHASE 0 — GATE CHECK
**ALL of these must pass before Phase 1 begins:**

| # | Test | Pass? |
|---|------|-------|
| 0.1a | Supabase has ~17 memories (not 100) | ☐ |
| 0.1b | Library table exists (no PGRST205 error) | ☐ |
| 0.1c | "Who is Benso?" returns cat info | ☐ |
| 0.2a | "What are my 12-month goals?" returns goals from SOUL.md | ☐ |
| 0.2b | "Who is Patti Baker?" returns GAIG info | ☐ |
| 0.2c | Logs show all memory files loaded | ☐ |
| 0.3 | Same-session recall works (brother = Ryan test) | ☐ |
| 0.4 | Biscuit test passes (learn → restart → recall) | ☐ |
| 0.5a | Personal Drive search works | ☐ |
| 0.5b | Business email check works | ☐ |
| 0.5c | Calendar check works | ☐ |
| 0.6 | No 403 Drive sync errors in 5 min | ☐ |

**Jay signs off:** __________ **Date:** __________
**Frankie confirms:** __________ (via Telegram response)

---

## PHASE 1: FRANKIE WORKS ALONE
**Goal:** Single agent, fully capable, proactively managing Jay's businesses.
**Prereq:** Phase 0 gate check 100% pass.
**Timeline:** 1-2 weeks after Phase 0.

### 1.1 — Skill Auto-Discovery
**What:** When Jay sends a message, Frankie automatically loads the relevant skill file.
**Why:** 44 skills exist on disk but never load unless manually requested.

**Implementation:**
1. `workspace/skills/index.json` already exists (from Execution Prompts) — verify it
2. Add to `claude-bridge.ts`: before sending prompt to Claude, scan message against skill triggers
3. If match found, read that skill's SKILL.md and append to prompt inside `<active_skill>` tags
4. If no match, skip (just personality + memory)
5. Max 1 skill loaded per message (pick best match if multiple trigger)

**TEST 1.1:**
```
1. Send: "Write me a cold email for an HVAC contractor in Plano"
   → Response must follow copywriting skill structure (pain-solution-CTA)
   → Logs show: "SKILL LOADED: copywriting"
2. Send: "Good morning Frankie"
   → Response is casual personality
   → Logs show: "SKILL LOADED: none"
```

---

### 1.2 — Goal System
**What:** `/goal` command stores goals in Supabase. Goals feed into morning brief.
**Why:** This is what makes auto-task generation possible (OpenClaw's killer feature).

**Supabase table:**
```sql
CREATE TABLE IF NOT EXISTS goals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  category TEXT DEFAULT 'business',
  priority TEXT DEFAULT 'medium',
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Commands:**
- `/goal Scale Human Led AI to $15K/month` → Stores goal, confirms
- `/goals` → Lists all active goals
- `/goal-done [id]` → Marks goal as achieved

**TEST 1.2:**
```
1. Send: /goal Grow Human Led AI to 10 clients by April
2. Frankie confirms: "Goal stored: Grow Human Led AI to 10 clients by April"
3. Send: /goals
4. Must list the goal just created
```

---

### 1.3 — Auto-Task Generation (Morning Brief Upgrade)
**What:** Every morning at 5:30 AM, Frankie reads active goals, asks Claude to suggest 4 tasks, creates them, includes them in morning brief.
**Why:** Frankie stops waiting for commands and starts suggesting work.

**Flow:**
1. `morning-brief.ts` queries `goals` table for active goals
2. Sends goals to Claude CLI: "Given these goals, suggest 4 specific tasks Jay or I can complete today. Return JSON array."
3. Creates tasks in `scheduled_tasks` table with `task_type: 'auto-generated'`
4. Morning brief includes: "🎯 TODAY'S TASKS: [list]"
5. Limit: Max 4 auto-tasks per day

**TEST 1.3:**
```
1. Create 2-3 goals via /goal
2. Manually trigger morning brief (or wait for 5:30 AM)
3. Morning brief must include 4 auto-generated tasks
4. Tasks must be specific and actionable (not vague)
```

---

### 1.4 — Heartbeat Runner
**What:** Separate process that runs every 30 minutes, checks email/calendar/trades, alerts Jay only when needed.
**Why:** This is what makes Frankie proactive instead of reactive.

**Architecture:**
- New file: `src/heartbeat-runner.ts` — separate from relay.ts
- Reads `workspace/HEARTBEAT.md` for checklist
- Checks: email (all accounts), calendar (next 2 hours), campaign status, trading (if market hours)
- If something needs attention → sends Telegram message
- If nothing → stays silent (logs "HEARTBEAT_OK")
- Max 3 messages per hour (anti-spam)
- Runs via cron or setInterval (30 min)

**TEST 1.4:**
```
1. Start heartbeat: bun run src/heartbeat-runner.ts
2. If there are unread emails or upcoming meetings → Jay gets a Telegram alert
3. If nothing → logs show "HEARTBEAT_OK" and no message sent
4. Send a test email to jlpschell@gmail.com from another account
5. Wait for next heartbeat cycle
6. Must receive Telegram alert about the new email
```

---

### 1.5 — Email Management (All 3 Accounts)
**What:** Frankie can check, search, read, draft, and send email across all three accounts.
**Why:** Jay wants humanledai@gmail.com managed semi-autonomously. Personal email triaged. Workspace ready for growth.

**Commands:**
- `/email` or "check my email" → Shows flagged/urgent from all accounts
- `/email personal` → Last 10 from jlpschell
- `/email business` → Last 10 from humanledai@gmail.com
- "Draft a reply to the GAIG email" → Uses CONFIRM class (Jay approves before send)
- "Send this to john@example.com from humanledai" → CONFIRM class

**Action classes:**
- Read email: SAFE (auto-execute)
- Draft email: SAFE (shows draft, doesn't send)
- Send email: CONFIRM (Jay must approve)
- Delete email: NEVER (Jay does this himself)

**TEST 1.5:**
```
1. Send: "Check my business email"
   → Returns recent emails from humanledai@gmail.com
2. Send: "Draft a reply to [specific email] saying we'll follow up next week"
   → Shows draft, asks for approval
3. Approve → Email sends from correct account
```

---

### 1.6 — Calendar Management
**What:** Frankie reads, creates, and manages calendar events.
**Why:** Scheduling is daily overhead Jay shouldn't have to handle manually.

**Commands:**
- `/calendar` or "What's on my schedule?" → Today's events
- `/calendar tomorrow` → Tomorrow's events
- "Schedule a call with [person] at 3pm Friday" → CONFIRM class
- "Block 2 hours for deep work tomorrow morning" → CONFIRM class

**TEST 1.6:**
```
1. Send: "What's on my calendar today?"
   → Returns real events (or "nothing scheduled")
2. Send: "Remind me about the Baker deadline at 3pm"
   → Creates calendar event after confirmation
```

---

### PHASE 1 — GATE CHECK

| # | Test | Pass? |
|---|------|-------|
| 1.1 | Cold email loads copywriting skill | ☐ |
| 1.2 | /goal stores and /goals retrieves | ☐ |
| 1.3 | Morning brief includes 4 auto-tasks from goals | ☐ |
| 1.4 | Heartbeat detects new email and alerts | ☐ |
| 1.5 | Business email check + draft + send works | ☐ |
| 1.6 | Calendar read + event creation works | ☐ |

**Jay signs off:** __________ **Date:** __________

---

## PHASE 2: FRANKIE DELEGATES
**Goal:** Sub-agents, GHL integration, Discord, mission control.
**Prereq:** Phase 1 gate check 100% pass + 1-2 weeks of daily use confirming stability.
**Timeline:** 2-4 weeks after Phase 1.

### 2.1 — Sub-Agent Architecture
**What:** Manager/Worker pattern. Frankie dispatches specialist agents for complex tasks.

**How it works:**
- Jay sends: "Write me a cold email for a roofer in Rockwall"
- Manager checks skill index → matches copywriting → has sub_agent defined
- Manager spawns: `claude -p "[focused copywriting prompt with SKILL.md]"`
- Copywriting Agent returns the email
- Manager wraps it in Frankie's voice and sends to Jay
- Manager logs to daily memory file

**Sub-agents to build (in order):**
1. **Copywriting Agent** — Cold emails, DMs, ad copy. Gets: SKILL.md + brand identity + target info.
2. **Trading Agent** — P&L, risk, position monitoring. Gets: TRADING_SKILL.md + trades data.
3. **Email Agent** — Inbox triage, draft responses. Gets: email skill + SOUL.md communication style.
4. **GHL Agent** — CRM, pipelines, campaigns. Gets: ghl-mastery SKILL.md + GHL API access.

**Rules:**
- Sub-agents get ONLY their relevant skill + minimal context (not full memory)
- Sub-agents CANNOT talk to Jay directly — only through Manager
- Sub-agents route through the Validator (SAFE/CONFIRM/NEVER still applies)
- Max 60-second timeout per sub-agent call (kill switch for runaway processes)

---

### 2.2 — GHL Deep Integration
**What:** Frankie manages GoHighLevel CRM, pipelines, contacts, campaigns.
**Why:** GHL is the core business tool for Human Led AI. This is where Frankie earns money.

**Functions:**
- Create/update contacts
- Move contacts through pipelines
- Send SMS/emails via GHL
- Create/update opportunities
- Tag contacts
- Search by tag/pipeline/status
- Trigger workflows

**GHL_API_KEY and GHL_LOCATION_ID already exist in .env.**

**Commands:**
- "Add John Doe to the HVAC pipeline" → CONFIRM
- "Show me all leads tagged roofing-quote" → SAFE
- "Send follow-up to all stale leads" → CONFIRM
- "Show pipeline summary" → SAFE

---

### 2.3 — Discord Integration
**What:** Frankie available on Discord with channels per domain.
**Why:** Jay wants to manage different business areas through separate channels.

**Channel structure:**
- `#general` — Chat with Frankie
- `#human-led-ai` — Business leads, GHL updates, campaign reports
- `#trading` — Trade logs, P&L, risk alerts
- `#personal` — Calendar, email summaries, reminders
- `#frankie-logs` — What Frankie did today (transparency)

**Technical:**
- Discord.js library
- Separate bot token
- Shares same Supabase memory as Telegram
- Same validator layer applies

---

### 2.4 — Second Brain Dashboard
**What:** Visual web interface showing everything Frankie knows and does.
**Why:** Jay needs to see inside Frankie's brain without asking via Telegram.

**Pages:**
- **Home:** Stats (memory count, active goals, tasks today, unread emails)
- **Memories:** Search, filter by category, add/delete
- **Tasks:** Kanban board (To Do | In Progress | Done)
- **Goals:** Active goals, progress, archive
- **Conversations:** Browse past chats with search

**Tech:** NextJS 14, Tailwind, Supabase direct connection, password-protected.
**Deploy:** Modal (free tier) or local (Jay's machine).

---

### 2.5 — GitHub Integration
**What:** Version control for Frankie's codebase.
**Why:** Jay wants to fork to laptop, track changes, prevent losing work.

**Commands:**
- "Commit today's changes" → CONFIRM
- "Show me what changed since yesterday" → SAFE
- "Create a branch for the GHL update" → CONFIRM

---

### PHASE 2 — GATE CHECK

| # | Test | Pass? |
|---|------|-------|
| 2.1 | "Write cold email" delegates to copywriting agent | ☐ |
| 2.2 | "Add contact to HVAC pipeline" works in GHL | ☐ |
| 2.3 | Discord bot responds in #general channel | ☐ |
| 2.4 | Dashboard loads, shows memories and tasks | ☐ |
| 2.5 | Git commit from Telegram works | ☐ |

---

## OPEN QUESTIONS (Decide during or before build)

1. **Google Cloud project consolidation:** One project for all accounts, or keep two? Recommendation: One (frankie1-486714).
2. **MEMORY.md location:** Symlink from `.claude/` path to `workspace/`? Or maintain two copies? Recommendation: Symlink.
3. **Dashboard hosting:** Modal (free, public URL, cold starts) or local (fast, requires WSL running)? Recommendation: Start local, move to Modal when stable.
4. **Discord first or Dashboard first?** Recommendation: Discord (Jay uses messaging daily, dashboard is a "nice to have").
5. **Sub-agent timeout:** 60 seconds enough? Some tasks (research, long emails) might need more. Recommendation: 60s default, 120s for research tasks.
6. **humanledai@gmail.com autonomy level:** How much can Frankie do without asking? Recommendation: Read=SAFE, Draft=SAFE, Send=CONFIRM, Delete=NEVER. Revisit after 2 weeks.

---

## SUCCESS CRITERIA

**Phase 0 success:** Jay messages Telegram Frankie and gets contextual, memory-aware responses that reference his goals, contacts, and recent conversations. No amnesia after restart. No auth errors.

**Phase 1 success:** Jay wakes up to a morning brief with 4 tasks. Frankie alerts him about urgent emails and upcoming meetings without being asked. Jay manages email and calendar through Telegram.

**Phase 2 success:** Jay says "write me a cold email for a roofer" and gets back Hormozi-quality copy in 15 seconds. GHL pipelines are updated without Jay touching the CRM. Discord channels show what Frankie did today.

**Ultimate success:** Jay goes to work at Alacrity, comes home, and Frankie has done 4 hours of business development, lead gen, and admin work. The $15K-$25K/month goal gets closer every week.

---

## APPENDIX A: KEY ENVIRONMENT VARIABLES

```
# Telegram
TELEGRAM_BOT_TOKEN=
ALLOWED_USER_IDS=

# Database
SUPABASE_URL=
SUPABASE_ANON_KEY=

# AI
OPENAI_API_KEY=           # Embeddings only
GEMINI_API_KEY=           # Utility (NotebookLM, YouTube, search)
GEMINI_API_KEY_2=         # Fallback
GEMINI_API_KEY_3=         # Fallback

# Google — Personal (jlpschell@gmail.com)
GOOGLE_PERSONAL_CLIENT_ID=
GOOGLE_PERSONAL_CLIENT_SECRET=
GOOGLE_PERSONAL_REFRESH_TOKEN=

# Google — Business (humanledai@gmail.com)
GOOGLE_BUSINESS_CLIENT_ID=
GOOGLE_BUSINESS_CLIENT_SECRET=
GOOGLE_BUSINESS_REFRESH_TOKEN=

# Google — Workspace (jason@humanledai.net)
GOOGLE_WORKSPACE_CLIENT_ID=
GOOGLE_WORKSPACE_CLIENT_SECRET=
GOOGLE_WORKSPACE_REFRESH_TOKEN=

# Business Tools
GHL_API_KEY=
GHL_LOCATION_ID=
ELEVENLABS_API_KEY=

# Discord (Phase 2)
DISCORD_BOT_TOKEN=
```

---

## APPENDIX B: COMMAND REFERENCE (All Phases)

### Current (Working)
- `/help` — Show commands
- `/remember [fact]` — Force-save to memory
- `/status` — Bot status
- `/clear` — Clear session

### Phase 0 (No new commands — infrastructure only)

### Phase 1 (New)
- `/goal [description]` — Store a goal
- `/goals` — List active goals
- `/goal-done [id]` — Mark goal achieved
- `/email` — Check all email (urgent/flagged)
- `/email personal|business|workspace` — Check specific account
- `/calendar` — Today's schedule
- `/calendar tomorrow` — Tomorrow's schedule

### Phase 2 (New)
- `/trades` — Today's trades
- `/pnl` — P&L summary
- `/risk` — Drawdown status
- `/pipeline` — GHL pipeline summary
- `/leads [niche]` — Search leads
- `/search [query]` — Search library/knowledge base

---

*End of PRD — Ready for review by Jay and Frankie*
*Generated by Claude Opus 4.6 | February 13, 2026*
