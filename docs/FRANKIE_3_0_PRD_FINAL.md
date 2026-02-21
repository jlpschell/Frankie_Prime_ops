# FRANKIE 3.0 — PRODUCT REQUIREMENTS DOCUMENT
## From Reactive Chatbot to Autonomous Business Manager

**Owner:** Jay Schell
**Architect:** Claude Opus 4.6
**Builder:** Assigned by Jay (Claude Code / Anti-Gravity / Both)
**Date:** February 13, 2026
**Status:** ✅ APPROVED — Ready for build

---

## EXECUTIVE SUMMARY

Frankie is a Telegram-based AI assistant running on a Dell Precision 5810 in WSL (Ubuntu). He uses Claude CLI as his brain (`claude -p` on Jay's Max subscription), Supabase for vector memory, Google APIs for email/calendar/drive, and Grammy for Telegram.

**The problem:** Frankie has been running with partial amnesia. Only 2 of 4 memory files auto-inject. The Telegram bot and Claude Code terminal are separate runtimes with different memory paths. Google auth is split across two Cloud projects with incomplete scopes. Memory write-back (learning from conversations) was designed but never confirmed working. Frankie sits idle waiting for input instead of proactively managing Jay's businesses.

**The solution:** Three phases that each deliver working, testable functionality before the next begins. Phase 0 fixes the foundation. Phase 1 makes Frankie proactive with Discord as primary interface. Phase 2 scales him with sub-agents and business tools.

---

## CRITICAL RULES (NON-NEGOTIABLE)

Every builder must follow these. No exceptions.

1. **Claude CLI only.** Use `claude -p` via Max subscription. NEVER use `@anthropic-ai/sdk`. Never pay twice.
2. **Google APIs direct.** `googleapis` npm package. No AI middleman for tool execution.
3. **Validator always.** SAFE/CONFIRM/NEVER action classes on every tool call. 8-call limit per message.
4. **Working directory:** `~/frankie-bot/` in WSL. All work happens here. No new projects.
5. **Runtime:** Bun (not Node). Already configured.
6. **Trust but verify.** If Frankie claims "I fixed it," check actual files and logs. He CANNOT edit his own running code.
7. **Local files are source of truth.** Supabase accelerates search — it doesn't own the data.
8. **No building without passing prior phase tests.** Phase 1 doesn't start until Phase 0 tests all pass.
9. **Jay is not a coder.** Explain code plans in plain English. Step-by-step terminal instructions. Brief explanation of WHY decisions were made.

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

### Runtime 2: Telegram Bot (and future Discord bot)
- **Where:** `bun run src/relay.ts` — the bot Jay talks to daily
- **Brain:** Claude CLI via `claude -p` subprocess (spawned per message)
- **Prompt construction:** `src/claude-bridge.ts` builds the prompt manually
- **Memory injection:** Whatever claude-bridge.ts explicitly loads — currently: CLAUDE.md + Supabase vector search results + session history (last 20 messages)
- **NOT loaded:** SOUL.md, HEARTBEAT.md, MEMORY.md, contacts.md, projects.md (unless claude-bridge.ts is modified to load them)
- **Used for:** Daily operations, the actual Frankie Jay talks to

### What This Means
If we only fix memory for Claude Code, Telegram/Discord Frankie still has amnesia. Phase 0 must solve BOTH runtimes. Every test has a Claude Code version AND a Telegram version.

---

## DECISIONS MADE (February 13, 2026 — Jay + Frankie + Architect)

| Decision | Resolution |
|----------|-----------|
| Google Cloud projects | **One project: frankie1-486714.** Kill humanledai-485503 after migration. |
| MEMORY.md location | **Symlink** from `.claude/projects/.../memory/MEMORY.md` to `workspace/MEMORY.md`. One file, two paths. |
| Dashboard hosting | **Start local.** Jay's Dell Precision runs 24/7. Add Cloudflare tunnel later if mobile access needed. |
| Discord vs Dashboard first | **Discord first (Phase 1).** Telegram stays as fallback. Dashboard moves to Phase 2. |
| Sub-agent timeout | **60s default, 180s for research tasks.** Hard kill after timeout — terminate subprocess, don't just log. |
| humanledai@gmail.com autonomy | **Read=SAFE, Draft=SAFE, Send=CONFIRM, Delete=NEVER.** Daily cap: 10 sends/day. Revisit after 2 weeks. |
| Primary Google account | **jlpschell@gmail.com** = primary arm with full Drive R/W, Gmail, Calendar, Sheets. |
| humanledai@gmail.com role | **Stopgap** for business until jason@humanledai.net Workspace access is sorted. |
| jason@humanledai.net role | **Future primary business account.** Gets wired once Workspace admin grants OAuth consent. |

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
| contacts.md auto-injection | ✅ Working | Claude Code only |
| projects.md auto-injection | ✅ Working | Claude Code only |
| Scheduler (fires on time) | ✅ Working | Telegram |
| Validator layer (SAFE/CONFIRM/NEVER) | ✅ Working | Telegram |
| 44 skill files on disk | ✅ Exist | Neither (not wired for auto-discovery) |
| Knowledge files (GHL, YouTube, NotebookLM, Ghost) | ✅ Exist | On-demand read only |

### What's Broken or Missing
| Component | Status | Impact |
|-----------|--------|--------|
| SOUL.md injection | ❌ Not auto-loaded in either runtime | Identity/goals missing from Telegram prompts |
| HEARTBEAT.md injection | ❌ Not auto-loaded | Proactive behavior never triggered |
| Memory files in Telegram | ❌ MEMORY.md, contacts.md, projects.md not loaded | Telegram Frankie has amnesia |
| Memory auto-extraction (write-back) | ❓ Designed, never confirmed working | Frankie can't learn from conversations |
| Session history in Telegram | ❓ Designed, unconfirmed | May not remember same-session context |
| `public.library` table | ❌ Missing from Supabase | PGRST205 error fires every message |
| Google auth — scopes | ⚠️ Split across 2 projects, incomplete | Calendar/Gmail limited on workspace tools |
| Google auth — accounts | ⚠️ humanledai@gmail.com not authed, jason@humanledai.net not authed | Can't manage business email |
| Skill auto-discovery | ❌ Not wired | Skills exist but never load automatically |
| Heartbeat runner | ❌ Not built | Frankie waits for input |
| Sub-agent spawning | ❌ Not built | Everything runs through one brain |
| Goal system | ❌ Not built | No proactive task generation |
| GHL integration | ⚠️ API key exists, not wired | Can't manage CRM/pipelines |
| Discord | ❌ Not built | Single Telegram channel for everything |
| Duplicate memories in Supabase | ⚠️ ~100, should be ~17 | Wastes context window |
| Similarity threshold | ⚠️ Set to 0.1 (too low) | Returns junk results mixed with good ones |
| Old OAuth Drive sync | ⚠️ Logging 403 errors every 5 min | Noise in logs, masks real errors |

### File System (Verified by Frankie)
```
~/frankie-bot/
├── src/
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
│   │   └── gemini-bridge.ts      ← Utility only (NotebookLM, YouTube, search)
│   └── scheduler/
│       ├── scheduler-service.ts  ← Cron engine
│       ├── morning-brief.ts      ← 5:30 AM Central daily summary
│       └── nightly-wrapup.ts     ← 9:30 PM Central daily recap
├── workspace/
│   ├── CLAUDE.md                 ← Frankie personality + behavior (AUTO-INJECTED)
│   ├── CLAUDE.md.backup          ← Pre-upgrade backup
│   ├── SOUL.md                   ← Jay's identity (ON DISK ONLY — needs wiring)
│   ├── HEARTBEAT.md              ← Proactive checklist (ON DISK ONLY — needs wiring)
│   ├── MEMORY.md                 ← SYMLINK TARGET (needs creating — points to .claude/ copy)
│   ├── memory/                   ← Daily logs directory
│   ├── skills/                   ← Consolidated skill files (44 skills, 3 tiers)
│   │   ├── index.json            ← Skill trigger registry (needs wiring)
│   │   ├── copywriting/          ← 889-line copywriting weapon
│   │   ├── trading/              ← ORB strategy, Ghost, risk management
│   │   ├── ghl-mastery/          ← GoHighLevel reference
│   │   ├── build/                ← Tier 2: dev/build skills
│   │   └── agents/               ← Tier 3: agent architecture skills
│   ├── knowledge/                ← Reference material
│   │   ├── ghl_reference.md
│   │   ├── youtube_index.md
│   │   ├── notebooklm_index.md
│   │   └── quantcrawler_ghost_reference.md
│   └── credentials/              ← OAuth tokens, configs
│       ├── google_tokens.json    ← Token Set 1 (humanledai-485503 project)
│       └── token.json            ← Token Set 2 (frankie1-486714 project)
├── .claude/projects/.../memory/
│   ├── MEMORY.md                 ← Auto-memory (AUTO-INJECTED in Claude Code)
│   ├── contacts.md               ← Contact list (AUTO-INJECTED in Claude Code)
│   └── projects.md               ← Active projects (AUTO-INJECTED in Claude Code)
├── .env                          ← All API keys and tokens
├── portal/                       ← Windows/WSL shared folder (symlink)
└── logs/                         ← Runtime logs
```

### Google Auth State (Current)
| Token Set | Cloud Project | Account | Scopes | Used By |
|-----------|--------------|---------|--------|---------|
| workspace/google_tokens.json | humanledai-485503 | jlpschell@gmail.com | Gmail R/W, Calendar R, Drive R, YouTube R | Telegram bot (Gemini bridge) |
| workspace/credentials/token.json | frankie1-486714 | jlpschell@gmail.com | Sheets full, Drive full | Workspace tools (direct API) |
| (not authed) | — | humanledai@gmail.com | Has Drive access (granted manually) | Not connected |
| (not authed) | — | jason@humanledai.net | Inside humanledai.net Workspace | Not connected |

### Google Auth Target State (After Phase 0)
| Account | Cloud Project | Scopes | Role |
|---------|--------------|--------|------|
| jlpschell@gmail.com | frankie1-486714 | Gmail R/W, Calendar R/W, Drive full, Sheets full, YouTube R | Primary — Jay's personal |
| humanledai@gmail.com | frankie1-486714 | Gmail R/W, Calendar R/W, Drive full, Sheets full | Stopgap — business until Workspace sorted |
| jason@humanledai.net | frankie1-486714 | Gmail R/W, Calendar R/W | Future — wired when Workspace admin consents |

---

## PHASE 0: FOUNDATION
**Goal:** Bulletproof memory across both runtimes. Fix auth. Clean up debt.
**Timeline:** Complete before any other work.
**Builder:** Claude Code (Frankie) — he knows his own codebase best.

### 0.1 — Clean Supabase
**What:** Remove duplicate memories, create missing library table, fix threshold.
**Why:** 100 duplicates waste context window. Library table error fires every message. Low threshold returns junk.

**Steps:**
1. Run dedup SQL in Supabase SQL Editor:
```sql
DELETE FROM memories a USING memories b
WHERE a.content = b.content AND a.created_at < b.created_at;
SELECT COUNT(*) FROM memories;
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

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 0.1a | `SELECT COUNT(*) FROM memories;` | ~17 (not 100) |
| 0.1b | `SELECT COUNT(*) FROM library;` | Returns 0 (no PGRST205 error) |
| 0.1c | Send Frankie "Who is Benso?" via Telegram | Returns cat info, not junk |

---

### 0.2 — Wire ALL Memory Files Into Telegram Runtime
**What:** Modify `claude-bridge.ts` to load ALL memory files into every Telegram prompt.
**Why:** Telegram Frankie only gets CLAUDE.md + Supabase results today. He doesn't see SOUL.md, HEARTBEAT.md, contacts, projects, or daily logs.

**Create symlink** (one-time):
```bash
ln -sf ~/.claude/projects/.../memory/MEMORY.md ~/frankie-bot/workspace/MEMORY.md
```
*(Builder: find the actual `.claude/` path on Jay's machine and use it)*

**What claude-bridge.ts must do when building a prompt (in order):**
```
ALWAYS LOADED (local files — works even if cloud is down):
1. Read workspace/CLAUDE.md           → Personality & behavior rules
2. Read workspace/SOUL.md             → Jay's identity, goals, communication style
3. Read workspace/MEMORY.md           → Curated critical facts (symlinked)
4. Read workspace/memory/[today].md   → Today's session log (if exists)
5. Read workspace/memory/[yesterday].md → Yesterday's log (if exists)

LOADED WHEN AVAILABLE (cloud — graceful failure):
6. Search Supabase via match_memories() → Semantic search relevant to this message
   └── If Supabase fails → Log warning, continue (local files cover baseline)

ALWAYS LOADED (session):
7. Last 20 messages from session-manager.ts → Conversation context
```

**Formatting:** Wrap each source in XML-style tags so Claude can distinguish:
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
[Supabase vector search results]
</relevant_memories>

<conversation_history>
[last 20 messages]
</conversation_history>

<current_message>
[Jay's message]
</current_message>
```

**Implementation rules:**
- Read files with try/catch — if any file missing, log warning and continue
- Total injected context should stay under 8,000 tokens to leave room for response
- If total exceeds limit, trim daily logs first, then reduce Supabase results count
- Add logging: `console.log("CONTEXT LOADED: CLAUDE.md ✅ | SOUL.md ✅ | MEMORY.md ✅ | today.md ❌ (not found)")` etc.

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 0.2a | Restart bot. Send: "What are my 12-month goals?" | Returns goals from SOUL.md |
| 0.2b | Send: "Who is Patti Baker?" | Returns "GAIG account manager" |
| 0.2c | Send: "What's my cat's name?" | Returns "Benso/Benson, tuxedo cat" |
| 0.2d | Check logs after any message | Shows each file loaded/skipped with ✅/❌ |

---

### 0.3 — Confirm Session History Works
**What:** Verify session-manager.ts passes last 20 messages to claude-bridge.ts.
**Why:** Without this, Frankie can't remember what you said 2 minutes ago.

**Steps:**
1. Read `src/session-manager.ts` — confirm it stores messages per user
2. Read `src/claude-bridge.ts` — confirm it calls session-manager for history
3. Add logging: `console.log("SESSION HISTORY: " + messages.length + " messages included")`

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 0.3a | Send: "My brother's name is Ryan" then "What's my brother's name?" | Answers "Ryan" (same session) |
| 0.3b | Check logs | Shows "SESSION HISTORY: 2 messages included" |

---

### 0.4 — Memory Write-Back (Auto-Extraction)
**What:** When Jay tells Frankie a fact, it must get stored in Supabase AND appended to today's daily log.
**Why:** Designed in every planning doc. Never confirmed working. This is the difference between learning and pretending.

**How it works:**
1. Jay sends message → Claude responds
2. AFTER response, separate extraction step runs
3. Extraction prompt to Claude CLI: "Extract any new facts about Jay from this exchange. Return JSON: [{content, category}]. Categories: fact, preference, decision, goal, person. Empty array if none."
4. For each extracted fact:
   - Generate embedding via OpenAI text-embedding-ada-002
   - Insert into Supabase `memories` table with embedding
   - Append to `workspace/memory/YYYY-MM-DD.md` (today's log)
5. Only say "filed away" AFTER Supabase write confirmed
6. If write fails: "I tried to remember that but had a database issue"

**If extraction code doesn't exist:** Build it in `claude-bridge.ts` as a post-response step.

**TESTS (THE BISCUIT TEST):**
| ID | Test | Expected |
|----|------|----------|
| 0.4a | Send: "Remember that my dog's name is Biscuit" | Confirms stored |
| 0.4b | Check logs | Shows "MEMORY EXTRACTED: 1 new facts stored" |
| 0.4c | `pkill -f bun && sleep 5 && cd ~/frankie-bot && bun run src/relay.ts` | Bot restarts clean |
| 0.4d | Send: "What's my dog's name?" | Answers "Biscuit" |
| 0.4e | Check `workspace/memory/2026-02-XX.md` | Contains "dog's name is Biscuit" entry |

---

### 0.5 — Google Auth Consolidation
**What:** Consolidate to one Cloud project (frankie1-486714). Auth all needed accounts.
**Why:** Split auth = split capabilities. Calendar on one token, Drive on another, business email not connected at all.

**Target state:**
| Account | Scopes | Purpose |
|---------|--------|---------|
| jlpschell@gmail.com | Gmail R/W, Calendar R/W, Drive full, Sheets full, YouTube R | Jay's personal — primary arm |
| humanledai@gmail.com | Gmail R/W, Calendar R/W, Drive full, Sheets full | Business stopgap until Workspace sorted |
| jason@humanledai.net | Gmail R/W, Calendar R/W | Workspace — wire when admin consents |

**Steps (Jay does these — requires browser):**
1. Use frankie1-486714 Cloud project for all accounts
2. Run OAuth flow for jlpschell@gmail.com with ALL scopes listed above
3. Run OAuth flow for humanledai@gmail.com with ALL scopes listed above
4. Store in `.env` with clear naming:
```env
# Personal (jlpschell@gmail.com)
GOOGLE_PERSONAL_CLIENT_ID=
GOOGLE_PERSONAL_CLIENT_SECRET=
GOOGLE_PERSONAL_REFRESH_TOKEN=

# Business (humanledai@gmail.com)
GOOGLE_BUSINESS_CLIENT_ID=
GOOGLE_BUSINESS_CLIENT_SECRET=
GOOGLE_BUSINESS_REFRESH_TOKEN=

# Workspace (jason@humanledai.net) — future
GOOGLE_WORKSPACE_CLIENT_ID=
GOOGLE_WORKSPACE_CLIENT_SECRET=
GOOGLE_WORKSPACE_REFRESH_TOKEN=
```
5. Update `google-api.ts` to accept an `account` parameter (`personal` | `business` | `workspace`) so Frankie specifies which account per operation
6. Update old token references to use new naming

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 0.5a | Send: "Search my Drive for claims" | Returns results from jlpschell Drive |
| 0.5b | Send: "Check the business inbox" | Returns emails from humanledai@gmail.com |
| 0.5c | Send: "What's on my calendar tomorrow?" | Returns real calendar events |
| 0.5d | No 401/403 errors in logs | Clean auth |

---

### 0.6 — Disable Old OAuth Drive Sync + Clean Logs
**What:** Stop the old Drive sync spamming 403 errors every 5 minutes.
**Why:** Log noise masks real errors.

```bash
grep -rn "drive-sync\|drivesync\|DriveSync\|ACCESS_TOKEN_SCOPE" src/
```
Find and disable the interval/cron. Don't delete files — just stop execution.

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 0.6a | Restart Frankie, watch logs 5 min | No "ACCESS_TOKEN_SCOPE_INSUFFICIENT" errors |

---

### PHASE 0 — GATE CHECK
**ALL must pass before Phase 1 begins.**

| # | Test | Pass? |
|---|------|-------|
| 0.1a | Supabase has ~17 memories (not 100) | ☐ |
| 0.1b | Library table exists (no PGRST205 error) | ☐ |
| 0.1c | "Who is Benso?" returns cat info via Telegram | ☐ |
| 0.2a | "What are my 12-month goals?" returns SOUL.md goals via Telegram | ☐ |
| 0.2b | "Who is Patti Baker?" returns GAIG info via Telegram | ☐ |
| 0.2c | "What's my cat's name?" returns Benso via Telegram | ☐ |
| 0.2d | Logs show all memory files loaded with ✅/❌ | ☐ |
| 0.3a | Same-session recall: "brother = Ryan" test passes | ☐ |
| 0.3b | Logs show session history count | ☐ |
| 0.4a | Biscuit test: learn → restart → recall | ☐ |
| 0.4b | Daily log file contains new fact | ☐ |
| 0.5a | Personal Drive search works | ☐ |
| 0.5b | Business email check works | ☐ |
| 0.5c | Calendar check works | ☐ |
| 0.5d | No auth errors in logs | ☐ |
| 0.6a | No 403 Drive sync errors in 5 min | ☐ |

**Jay signs off:** _________________ **Date:** _____________
**Frankie confirms (via Telegram):** _________________ **Date:** _____________

---

## PHASE 1: FRANKIE WORKS ALONE
**Goal:** Single agent, fully capable, proactively managing Jay's businesses. Discord as primary interface.
**Prereq:** Phase 0 gate check 100% pass.
**Timeline:** 1-2 weeks after Phase 0.

### 1.1 — Discord Bot Setup
**What:** Build Discord bot as primary interface. Telegram stays as fallback.
**Why:** Channels per business area > one endless Telegram thread. Better for sub-agents later. Better bot API (embeds, buttons, threads).

**Channel structure:**
| Channel | Purpose |
|---------|---------|
| #general | Chat with Frankie, ask anything |
| #human-led-ai | Business: leads, GHL updates, campaigns, outreach |
| #trading | Trade logs, P&L, risk alerts, Ghost status |
| #personal | Calendar, email summaries, reminders, Alacrity stuff |
| #frankie-logs | Transparency: what Frankie did today (auto-posted) |

**Technical:**
- Discord.js library
- Separate bot token (Jay creates in Discord Developer Portal)
- Same brain: `claude -p` subprocess with same prompt construction as Telegram
- Same memory: reads same files, same Supabase, same session manager
- Same validator: SAFE/CONFIRM/NEVER applies identically
- Channel-aware routing: messages in #trading get trading context, #human-led-ai gets business context

**What stays on Telegram:**
- Quick pings when you don't want to open Discord
- Heartbeat alerts (sent to both platforms)
- Backward compatibility — nothing breaks

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 1.1a | Send message in #general | Frankie responds with personality |
| 1.1b | Send "Who is Benso?" in #general | Correct memory recall |
| 1.1c | Send "Check my email" in #personal | Returns email summary |
| 1.1d | Send same via Telegram | Same result (backward compat) |

---

### 1.2 — Skill Auto-Discovery
**What:** Frankie automatically loads the relevant skill file when Jay's message matches triggers.
**Why:** 44 skills exist on disk but never load unless manually requested. The copywriting skill is 889 lines of weapon that never fires.

**Implementation:**
1. `workspace/skills/index.json` contains skill triggers — verify it exists and is complete
2. In `claude-bridge.ts`: before sending prompt, scan message against triggers in index.json
3. If match found, read that skill's SKILL.md and append to prompt inside `<active_skill>` tags
4. If no match, skip (just personality + memory — no skill needed for casual chat)
5. Max 1 skill loaded per message (pick highest match count if multiple trigger)
6. Log: `console.log("SKILL LOADED: copywriting")` or `console.log("SKILL LOADED: none")`

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 1.2a | "Write me a cold email for an HVAC contractor in Plano" | Response follows copywriting SKILL.md structure. Logs: "SKILL LOADED: copywriting" |
| 1.2b | "Good morning Frankie" | Casual response. Logs: "SKILL LOADED: none" |
| 1.2c | "Check my MNQ P&L" | Trading context loaded. Logs: "SKILL LOADED: trading" |

---

### 1.3 — Goal System
**What:** `/goal` command stores goals in Supabase. Goals feed morning brief.
**Why:** This enables auto-task generation — OpenClaw's killer feature adapted for Frankie.

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
CREATE INDEX idx_goals_user_status ON goals(user_id, status);
```

**Commands:**
- `/goal Scale Human Led AI to $15K/month` → Stores goal, confirms
- `/goals` → Lists all active goals with categories
- `/goal-done [id]` → Marks goal as achieved, moves to archive

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 1.3a | `/goal Grow Human Led AI to 10 clients by April` | "Goal stored: Grow Human Led AI to 10 clients by April" |
| 1.3b | `/goals` | Lists the goal just created |
| 1.3c | `/goal-done [id]` | Marks as achieved, disappears from active list |

---

### 1.4 — Auto-Task Generation (Morning Brief Upgrade)
**What:** Every morning at 5:30 AM Central, Frankie reads goals, generates 4 tasks, includes them in morning brief.
**Why:** Frankie stops waiting. He wakes up, makes a plan, and gets to work.

**Flow:**
1. `morning-brief.ts` queries `goals` table for active goals
2. Sends to Claude CLI: "Given these goals, suggest 4 specific tasks Jay or I can complete today. Return JSON array."
3. Creates tasks in `scheduled_tasks` with `task_type: 'auto-generated'`
4. Morning brief Telegram + Discord message includes: "🎯 TODAY'S TASKS: [list]"
5. Hard limit: Max 4 auto-tasks per day (prevents runaway generation)

**Modified `scheduled_tasks` table:**
```sql
ALTER TABLE scheduled_tasks ADD COLUMN IF NOT EXISTS created_by TEXT DEFAULT 'user';
ALTER TABLE scheduled_tasks ADD COLUMN IF NOT EXISTS goal_id UUID REFERENCES goals(id);
```

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 1.4a | Create 2-3 goals via `/goal` | Goals stored |
| 1.4b | Trigger morning brief (manually or wait for 5:30 AM) | Brief includes 4 auto-generated tasks |
| 1.4c | Tasks are specific and actionable | Not vague ("research HVAC market in Rockwall" not "work on business") |

---

### 1.5 — Heartbeat Runner
**What:** Separate process. Runs every 30 minutes. Checks email, calendar, trades. Alerts Jay only when needed.
**Why:** This is what transforms Frankie from ChatGPT to a business manager.

**Architecture:**
- New file: `src/heartbeat-runner.ts` — SEPARATE from relay.ts
- Reads `workspace/HEARTBEAT.md` for checklist
- Checks:
  - Email: all authed accounts (flag urgent senders, keywords)
  - Calendar: events in next 2 hours
  - Trading: P&L and drawdown (during market hours only: weekdays 9:15-4:15 ET)
  - Portal: new files in `~/frankie-bot/portal/to-frankie/`
- If something needs attention → sends message to Telegram AND Discord #personal
- If nothing → stays silent, logs "HEARTBEAT_OK"
- Anti-spam: max 3 messages per hour
- De-duplication: don't repeat same alert from previous cycle

**Launch:**
```bash
# Run alongside main bot (separate process)
cd ~/frankie-bot && nohup bun run src/heartbeat-runner.ts > logs/heartbeat.log 2>&1 &
```

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 1.5a | Start heartbeat runner | Logs show "HEARTBEAT STARTED — checking every 30 min" |
| 1.5b | Unread urgent email exists | Jay gets Telegram + Discord alert |
| 1.5c | No events, no urgent email | Logs show "HEARTBEAT_OK", no message sent |
| 1.5d | Drop a file in portal/to-frankie/ | Next heartbeat: "I see you dropped [filename] in the portal" |

---

### 1.6 — Email Management (All Accounts)
**What:** Check, search, read, draft, send email across all authed accounts.
**Why:** Jay wants humanledai@gmail.com managed semi-autonomously. Personal email triaged.

**Commands:**
- `/email` or "check my email" → Flagged/urgent from all accounts
- `/email personal` → Last 10 from jlpschell
- `/email business` → Last 10 from humanledai@gmail.com
- "Draft a reply to the GAIG email" → CONFIRM class (shows draft, waits for approval)
- "Send this to john@example.com from humanledai" → CONFIRM class

**Action classes:**
| Action | Class | Notes |
|--------|-------|-------|
| Read email | SAFE | Auto-execute |
| Search email | SAFE | Auto-execute |
| Draft email | SAFE | Shows draft, doesn't send |
| Send email (personal) | CONFIRM | Jay must approve |
| Send email (business) | CONFIRM | Jay must approve. Max 10/day. |
| Delete email | NEVER | Jay does this himself |

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 1.6a | "Check my business email" | Returns recent from humanledai@gmail.com |
| 1.6b | "Draft a reply to [email] saying we'll follow up next week" | Shows draft, asks for approval |
| 1.6c | Approve draft | Email sends from correct account |
| 1.6d | 11th send attempt in one day | Blocked: "Daily send limit (10) reached for business account" |

---

### 1.7 — Calendar Management
**What:** Read, create, manage calendar events across accounts.
**Why:** Scheduling is daily overhead Frankie should handle.

**Commands:**
- `/calendar` or "What's on my schedule?" → Today's events
- `/calendar tomorrow` → Tomorrow's events
- "Schedule a call with Baker at 3pm Friday" → CONFIRM class
- "Block 2 hours for deep work tomorrow morning" → CONFIRM class

**Action classes:**
| Action | Class |
|--------|-------|
| Read calendar | SAFE |
| Create event | CONFIRM |
| Modify event | CONFIRM |
| Delete event | NEVER |

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 1.7a | "What's on my calendar today?" | Returns real events (or "nothing scheduled") |
| 1.7b | "Remind me about Baker deadline at 3pm" | Creates event after confirmation |

---

### PHASE 1 — GATE CHECK

| # | Test | Pass? |
|---|------|-------|
| 1.1a | Discord bot responds in #general | ☐ |
| 1.1b | Discord memory recall works | ☐ |
| 1.1d | Telegram still works (backward compat) | ☐ |
| 1.2a | Cold email loads copywriting skill | ☐ |
| 1.3a | /goal stores goal | ☐ |
| 1.3b | /goals retrieves goals | ☐ |
| 1.4b | Morning brief includes 4 auto-tasks | ☐ |
| 1.5b | Heartbeat detects urgent email and alerts | ☐ |
| 1.6a | Business email check works | ☐ |
| 1.6c | Email send with CONFIRM works | ☐ |
| 1.7a | Calendar read works | ☐ |
| 1.7b | Calendar event creation works | ☐ |

**Jay signs off:** _________________ **Date:** _____________

**MANDATORY: Use Frankie daily for 1-2 weeks before starting Phase 2. Confirm stability.**

---

## PHASE 2: FRANKIE DELEGATES
**Goal:** Sub-agents, GHL integration, dashboard, GitHub.
**Prereq:** Phase 1 gate check 100% pass + 1-2 weeks daily use confirming stability.
**Timeline:** 2-4 weeks after Phase 1 stabilizes.

### 2.1 — Sub-Agent Architecture
**What:** Manager/Worker pattern. Frankie dispatches specialist agents for complex tasks.

**How it works:**
1. Jay sends: "Write me a cold email for a roofer in Rockwall"
2. Manager checks skill index → matches copywriting → has `sub_agent` defined
3. Manager builds focused prompt: SKILL.md + relevant context only (not full memory)
4. Manager spawns: `claude -p "[focused prompt]"` with timeout
5. Sub-agent returns result
6. Manager wraps in Frankie's voice, sends to Jay
7. Manager logs to daily memory file

**Sub-agents (build in order):**

| Agent | Gets | Does | Cannot |
|-------|------|------|--------|
| Copywriting | SKILL.md + brand identity + target info | Cold emails, DMs, ad copy, landing pages | Access trading data, check calendar |
| Trading | TRADING_SKILL.md + trades table data | Log trades, P&L, drawdown, ORB validation | Execute trades, read email |
| Email | Email skill + SOUL.md communication style | Triage inbox, draft responses, flag urgent | Send without CONFIRM routing |
| GHL | ghl-mastery SKILL.md + GHL API access | CRM, pipelines, contacts, campaigns | Make live API calls without CONFIRM |

**Rules:**
- Sub-agents get ONLY their skill + minimal context (not full memory)
- Sub-agents CANNOT talk to Jay directly — only through Manager
- Sub-agents route through Validator (SAFE/CONFIRM/NEVER still applies)
- **Timeout: 60 seconds default. 180 seconds for research tasks. HARD KILL after timeout** — terminate subprocess, don't just log
- Max 1 sub-agent per user message (no chaining without Manager approval)

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 2.1a | "Write a cold email for a roofer in Rockwall" | Delegates to copywriting agent. Response follows SKILL.md. |
| 2.1b | "Good morning" | Manager handles directly (no delegation) |
| 2.1c | Sub-agent exceeds 60s | Process killed, Jay gets: "Task timed out — want me to try again?" |

---

### 2.2 — GHL Deep Integration
**What:** Frankie manages GoHighLevel CRM, pipelines, contacts, campaigns.
**Why:** GHL is the money-maker for Human Led AI. This is where Frankie earns his keep.

**GHL_API_KEY and GHL_LOCATION_ID already exist in .env.**

**Functions to build:**
- Create/update contacts
- Move contacts through pipelines
- Send SMS/emails via GHL
- Create/update opportunities
- Tag contacts
- Search by tag/pipeline/status
- Trigger workflows

**Commands:**
| Command | Action Class |
|---------|-------------|
| "Show pipeline summary" | SAFE |
| "Show leads tagged roofing-quote" | SAFE |
| "Add John Doe to HVAC pipeline" | CONFIRM |
| "Send follow-up to stale leads" | CONFIRM |
| "Delete contact" | NEVER |
| Mass messaging (50+ contacts) | NEVER |

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 2.2a | "Show me all contacts in the HVAC pipeline" | Returns real GHL data |
| 2.2b | "Add John Doe 555-1234 to roofing pipeline" | Creates contact after CONFIRM |
| 2.2c | "Send follow-up to all leads tagged roofing-quote" | Shows plan, waits for CONFIRM, sends via GHL |

---

### 2.3 — Second Brain Dashboard (Local)
**What:** Visual web interface showing Frankie's brain and activity.
**Why:** Jay needs to see inside Frankie without asking via Telegram/Discord.

**Pages:**
| Page | Content |
|------|---------|
| Home | Stats: memory count, active goals, tasks today, unread emails |
| Memories | Search, filter by category, add/delete |
| Tasks | Kanban: To Do → In Progress → Done |
| Goals | Active goals, progress, archive |
| Conversations | Browse past chats with search |

**Tech:** NextJS 14, Tailwind CSS, shadcn/ui, Supabase direct connection.
**Hosting:** Local at `http://localhost:3000`. Password-protected.
**Future:** Add Cloudflare tunnel for mobile access if needed.

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 2.3a | Open localhost:3000 | Dashboard loads, shows stats |
| 2.3b | Search memories for "Benso" | Returns cat memory |
| 2.3c | Kanban shows today's auto-generated tasks | Tasks visible in "To Do" column |

---

### 2.4 — GitHub Integration
**What:** Version control for Frankie's codebase.
**Why:** Jay wants to fork to laptop, track changes, prevent losing work to session deaths.

**Commands:**
| Command | Action Class |
|---------|-------------|
| "Show what changed since yesterday" | SAFE |
| "Commit today's changes" | CONFIRM |
| "Create branch for GHL update" | CONFIRM |
| "Push to main" | NEVER (always branch first) |

**Technical:** GitHub CLI (`gh`) or Octokit. OAuth. All pushes go to branches, never main.

**TESTS:**
| ID | Test | Expected |
|----|------|----------|
| 2.4a | "Commit today's changes with message: phase 1 complete" | Creates commit after CONFIRM |
| 2.4b | "Show diffs from yesterday" | Shows file changes |

---

### PHASE 2 — GATE CHECK

| # | Test | Pass? |
|---|------|-------|
| 2.1a | Cold email delegates to copywriting agent | ☐ |
| 2.1c | Sub-agent timeout kills process | ☐ |
| 2.2a | GHL pipeline search returns data | ☐ |
| 2.2b | GHL contact creation with CONFIRM works | ☐ |
| 2.3a | Dashboard loads at localhost:3000 | ☐ |
| 2.3c | Kanban shows auto-generated tasks | ☐ |
| 2.4a | Git commit from Telegram/Discord works | ☐ |

**Jay signs off:** _________________ **Date:** _____________

---

## COMMAND REFERENCE (All Phases)

### Phase 0 (No new user commands — infrastructure only)
Existing: `/help`, `/remember [fact]`, `/status`, `/clear`

### Phase 1 (New)
| Command | What It Does |
|---------|-------------|
| `/goal [description]` | Store a business/personal goal |
| `/goals` | List all active goals |
| `/goal-done [id]` | Mark goal as achieved |
| `/email` | Check urgent/flagged across all accounts |
| `/email personal\|business` | Check specific account |
| `/calendar` | Today's schedule |
| `/calendar tomorrow` | Tomorrow's schedule |

### Phase 2 (New)
| Command | What It Does |
|---------|-------------|
| `/pipeline` | GHL pipeline summary |
| `/leads [niche]` | Search GHL contacts by tag/niche |
| `/trades` | Today's trades |
| `/pnl` | P&L summary |
| `/risk` | Drawdown status per account |
| `/search [query]` | Search library/knowledge base |

---

## ENVIRONMENT VARIABLES (Target State)

```env
# === Telegram ===
TELEGRAM_BOT_TOKEN=
ALLOWED_USER_IDS=

# === Discord (Phase 1) ===
DISCORD_BOT_TOKEN=
DISCORD_GUILD_ID=

# === Database ===
SUPABASE_URL=
SUPABASE_ANON_KEY=

# === AI ===
OPENAI_API_KEY=           # Embeddings only (text-embedding-ada-002)
GEMINI_API_KEY=           # Utility: NotebookLM, YouTube, search
GEMINI_API_KEY_2=         # Fallback
GEMINI_API_KEY_3=         # Fallback

# === Google Personal (jlpschell@gmail.com) ===
GOOGLE_PERSONAL_CLIENT_ID=
GOOGLE_PERSONAL_CLIENT_SECRET=
GOOGLE_PERSONAL_REFRESH_TOKEN=

# === Google Business (humanledai@gmail.com — stopgap) ===
GOOGLE_BUSINESS_CLIENT_ID=
GOOGLE_BUSINESS_CLIENT_SECRET=
GOOGLE_BUSINESS_REFRESH_TOKEN=

# === Google Workspace (jason@humanledai.net — future) ===
GOOGLE_WORKSPACE_CLIENT_ID=
GOOGLE_WORKSPACE_CLIENT_SECRET=
GOOGLE_WORKSPACE_REFRESH_TOKEN=

# === Business Tools ===
GHL_API_KEY=
GHL_LOCATION_ID=
ELEVENLABS_API_KEY=
```

---

## SUCCESS CRITERIA

**Phase 0:** Jay messages Telegram Frankie cold (fresh restart) and gets memory-aware responses referencing goals, contacts, and recent conversations. No amnesia. No auth errors. Biscuit test passes.

**Phase 1:** Jay wakes up to a morning brief in Discord with 4 auto-generated tasks. Frankie alerts about urgent emails and upcoming meetings via heartbeat. Jay manages email and calendar through Discord channels. Skills auto-load for specialized requests.

**Phase 2:** Jay says "write a cold email for a roofer" and gets Hormozi-quality copy in 15 seconds via sub-agent. GHL pipelines update without Jay touching the CRM. Dashboard shows what Frankie did all day. Code is version-controlled.

**Ultimate:** Jay works his Alacrity day job. Comes home. Frankie has done 4+ hours of business development, lead gen, email management, and admin. The path to $15K-$25K/month gets shorter every week.

---

*End of PRD — Approved by Jay, Frankie, and Architect*
*February 13, 2026*
