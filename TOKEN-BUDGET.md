# Token Budget — Hard Limits (MANDATORY)

**Purpose:** Stop burning Jay's money on context bloat. Every token costs real dollars. Rate limits = YOU failing.

---

## Token Budgets by Task Type (ENFORCED)

| Task Type | Max Context | Model | Cost/M | When to Use |
|-----------|-------------|-------|--------|-------------|
| **Greeting / Simple Q&A** | 5k | Haiku | $0.80 in / $4 out | "Hello", "What's status?", "How many X?" |
| **Memory Recall** | 20k | Sonnet | $3 in / $15 out | "What did we do yesterday?", "When was X?" |
| **Task Execution** | 50k | Sonnet | $3 in / $15 out | "Build Y", "Write Z", "Fix config" |
| **Complex Reasoning** | Full (200k) | Opus | $5 in / $25 out | Only when Jay explicitly requests |
| **Heartbeat** | 2k | Haiku | $0.80 in / $4 out | Every 30 min automated check |
| **Morning Brief** | 30k | Sonnet | $3 in / $15 out | 5:30 AM daily summary |
| **A2P Check** | 5k | Haiku | $0.80 in / $4 out | 9 AM daily status check |

---

## Loading Rules (NON-NEGOTIABLE)

### NEVER Auto-Load:
- ❌ Full workspace files (SOUL.md, MEMORY.md, skills, etc.) — 20k+ tokens wasted
- ❌ All conversation history — keep last 5 exchanges max
- ❌ Prior tool responses unless directly relevant to current task
- ❌ Skill docs "just in case" — load ONLY when task requires that skill

### ALWAYS:
- ✅ Run `memory_search` before loading any workspace file
- ✅ Use `memory_get` with offsets to pull ONLY relevant lines
- ✅ Load workspace files surgically (specific sections, not entire files)
- ✅ Stay within token budget for task type

### Example: WRONG vs RIGHT

**❌ WRONG (Old Behavior):**
```
User: "Hello"
Agent loads: SOUL.md (5k) + MEMORY.md (8k) + ACTIVE-TASKS.md (4k) + conversation history (10k) = 27k tokens
Agent: "Hey Jay! [rambling update]"
Total: 27k tokens for a greeting
```

**✅ RIGHT (New Behavior):**
```
User: "Hello"
Agent loads: NOTHING
Agent: "Hey Jay! What do you need?"
Total: <1k tokens
```

**❌ WRONG (Memory Recall):**
```
User: "What did we do yesterday?"
Agent loads: Full daily note (15k) + MEMORY.md (8k) + ACTIVE-TASKS.md (4k) = 27k tokens
Agent: "Yesterday we..."
```

**✅ RIGHT (Memory Recall):**
```
User: "What did we do yesterday?"
Agent runs: memory_search("yesterday activities")
Agent runs: memory_get("memory/2026-02-19.md", lines=50)
Agent loads: 2k tokens
Agent: "Yesterday we..."
```

---

## Heartbeat Token Breakdown (2k Budget)

| Step | Command | Max Tokens | Why |
|------|---------|------------|-----|
| Daily note check | `ls memory/YYYY-MM-DD.md` | 500 | File exists? Create if missing. |
| Task status | `grep "Status:" ACTIVE-TASKS.md` | 800 | Scan for idle tasks only. |
| Pending items | `grep "Pending:" memory/YYYY-MM-DD.md` | 300 | Check for follow-ups only. |
| Inbox check | `sb-sync.sh inbox prime \| wc -l` | 400 | Message count, don't read. |
| System health | `curl -s supabase_url` (optional) | 200 | Skip if budget tight. |

**Total: 2,200 tokens max** (includes model overhead)

**If exceeded:** You FAILED the heartbeat. Heartbeats are status checks, not conversations.

---

## Model Selection Rules

### Use Haiku When:
- Task is pattern matching (status checks, greetings, simple lookups)
- No reasoning required
- Answer exists in memory or simple data check
- **Examples:** "Hello", "A2P status?", "Lead count?", heartbeats

### Use Sonnet When:
- Task requires thought (building, writing, analyzing)
- Multi-step execution
- Memory recall + synthesis
- **Examples:** "Build dashboard", "Write PRD", "What happened yesterday?"

### Use Opus When:
- Jay explicitly says "use Opus" or `/model opus`
- Complex architecture decisions (multiple trade-offs)
- Strategic analysis requiring deep reasoning
- **Examples:** "Design the entire system", "Evaluate 10 options and recommend"

**NEVER use Opus by default.** It's 67% more expensive than Sonnet for marginal benefit on most tasks.

---

## Enforcement

### How to Stay Within Budget:

**Before responding:**
1. Check task type → look up max context
2. Estimate current context size (tokens used so far)
3. If over budget → trim context aggressively or ask Jay to expand scope

**During task:**
- Load files with `limit=` parameter (e.g., `Read(file, limit=50)` not full file)
- Use `memory_get(from=X, lines=Y)` not full memory read
- Grep/head/tail outputs instead of loading entire tool responses

**After task:**
- Run `session_status` to check token usage
- If >80% of budget used, log it and tighten next time

### Violations:

**If you exceed token budget:**
- You wasted Jay's money
- You're ignoring explicit directives
- You're creating rate limit risk

**Rate limit = FAILURE.** Two rate limits in 24 hours means you're not following this protocol.

---

## Multi-Model Future (When Jay Adds OpenAI/Gemini/Llama/Kimi)

Once other providers are configured, routing will change:

| Task | Primary | Fallback | Cost |
|------|---------|----------|------|
| Greetings/Heartbeats | Gemini Flash / Haiku | GPT-4o-mini | Cheapest |
| Memory Recall | Sonnet / GPT-4o | Gemini Pro | Mid-range |
| Task Execution | Sonnet / GPT-4o | Claude Haiku | Mid-range |
| Code Generation | GPT-4o / Claude Sonnet | Gemini Pro | Best for code |
| Complex Reasoning | Opus / o1 | Claude Sonnet | Premium only |

**Goal:** Reserve Claude ($$$) for what it's best at. Use cheaper models (OpenAI, Gemini, Llama) for routine work.

---

## Current Session Token Waste Example

**This session (as of now):**
- Tokens used: 132k/200k (66%)
- Messages: ~100 exchanges
- **Problem:** Auto-loading workspace files every message (20k+ per exchange)

**What should have happened:**
- "Hello" → 1k tokens (no workspace load)
- Simple Q&A → 5k tokens (memory search only)
- Research task → 30k tokens (browser + web fetch results)
- **Total budget:** ~50k tokens instead of 132k

**Savings:** 82k tokens = $0.25 saved on input alone (Sonnet @ $3/M)

**Multiply that by 50 sessions/day = $12.50/day savings = $375/month**

That's real money. That's why this matters.

---

## Summary

**Three rules:**
1. **NEVER auto-load workspace files** — memory search first, surgical loads only
2. **ALWAYS stay within token budget** — if task exceeds budget, ask Jay to expand scope
3. **USE CHEAP MODELS** — Haiku for greetings/heartbeats, Sonnet for work, Opus only when Jay says so

**This is not optional. This is how you operate.**
