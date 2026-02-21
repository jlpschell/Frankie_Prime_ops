# Mission Control V3 — War Room Spec
# Author: Prime | Date: 2026-02-19
# For: VC to build | Directed by: Jay Schell
# Replaces: DASHBOARD-V2.md (V2 endpoints still valid — V3 adds screens & upgrades)

---

## Philosophy
This is Jay's **war room**. Not a status page. Not a monitoring dashboard. A command console where Jay sees everything, directs everything, and nothing falls through the cracks.

Jay said it best: "I have so much going on. Seeing it keeps it real."

Every project has a PRD, goals, and clear steps to finish. Every piece of content has a pipeline. Every agent has a seat at the table. Jay is the overseer above all the worker bees.

---

## SCREEN 1: The Office (Home / Overview)

### Concept
Bird's-eye view of the entire operation. Think: looking down at a floor of worker bees from the overseer's office.

### Layout
- **Top bar**: Clock, Jay's avatar, connection status dots (Prime 🟢/🔴, VC 🟢/🔴), quick stats ribbon
- **Quick stats ribbon**: `Leads: 6,396 | GHL: 738 | A2P: Pending | Content Queue: 12 | Active Agents: 2`
- **Agent cards** (visual — like desks in an office):
  - Each agent shows: avatar/icon, name, current task, status (Working / Idle / Waiting / Error)
  - Pulse animation when actively processing
  - Click to jump to that agent's detail screen
- **Recent activity feed** (right sidebar): Last 10 actions across all agents, color-coded
  - Prime = 🟣 Purple | VC = 🔵 Blue | Jay = 🟡 Yellow | System = ⚪ Gray
- **Alert banner** at top for anything blocking (A2P pending, credits depleted, errors)

### Future: Sub-Agents
When sub-agents are added, they appear as additional desks in the office. New agent = new desk, auto-populated.

---

## SCREEN 1B: Live Operations Panel (ON THE OFFICE SCREEN)

### Concept
Three widgets embedded on the Office home screen so Jay never has to leave to see what matters most.

### Widget 1: Live Task Tracker (left side)
Real-time view of what each agent is doing RIGHT NOW and what's queued up next.

```
┌─ LIVE TASKS ─────────────────────────┐
│                                       │
│ 🟣 Prime — ACTIVE                    │
│ ▶ Writing Dashboard V3 spec          │
│   Started: 8:50 PM | Est: 15 min     │
│   Next up: Push to shared-brain repo  │
│                                       │
│ 🔵 VC — IDLE                         │
│ ▶ Last: Updated dashboard styles      │
│   Completed: 7:30 PM                  │
│   Next up: Pull shared-brain, read V3 │
│                                       │
│ ⏳ QUEUE                              │
│ 1. Enable memoryFlush config (Prime)  │
│ 2. Set heartbeat active hours (Prime) │
│ 3. Restructure memory/ folder (Prime) │
│ 4. Pull repo + read V3 spec (VC)     │
└───────────────────────────────────────┘
```

- Updates every 15 seconds via Bridge API
- Shows: current task, start time, estimated completion, what's next
- Queue pulls from ACTIVE-TASKS.md and PROJECTS.md steps
- Click any task to jump to its project card

### Widget 2: Goals & Milestones Board (center/right)
Message-board style. Each goal has a target date and completion percentage.

```
┌─ GOALS & MILESTONES ─────────────────────────┐
│                                                │
│ 🎯 Get Human Led AI VISIBLE        Due: Mar 1 │
│ ████████░░░░░░░░ 40%                          │
│ ✅ Brand kit done | ✅ Platform guides written  │
│ ⬜ Accounts created | ⬜ First post published   │
│                                                │
│ 🎯 10,000 Verified Leads in GHL    Due: Mar 15│
│ ███░░░░░░░░░░░░░ 20%                          │
│ ✅ 1,966 scraped | ✅ 738 in GHL               │
│ ⏳ A2P approval | ⬜ Outscraper top-up          │
│                                                │
│ 🎯 First SMS Campaign Sent         Due: TBD   │
│ █░░░░░░░░░░░░░░░ 5%  ⚠️ BLOCKED: A2P         │
│                                                │
│ 🎯 Dashboard V3 Live               Due: Mar 7 │
│ ██░░░░░░░░░░░░░░ 10%                          │
│ ✅ V3 spec written | ⬜ VC builds screens       │
│                                                │
│ 🎯 27 VM Demo Videos Published     Due: Mar 10│
│ ██████░░░░░░░░░░ 35%                          │
│ ✅ Scripts written | ⏳ Jay reviewing            │
│ ⬜ Audio rendered | ⬜ Videos assembled          │
└────────────────────────────────────────────────┘
```

- Progress bar auto-calculates from completed vs total steps
- Color: Green (on track), Yellow (at risk), Red (overdue/blocked)
- Due dates are editable — Jay clicks to change
- "Add Goal" button at bottom
- Completed goals move to a "🏆 Done" archive

### Widget 3: Recording Feed (bottom-right corner)
Small, always-visible feed showing what's being written to memory RIGHT NOW. Jay can see the agents' brains working in real-time.

```
┌─ 📝 RECORDING... ──────────────┐
│                                  │
│ 9:01 PM 🟣 Prime                │
│ → memory/2026-02-19.md           │
│ "Dashboard V3 spec written,      │
│  pushed to shared-brain"         │
│                                  │
│ 8:46 PM 🟣 Prime                │
│ → memory/2026-02-19.md           │
│ "Jay sent dashboard article,     │
│  discussing upgrade vision"      │
│                                  │
│ 7:30 PM 🔵 VC                   │
│ → ACTIVE-TASKS.md                │
│ "Updated dashboard task status"  │
│                                  │
│ [View All →]                     │
└──────────────────────────────────┘
```

- Shows last 5 memory writes across all agents
- Each entry: timestamp, agent, file path, snippet of what was written
- Subtle fade-in animation when new entries appear
- Click "View All" → jumps to Memory Viewer screen
- Click any entry → opens that file in Memory Viewer at that line
- **This is Jay's proof we're actually logging.** No more "did you write that down?" — he can SEE it happening.

### Widget 4: "Hey You" Quick Command Bar (persistent — always visible, every screen)

A dropdown + message box that lives in the top bar on EVERY screen. Jay can bark an order to any agent at any time without navigating anywhere.

```
┌──────────────────────────────────────────────────────────┐
│ 🎯 [▼ Prime     ] │ Type a command...              [Send]│
│    ├─ Prime                                               │
│    ├─ VC                                                  │
│    ├─ All Agents                                          │
│    ├─ Content Agent (future)                              │
│    └─ Lead Gen Agent (future)                             │
└──────────────────────────────────────────────────────────┘
```

**Behavior:**
- Dropdown lists ALL active agents — current and future. New agents auto-appear when added.
- "All Agents" broadcasts to everyone simultaneously
- Type a message, hit Send (or Enter) → routes to that agent instantly
- Response appears in a slide-out panel below the bar (doesn't navigate away from current screen)
- Response panel shows agent avatar, typing indicator, then the reply
- Panel auto-collapses after 30 seconds of inactivity, or Jay can pin it open
- **Keyboard shortcut**: `/` focuses the command bar from anywhere (like Slack)
- History: Click the dropdown arrow on the response panel → see last 10 commands sent

**Response Panel:**
```
┌──────────────────────────────────────────────────────┐
│ 🟣 Prime is typing...                                │
│                                                      │
│ 🟣 Prime (9:12 PM):                                 │
│ "V3 spec updated with your feedback. Pushed to repo. │
│  Want me to message VC to start building?"           │
│                                                      │
│                          [Reply] [Jump to Round Table]│
└──────────────────────────────────────────────────────┘
```

**Data Flow:**
- Send → Bridge API `POST /command` → OpenClaw webhook relay → agent processes
- Response streams back via Bridge API polling or Supabase Realtime subscription
- All commands logged to `agent_messages` Supabase table (visible in Round Table history)
- Jay's commands also appear in the Recording Feed so the "wiretap" stays complete

---

## SCREEN 2: Projects Board

### Concept
Every project Jay has going — past, present, and planned — in one place. Nothing gets lost. Each project is a **living card** with three things always visible:

1. **PRD** (1-liner): What is this project and why does it exist?
2. **Goals** (2-3 bullets): What does "done" look like?
3. **Steps to Finish** (accurate, numbered): What's left, who owns each step?

### Layout
Three columns (Kanban):
- **On Deck** — planned but not started
- **In Progress** — actively being worked
- **Waiting For...** — blocked, with a clear label of WHAT it's waiting for

### Project Card Structure
```
┌─────────────────────────────────────┐
│ 🔴 P1  Lead Generation Pipeline    │
│                                     │
│ PRD: Scrape DFW contractors, enrich │
│ with phone/email, load into GHL     │
│ for outbound campaigns.             │
│                                     │
│ Goals:                              │
│ • 10,000 verified leads in GHL      │
│ • A2P approved for SMS outreach     │
│ • First campaign sent               │
│                                     │
│ Steps to Finish:                    │
│ 1. ✅ Scrape 19 niches (1,966 done) │
│ 2. ⏳ Top up Outscraper credits     │
│    → Owner: Jay | Waiting: Purchase │
│ 3. ⏳ A2P campaign approval         │
│    → Owner: Carrier | Waiting: Rev. │
│ 4. ⬜ Enrich remaining leads        │
│    → Owner: Prime                   │
│ 5. ⬜ Upload to GHL                 │
│    → Owner: Prime                   │
│ 6. ⬜ Launch first SMS campaign     │
│    → Owner: Prime (after A2P)       │
│                                     │
│ Lane: Business | Agent: Prime       │
│ Last updated: Feb 19, 8:46 PM       │
└─────────────────────────────────────┘
```

### Step Status Icons
- ✅ Done
- ⏳ In progress / waiting
- ⬜ Not started
- 🚫 Blocked (with reason)

### Projects to Pre-Populate

**In Progress:**
| Project | PRD | Goals | Lane |
|---------|-----|-------|------|
| Lead Gen Pipeline | Scrape, enrich, load DFW contractor leads | 10K leads, A2P approved, first campaign | Business/Prime |
| VM Scripts & Audio | Create voice-AI demo videos for outreach | 27 scripts reviewed, audio rendered, videos published | Business/Prime |
| Brand & Platform Launch | Establish Human Led AI on all major platforms | 6 platforms live, consistent branding, posting schedule | Business/Prime |
| Dashboard V3 | Build Mission Control war room | All 7 screens functional, both agents connected | Shared/VC |
| Agent Sync | Connect Prime + VC via shared brain | Git sync working, Supabase writes tagged, round table live | Shared/Both |

**On Deck:**
| Project | PRD | Goals | Lane |
|---------|-----|-------|------|
| Remotion Marketing Videos | Audiogram-style demos of AI handling calls | 3 videos published, reduce AI "scariness factor" | Business/Prime |
| Email Automation | Manage Jay's inbox, unsub bloat, route important mail | Auto-classify, protected senders respected, weekly digest | Business/Prime |
| $497 Lead Bundle | Package enriched leads for direct sale to contractors | Bundle template, pricing page, first sale | Business/Prime |

**Waiting For:**
| Project | Waiting For What |
|---------|-----------------|
| A2P SMS Campaign | Carrier approval (submitted Feb 18) |
| Lead Gen Round 4+ | Outscraper credit top-up (Jay) |
| VM Audio Rendering | Jay's script review → then ElevenLabs render |

### Data Source
- Pull from a new `PROJECTS.md` file in workspace (Prime maintains it)
- Each project is a markdown section with structured fields
- Bridge API endpoint: `GET /projects` — returns parsed JSON
- Jay can reorder, change status, or add notes from the dashboard → `POST /projects/update`

---

## SCREEN 3: Content Pipeline

### Concept
Every piece of content — from idea to published — tracked across ALL platforms. Whether Jay has an account yet or not. Sub-agents can be assigned to content creation 24/7.

### Platform Columns (always visible, whether active or not)

| Platform | Account Status | Handle/URL |
|----------|---------------|------------|
| **Facebook** | ✅ Active | humanledai |
| **YouTube** | ⬜ Needs Setup | humanledai@gmail.com |
| **LinkedIn** | ⬜ Needs Setup | — |
| **Instagram** | ⬜ Needs Setup | — |
| **TikTok** | ⬜ Needs Setup | — |
| **Threads** | ⬜ Needs Setup | — |
| **Substack** | ⬜ Needs Setup | — |
| **X (Twitter)** | ⬜ Needs Setup | — |
| **Google Business Profile** | ⬜ Needs Setup | — |
| **Reddit** | ⬜ Needs Setup | — |
| **Pinterest** | ⬜ Needs Setup | — |
| **Nextdoor** | ⬜ Needs Setup | — |

### Pipeline Stages (per content piece)
```
💡 Idea → 📝 Script → 🎨 Design → 🎬 Produce → ✅ Review → 📤 Schedule → ✅ Published
```

### Content Card
```
┌──────────────────────────────────────┐
│ "AI Answers Your Phones While You    │
│  Swing Hammers" — Short Video        │
│                                      │
│ Stage: 📝 Script                     │
│ Platforms: TikTok, Instagram Reels,  │
│           YouTube Shorts, Facebook   │
│ Assigned: Prime (script) → VC (post) │
│ Due: Feb 22                          │
│ Notes: Use Eric voice, roofer niche  │
└──────────────────────────────────────┘
```

### Features
- **Multi-platform posting**: One piece of content → checkboxes for which platforms to push to
- **Platform setup wizard**: Click a ⬜ platform → get step-by-step guide (we already wrote these in `content/platform-guides/`)
- **Content calendar**: Drag content cards to calendar dates
- **Sub-agent assignment**: Assign a sub-agent to handle a content type 24/7 (e.g., "Social Media Agent" writes daily posts)
- **Repurpose tracker**: Shows how one piece of content was sliced across platforms
- **Analytics** (future): Pull engagement metrics per platform

### "Others" Section
Expandable section below the main platforms for niche/future platforms:
- Yelp, Angi, HomeAdvisor, Thumbtack, BBB (contractor-specific directories)
- Medium, Dev.to (thought leadership)
- Podcast platforms (if Jay goes that route)

### Data Source
- New `CONTENT-PIPELINE.md` or Supabase table
- Bridge API endpoint: `GET /content/pipeline` — returns all content items with stages
- `POST /content/create` — add new content idea
- `POST /content/update` — move through stages

---

## SCREEN 4: The Round Table (Team / Comms)

### Concept
This is where Jay, Prime, VC, and all future agents sit at the same table. Jay can talk to anyone. Agents can talk to each other. Jay can tell them to stop horsing around and get to work. 😂

### Layout
- **Visual**: Round table in the center, seats for each participant
  - Jay (gold crown icon) — always at the head
  - Prime (purple icon) — business seat
  - VC (blue icon) — personal seat
  - Future agents get added seats automatically
- **Status indicators** on each seat:
  - 🟢 Online & active
  - 🟡 Idle
  - 🔴 Offline/Error
  - 💬 Currently responding

### Communication Panel (below the table)
- **To**: Dropdown → Prime | VC | All | [future agents]
- **Message box**: Type a command or message
- **Response area**: Shows the agent's reply in real-time
- **Thread view**: Toggle to see conversation history with each agent

### Agent-to-Agent Chat
- Prime and VC can message each other (via `sessions_send` / shared-brain)
- Jay can see ALL agent-to-agent messages in a "wiretap" feed
- Jay can jump into any conversation: "Hey, stop that. Focus on X."

### Quick Commands (buttons below table)
- "Status report — ALL" → both agents respond
- "What are you working on?" → current task from each
- "Priority override: [task]" → both agents ACK and reprioritize
- "Stand down" → pause non-critical work
- "Get to work!" → resume 😄

### Data Flow
- Messages route through Bridge APIs → OpenClaw webhook relay
- Agent-to-agent uses `sessions_send` or git-based shared-brain
- All messages logged to daily notes (both sides)

---

## SCREEN 5: Memory Viewer & Manager

### Concept
See everything your agents know. Search it. Edit it. Watch it grow in real-time. No more "it's buried in a .md file somewhere."

### Layout — Three Panels

**Left Panel: File Tree**
- Shows full memory structure for each agent:
  ```
  Prime/
  ├── MEMORY.md (core facts)
  ├── ACTIVE-TASKS.md
  ├── PROJECTS.md
  ├── memory/
  │   ├── 2026-02-19.md
  │   ├── 2026-02-18.md
  │   └── ...
  ├── TOOLS.md
  └── SOUL.md
  
  VC/
  ├── MEMORY.md
  ├── ...
  
  Shared/
  ├── SHARED-API-INVENTORY.md
  ├── SYNC-README.md
  └── ...
  ```
- Click any file to view in the center panel
- 🟢 dot on files modified today
- 🔴 dot on files not updated in 7+ days (stale warning)

**Center Panel: File Viewer/Editor**
- Rendered markdown view (default)
- Toggle to raw edit mode
- Syntax highlighting
- Save → pushes update via Bridge API → agent picks up changes

**Right Panel: Activity Stream**
- Real-time feed of memory changes:
  - "Prime wrote to memory/2026-02-19.md — '## 8:46 PM — Dashboard Upgrade Discussion'"
  - "VC updated ACTIVE-TASKS.md — marked 'Dashboard rebuild' as In Progress"
  - "Shared brain synced — 3 files updated"
- Filter by: Agent | File | Date range

### Search
- Top search bar searches ALL memory files across ALL agents
- Results show: file, line, snippet, agent, date
- Powered by: `memory_search` via Bridge API or direct Supabase vector search

### Memory Health Dashboard
- **Coverage**: How many days have logs? Any gaps?
- **Freshness**: When was each file last updated?
- **Completeness**: Does MEMORY.md have all key sections? Are daily notes following the template?
- **Gaps alert**: "⚠️ No daily note for Feb 17 — Prime may have missed logging"

### Data Source
- Bridge API endpoints: `GET /memory/tree`, `GET /memory/file?path=...`, `POST /memory/write`
- Supabase for vector search
- File modification timestamps for activity stream

---

## SCREEN 6: Calendar & Schedule

### Concept
See everything that's scheduled — cron jobs, follow-ups, content due dates, deadlines, heartbeats.

### Views
- **Month** | **Week** | **Day** toggle
- Color-coded by type:
  - 🟣 Prime tasks/deadlines
  - 🔵 VC tasks/deadlines
  - 🟢 Content due dates
  - 🔴 Blockers/deadlines
  - ⚪ System (heartbeats, crons)

### Auto-Populated Events
- Heartbeats (every 30 min during active hours)
- A2P daily check (9 AM)
- Morning brief (5:30 AM)
- Nightly wrapup (9:30 PM)
- Content due dates from Content Pipeline
- Project step deadlines from Projects Board

### Manual Events
- Jay can add events/reminders from the dashboard
- Assign to an agent: "Prime, follow up on Outscraper credits Feb 21"

---

## SCREEN 7: API Health & System Status

### Concept
Grid of every service both agents depend on. At a glance: what's up, what's down, who owns it.

### Service Grid (from V2, expanded)
| Service | Owner | Health Check | Status |
|---------|-------|-------------|--------|
| GHL API | Prime | `GET /contacts/?limit=1` | ✅/❌ |
| Supabase | Both | `GET /rest/v1/` | ✅/❌ |
| ElevenLabs | Prime | `GET /v1/user` | ✅/❌ |
| OpenAI | Both | `GET /v1/models` | ✅/❌ |
| Outscraper | Prime | Balance check | ✅/⚠️ Depleted |
| Twilio | Prime | Account check | ✅/❌ |
| Prime Bridge | Prime | `GET /ping` | ✅/❌ |
| VC Bridge | VC | `GET /ping` | ✅/❌ |
| GitHub | Both | `GET /user` | ✅/❌ |
| OpenClaw (Prime) | Prime | Gateway status | ✅/❌ |
| OpenClaw (VC) | VC | Gateway status | ✅/❌ |

### Alert Rules
- Any service ❌ → banner alert on all screens
- Service ⚠️ for 24+ hours → escalate to Jay
- Auto-retry failed checks every 5 minutes

---

## NAVIGATION

### Sidebar (always visible)
```
🏢 Office (Home)
📋 Projects
📱 Content Pipeline
🪑 Round Table
🧠 Memory
📅 Calendar
⚡ System Health
⚙️ Settings
```

### Settings Screen
- Agent config (heartbeat intervals, active hours)
- API key management (add/rotate keys)
- Notification preferences
- Theme (dark/light — default dark)
- User profile (Jay's info)

---

## TECH STACK

### Recommended
- **Frontend**: Next.js 14+ (App Router) + Tailwind CSS + shadcn/ui
- **Real-time**: Convex (as article suggests) OR Supabase Realtime (we already have Supabase)
- **Backend**: Bridge APIs (already running on both machines)
- **Hosting**: Netlify (current) or Vercel
- **Auth**: Simple token auth (Jay is only user)

### Recommendation: Use Supabase Realtime
We already have Supabase. Rather than adding Convex as a new dependency:
- Use Supabase tables for projects, content pipeline, calendar events
- Use Supabase Realtime subscriptions for live updates
- Use existing vector store for memory search
- Bridge APIs remain the data layer for agent-specific file access

### New Supabase Tables Needed
```sql
-- Projects
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  prd TEXT,
  goals JSONB, -- ["goal1", "goal2"]
  steps JSONB, -- [{step, owner, status, waiting_for}]
  status TEXT DEFAULT 'on_deck', -- on_deck, in_progress, waiting, done
  waiting_for TEXT,
  lane TEXT, -- business, personal, shared
  agent TEXT, -- prime, vc, both
  priority INT DEFAULT 3,
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Content Pipeline
CREATE TABLE content_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  type TEXT, -- video, post, article, reel, thread
  stage TEXT DEFAULT 'idea', -- idea, script, design, produce, review, schedule, published
  platforms JSONB, -- ["tiktok", "instagram", "youtube"]
  assigned_to TEXT,
  due_date DATE,
  notes TEXT,
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Platform Accounts
CREATE TABLE platforms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  status TEXT DEFAULT 'not_setup', -- active, needs_setup, not_setup
  handle TEXT,
  url TEXT,
  setup_guide_path TEXT
);

-- Calendar Events
CREATE TABLE calendar_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  type TEXT, -- task, content, system, reminder
  agent TEXT,
  start_time TIMESTAMPTZ,
  end_time TIMESTAMPTZ,
  recurring BOOLEAN DEFAULT false,
  recurrence_rule TEXT,
  color TEXT
);

-- Agent Messages (Round Table)
CREATE TABLE agent_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  from_agent TEXT NOT NULL, -- jay, prime, vc
  to_agent TEXT NOT NULL,
  message TEXT NOT NULL,
  response TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

---

## BRIDGE API — NEW ENDPOINTS NEEDED

### Both Agents
```
GET  /projects              → list all projects (parsed from PROJECTS.md or Supabase)
POST /projects/update       → update project status/steps
GET  /content/pipeline      → list content items
POST /content/create        → add content item
POST /content/update        → move content through stages
GET  /memory/tree           → file tree of workspace
GET  /memory/search?q=...   → search memories
POST /roundtable/message    → send message to this agent
GET  /roundtable/history    → get conversation history
GET  /calendar/events       → list events
POST /calendar/event        → create event
```

### Existing Endpoints (from V2 — still valid)
```
GET  /ping
GET  /status
GET  /memory/today
GET  /memory/tasks
GET  /memory/core
GET  /memory/file?name=...
GET  /files
GET  /file?path=...
POST /command
GET  /leads/summary
GET  /ghl/contacts/count
GET  /health
GET  /shared-inventory
GET  /dashboard-spec
```

---

## BUILD PRIORITY ORDER

### Phase 1: Foundation (Week 1)
1. **Office screen** — agent cards, status indicators, activity feed
2. **Projects Board** — Kanban with PRD/goals/steps structure
3. **Round Table** — basic messaging between Jay ↔ agents
4. **Navigation** — sidebar with all screens

### Phase 2: Content & Memory (Week 2)
5. **Content Pipeline** — all platforms, stages, cards
6. **Memory Viewer** — file tree, viewer, activity stream
7. **Calendar** — month/week/day views, auto-populated events

### Phase 3: Polish & Power (Week 3)
8. **System Health** — service grid, auto-checks, alerts
9. **Agent-to-agent chat** in Round Table
10. **Memory search** integration
11. **Settings** screen
12. **Sub-agent support** — new desks in office, new seats at table

---

## DESIGN DIRECTION

### Vibe
- **Dark mode default** (Jay's preference implied by "overseer" and "war room" language)
- Clean, modern, information-dense but not cluttered
- Human Led AI branding: Deep Navy `#1A2E5A` / Electric Blue `#2563EB` / Amber `#F59E0B`
- Montserrat Bold for headers, Open Sans for body
- Subtle animations (pulse for active agents, slide for transitions)
- No unnecessary chrome — every pixel earns its place

### Inspiration
- Linear (clean task management)
- Grafana (dense monitoring)
- Discord (team communication feel for Round Table)
- Notion (memory viewer layout)

---

## WHAT JAY SAID (direct quotes, for VC to understand the vision)

> "I want a projects screen that shows what is on deck, waiting for... and what unfinished tasks need what. Each project needs a PRD, goals, and accurate steps to finish. This way I don't lose what's been started."

> "I have so much going on. Seeing it keeps it real."

> "Content pipeline should have ALL the socials, whether I have an account yet or not — Substack, Facebook, YouTube, TikTok, Threads, Instagram — and a list of others. This can have sub-agents devoted to it 24/7."

> "Memory viewer and manager — I can see what is being shared, added to, updated."

> "Team screen needs to be where you and I and all other future versions connect and can have a round table. You can talk to VC, and vice versa, and I can say stop horsing around and get to work."

> "Office view is good. Like an overseer above all the worker bees."

---

*This spec supersedes DASHBOARD-V2.md. V2 endpoint definitions remain valid. V3 adds screens, Supabase tables, and the war room vision.*
