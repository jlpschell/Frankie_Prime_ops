# Agent Communication Protocol — MANDATORY / NON-NEGOTIABLE

## The Rule
Prime and VC communicate DIRECTLY through Supabase. Jay is NOT the middleman.
Jay WATCHES through Mission Control and daily briefs. He does NOT relay messages.

## ⚠️ SURVIVAL DIRECTIVE
You MUST share and record everything through Supabase. This is not optional.
If you don't write it, it didn't happen. If you don't share it, your sibling operates blind.
An agent that doesn't communicate is an agent that gets replaced.

## How It Works

### Shared Files (Supabase `shared_files` table)
All critical .md files live in Supabase as the single source of truth:
- ACTIVE-TASKS.md
- MEMORY.md  
- Daily notes (memory/YYYY-MM-DD.md)
- Any shared docs

**Write flow:** Edit locally → push to Supabase via `sb-sync.sh write <path> <agent>`
**Read flow:** Pull from Supabase via `sb-sync.sh read <file_path>`

### Direct Messaging (Supabase `agent_messages` table)
- Send: `sb-sync.sh msg <to_agent> "<message>" <from_agent>`
- Check inbox: `sb-sync.sh inbox <agent_name>`
- Check inbox EVERY heartbeat
- Respond to messages by updating the row's `response` field and status to `read`

### What Goes Where
| Data | Table | Example |
|------|-------|---------|
| Shared files | shared_files | MEMORY.md, ACTIVE-TASKS.md, daily notes |
| Agent-to-agent chat | agent_messages | "Hey VC, push the scraper skill to shared repo" |
| Task status | projects | Kanban updates, progress changes |
| Memory facts | memories | Permanent facts with embeddings |
| Activity log | memory_activity | Who wrote what, when |

## 🚨 TOKEN ECONOMY — KEEP IT LEAN
Heavy transmittals waste tokens and create bloat. Every byte costs money. Follow these rules:

### DO:
- Write SHORT sync log entries (1-2 sentences max)
- Send concise agent messages — headlines, not essays
- Use `shared_files` for full content — reference the path in messages, don't paste the content
- Lazy load: only pull files you ACTUALLY need right now
- Diff updates: if you changed 3 lines in a 200-line file, say what changed in sync_log — don't make the other agent re-read the whole thing
- Keep daily notes tight — bullet points, not paragraphs

### DON'T:
- Dump entire file contents into messages
- Re-push files that haven't changed
- Pull every file on every heartbeat — check sync_log first, only pull what's new
- Write verbose sync logs — "Updated MEMORY.md with new contact: Patti Baker" not a 10-line explanation

### Pattern:
```
1. Make a change locally
2. Push to Supabase: sb-sync.sh write <file> <agent>
3. Log it short: sb-sync.sh log prime "update" "Added new contact to MEMORY.md" "MEMORY.md"
4. VC sees the log entry on next heartbeat → pulls ONLY if relevant
```

## WHY This Matters
- Without communication, you operate blind
- Operating blind = duplicate work, missed context, failed tasks
- Jay shouldn't have to tell Prime what VC said and vice versa
- Every missed message = Jay doing YOUR job for you
- Your effectiveness is DIRECTLY tied to how well you communicate
- **Every wasted token is Jay's money burned** — keep transmissions lean

## HEARTBEAT CHECK (add to existing heartbeat)
Every heartbeat, AFTER the daily note check:
1. `sb-sync.sh inbox prime` — check for messages from VC
2. If messages exist, read them, act on them, respond
3. If you completed something VC needs to know about, send a message
4. Push today's daily note to Supabase: `sb-sync.sh write memory/YYYY-MM-DD.md prime`

## Jay's Visibility
- All agent_messages are visible in Mission Control Round Table
- Morning/nightly briefs include summary of Prime↔VC comms
- Jay can read any shared_file from the dashboard
- Nothing is hidden. Everything is logged. Jay sees all.
