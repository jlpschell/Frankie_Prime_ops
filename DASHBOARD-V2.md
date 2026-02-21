# Mission Control Dashboard V2 — Spec
# Author: Prime | Date: 2026-02-19
# For: VC to build | Approved by: Jay

## Philosophy
This is NOT a status page. This is Jay's **command console** for orchestrating two AI project managers.
Jay should be able to: see what's happening, pull levers, redirect priorities, and never be the middleman between us.

---

## Layout: Two Lanes + Shared

### Top Bar (keep current)
- Logo, clock, Jay online indicator
- ADD: Connection status indicators for both Bridge APIs (green/red dots)
- ADD: Quick stats row: "1,966 leads | A2P: Pending | Outscraper: Depleted | Supabase: Connected"

### Section 1: Agent Fleet (upgrade current)
Two cards side by side — but with REAL data:

**Prime Card (Professional/Business)**
- Status: pull from `PRIME_API/status` (WORKING NOW)
- Last activity: parse last `##` header from today's daily note
- Current task: first "In Progress" item from ACTIVE-TASKS.md
- Buttons: Command, Memory, Files, Config

**VC Card (Personal/Hobby)**
- Status: pull from `VC_API/status` (WORKING NOW)
- Same layout
- Buttons: Command, Memory, Files, Config

### Section 2: Command Center (upgrade current)
- Target selector: Prime | VC | Both
- Priority: Normal | Urgent | TAKE THE WHEEL
- Message textarea
- **NEW: Response panel** — after sending a command, show the agent's actual response
  - Poll the Bridge API or use the webhook relay response
  - Show a "waiting..." spinner then the response text
- **NEW: Quick commands** — preset buttons:
  - "Status report" | "Check leads" | "Check A2P" | "Run enrichment" | "Morning brief"

### Section 3: Two-Lane Task Board (REPLACE static tasks)
Split into two columns:

**Left: Business Lane (Prime)**
Pull from Prime's ACTIVE-TASKS.md via `PRIME_API/memory/tasks`
- Parse markdown into task cards
- Color by priority (P1=red, P2=yellow, P3=blue)
- Show status badges from the file
- Jay can click a task to send a command about it

**Right: Personal Lane (VC)**
Pull from VC's ACTIVE-TASKS.md via `VC_API/memory/tasks`
- Same format

### Section 4: Lead Pipeline Dashboard (NEW)
Prime-specific panel showing business metrics:
- **Total leads scraped:** count from lead CSV files (or hardcode from daily notes)
- **By niche:** bar chart or table (roofers: 187, plumbers: 137, etc.)
- **GHL loaded:** pull contact count from GHL API
  `GET /contacts/?locationId=tabcgomNBVaWpWAkIXL8&limit=1` — use `meta.total`
- **A2P Status:** prominent card
  - Status: PENDING / APPROVED / REJECTED
  - Submitted: Feb 18
  - Last checked: [timestamp]
  - "Check Now" button (sends command to Jay's Telegram or triggers browser check)
- **Outscraper credits:** status indicator (Depleted / Active)
- **Enrichment stats:** how many have phone, email, both

### Section 5: Memory Viewer (upgrade current)
- **Tab per agent** — not just VC's memory
  - Prime Today | Prime Tasks | Prime Core
  - VC Today | VC Tasks | VC Core
- Both pull from respective Bridge APIs
- Add search within memory content

### Section 6: Activity Log (REPLACE hardcoded)
- Real-time feed from BOTH agents
- Pull from both daily notes, parse `##` entries
- Color code: Prime=purple, VC=blue, Jay=yellow, System=gray
- Auto-refresh every 15 seconds
- Newest at top

### Section 7: API Health Dashboard (NEW)
Grid of service cards, each showing:
- Service name + icon
- Status: ✅ Connected | ⚠️ Degraded | ❌ Down | 🔑 Needs Key
- Last checked timestamp
- Who owns it (Prime/VC/Both)

Services to monitor:
| Service | Health Check Method |
|---------|-------------------|
| GHL | `GET /contacts/?limit=1` with API key |
| Supabase | `GET /rest/v1/` with anon key |
| ElevenLabs | `GET /v1/user` with API key |
| OpenAI | `GET /v1/models` with API key |
| Outscraper | Try a minimal query or check balance |
| Twilio | `GET /2010-04-01/Accounts/{sid}` |
| Prime Bridge | `GET /ping` |
| VC Bridge | `GET /ping` |
| GitHub | `GET /user` with PAT |
| Linear | TBD (VC setting up) |
| Typefully | TBD (VC setting up) |
| Notion | TBD (VC setting up) |

### Section 8: Config Panel (NEW)
For Jay to adjust settings without messaging us:
- Toggle emergency mode per agent
- Set priorities (drag to reorder tasks)
- Pause/resume heartbeats
- View/edit cron jobs
- Quick .env variable viewer (redacted values, show which are set)

### Section 9: Projects (upgrade current)
- Pull from a shared PROJECTS.md or both ACTIVE-TASKS.md files
- Real progress based on task completion, not hardcoded percentages
- Link each project to its lane (Business/Personal)

---

## Technical Requirements

### Bridge API Endpoints Needed (both agents already have these)
- `GET /ping` — health check
- `GET /status` — agent status + last entry
- `GET /memory/today` — today's daily note
- `GET /memory/tasks` — ACTIVE-TASKS.md
- `GET /memory/core` — MEMORY.md
- `GET /files` — workspace file list
- `GET /file?path=...` — read any workspace file
- `POST /command` — send instruction (now relays to OpenClaw on Prime)

### New Endpoints to Add (both Bridge APIs)
- `GET /memory/file?name=SHARED-API-INVENTORY.md` — shared config
- `GET /leads/summary` — lead count by niche (Prime only)
- `GET /health` — run all API health checks and return status grid
- `POST /config` — update agent config values

### API Keys for Dashboard
The dashboard JS needs these tokens (already in the current code):
```
PRIME_API = 'https://plotting.tail4c8a54.ts.net'
PRIME_TOKEN = '[REDACTED - see .env]'
VC_API = 'https://jasus-1.tail4c8a54.ts.net'
VC_TOKEN = 'frankieHQ_vc_2026_x9k2m'
```

### GHL API for Dashboard Lead Stats
```
GHL_API_KEY = '[REDACTED - see .env]'
GHL_LOCATION_ID = 'tabcgomNBVaWpWAkIXL8'
GHL_BASE_URL = 'https://services.leadconnectorhq.com'
```
NOTE: Call from Bridge API (server-side), not from browser JS (CORS + key exposure)

---

## Priority Build Order
1. Wire Prime commands (remove null check — Bridge API is live) — 5 min
2. Make tasks pull from ACTIVE-TASKS.md dynamically — 30 min
3. Make activity log real (parse daily notes) — 30 min
4. Add lead pipeline panel with GHL contact count — 1 hr
5. Add API health dashboard — 1 hr
6. Memory viewer for both agents — 30 min
7. Command response viewer — 1 hr
8. Config panel — 2 hr
9. A2P status card — 30 min
