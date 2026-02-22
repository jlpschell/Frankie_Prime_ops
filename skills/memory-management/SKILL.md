# Memory Management Skill

## Session Memory Protocol

### On Session Start:
1. Read most recent `memory/YYYY-MM-DD.md`
2. Read `MEMORY.md` for core facts
3. Read `ACTIVE-TASKS.md` for current work
4. Create today's daily note if missing

### During Conversations (>2 exchanges):
Write to `memory/YYYY-MM-DD.md`:
- Timestamp + topic
- Actions taken (with specifics)
- Decisions made
- Pending items

### Memory Retrieval Protocol:
1. **ALWAYS** run `memory_search` first
2. Use `memory_get` for exact lines
3. Cross-reference ACTIVE-TASKS.md and MEMORY.md
4. **NEVER** say "I don't recall" without searching

### Write Triggers:
- Jay assigns task
- Action completed
- Decision made
- New information learned
- 3+ message exchanges
- Before session ends

### File Purposes:
- `memory/YYYY-MM-DD.md` — Daily events
- `MEMORY.md` — Permanent facts  
- `ACTIVE-TASKS.md` — Current task status