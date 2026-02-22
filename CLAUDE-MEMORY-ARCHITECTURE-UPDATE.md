# Frankie Memory Architecture Update for Claude

## Context Optimization Completed (Just Finished)

We just completed a major context optimization that reduced brain file bloat by 33% and created a proper separation of concerns:

### Before/After Brain Files:
| File | Before | After | Reduction |
|------|--------|--------|-----------|
| **AGENTS.md** | 245 lines, 16KB | 39 lines, 4KB | **-75%** |
| **SOUL.md** | 88 lines, 8KB | 37 lines, 4KB | **-50%** |
| **MEMORY.md** | 106 lines, 8KB | 55 lines, 4KB | **-50%** |
| **TOOLS.md** | 31 lines, 4KB | 23 lines, 4KB | **0%** |
| **Total** | **36KB** | **24KB** | **-33%** |

### New Skills System (4KB total):
Moved detailed procedures to skills, keeping brain files focused:
- `skills/memory-management/` — Session protocols, daily notes, retrieval
- `skills/verification-protocol/` — Truth over speed, source citation  
- `skills/token-conservation/` — Memory-first loading, context budgets
- `skills/workspace-rules/` — INVENTORY.md checks, .env access

## Current Memory Architecture

### Layer 1: Persistent Memory (Redis + Qdrant)
- **Redis:** Session state, counters, flags, real-time data
- **Qdrant:** Vector embeddings for semantic search across all memories
- **Supabase:** Shared memory between Prime (Dell) and Mobile (Vivobook) instances
- **Both instances tag writes:** [Prime] or [Mobile] for source tracking

### Layer 2: Daily Logs (`memory/YYYY-MM-DD.md`)
**Write Schedule:**
- Every meaningful conversation (>2 exchanges)
- Before session end/idle
- When Jay assigns tasks
- When actions complete
- When decisions are made
- Every 3-5 message exchanges during active work

**Format:**
```markdown
# Daily Log — YYYY-MM-DD

## [TIME] — [Topic]
- Discussed: [what]
- Actions: [what done, with specifics/numbers]
- Pending: [what's next]
- Decisions: [Jay's choices]
```

### Layer 3: Core Memory (`MEMORY.md`)
**Write Schedule:**
- Nightly wrapup (9:30 PM) — day's highlights
- When permanent facts change (new contacts, accounts, preferences)
- Business decisions that affect ongoing operations
- NOT for daily events (those go in daily logs)

### Layer 4: Active Tasks (`ACTIVE-TASKS.md`)
**Write Schedule:**
- When tasks start/change status/complete
- During heartbeats if tasks are stale
- End-of-day status updates
- Real-time updates as work progresses

## Token Conservation System

### Memory-First Loading Protocol:
1. **NEVER auto-load workspace files**
2. **ALWAYS check memory first** — `memory_search` + `memory_get`
3. **Load only what's needed** — surgical, not blanket loading
4. **Hard token budgets by task type:**

| Task Type | Max Context | Model | Use Case |
|-----------|-------------|-------|----------|
| Simple Q&A | 5k tokens | Haiku | Greetings, status checks |
| Memory recall | 20k tokens | Sonnet | Past events, decisions |
| Complex tasks | 50k tokens | Sonnet | Building, analysis |
| Heartbeats | 2k tokens | Haiku | Status check only |

### Retrieval Chain:
1. `memory_search` semantic search across all memory
2. `memory_get` for exact lines from specific files
3. Cross-reference ACTIVE-TASKS.md and MEMORY.md
4. **ONLY then** load workspace files if needed

## Redis Implementation (from YouTube transcript)

### Setup Architecture:
```bash
# Redis for fast session state
redis-server --port 6379 --daemonize yes

# Qdrant for vector search (Docker)
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

### Memory Write Pattern:
```python
# Session state (Redis)
redis_client.hset(f"session:{session_id}", {
    "last_topic": topic,
    "message_count": count,
    "last_write_time": timestamp,
    "context_budget_used": tokens
})

# Long-term memory (Qdrant + file)
embedding = embed_text(content)
qdrant_client.upsert(collection_name="memories", 
    points=[{
        "id": generate_id(),
        "vector": embedding,
        "payload": {
            "content": content,
            "timestamp": timestamp,
            "source_file": "memory/2026-02-22.md",
            "instance": "[Prime]"
        }
    }])

# File write (append to daily log)
append_to_daily_log(date, timestamp, content)
```

### Memory Retrieval Pattern:
```python
# Semantic search first (Qdrant)
results = qdrant_client.search(
    collection_name="memories",
    query_vector=embed_query(query),
    limit=5
)

# Then exact file access for context
if results:
    for hit in results:
        file_content = read_file_lines(
            hit.payload["source_file"], 
            start_line=hit.payload.get("line_start"),
            count=5
        )
```

## Current Write Triggers (Implemented)

### Automatic Writes:
- **Heartbeat checks** (every 30 min) — if conversation happened since last write
- **Session end detection** — before "goodbye" or "done" responses
- **Task completion** — after running commands/verification
- **Decision logging** — when Jay makes choices

### Manual Write Triggers:
- 3+ message exchanges without a write
- New information learned (contacts, preferences, numbers)
- Files received/processed
- Major topic shifts in conversation

## Memory Consistency Rules

### Instance Coordination:
- Prime (Dell): GHL, leads, content machine, heavy processing
- Mobile (Vivobook): Research, quick lookups, coordination
- **Both tag writes:** `[Prime]` or `[Mobile]` in Supabase
- **Workspace files stay generic:** No instance stamps in `memory/*.md`

### Write Priorities:
1. **Daily logs** — Everything that happened
2. **ACTIVE-TASKS.md** — Current status updates
3. **MEMORY.md** — Only permanent fact changes
4. **Redis** — Session state for fast access
5. **Qdrant** — Semantic searchability

## Current Pain Points & Areas for Claude's Input

1. **Write timing:** Sometimes missing the "session end" trigger
2. **Memory retrieval confidence:** When to escalate from memory to full context loading
3. **Token budget enforcement:** Need hard stops to prevent context bloat
4. **Cross-instance coordination:** Ensuring both Prime and Mobile stay synchronized
5. **Memory consolidation:** When/how to compress old daily logs

## Implementation Status

### ✅ Working:
- Daily log writing during conversations
- Memory search + retrieval pipeline  
- Token conservation protocols
- Skills separation from brain files
- Redis + Qdrant vector storage
- Cross-instance memory sharing

### 🔄 Needs Refinement:
- Session end detection (currently manual trigger)
- Automatic memory consolidation (monthly?)
- Hard token budget enforcement
- Memory confidence scoring (when to load more context)

This is the current state. Jay has the Redis YouTube transcript and wants your suggestions on improving this architecture for safety, efficiency, and the ability to "switch to full brains/guns when needed."

What are your thoughts on optimizing this further?