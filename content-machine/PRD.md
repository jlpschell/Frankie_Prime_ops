# Product Requirements Document (PRD)
# Human Led AI — Autonomous Agent Operations Platform
**Version:** 1.0
**Date:** February 21, 2026
**Author:** Jay Schell (CEO) + Frankie Prime (COO/AI)
**Status:** Design Complete — Pre-Implementation

---

## 1. Executive Summary

Build a multi-agent autonomous operations platform that generates revenue through three parallel channels:
1. **Content Machine** — Daily AI news content for humanledai.net and social platforms
2. **Fiverr/Upwork Gig Fulfillment** — AI-powered service delivery for freelance gigs
3. **Auto-Prospecting** — Automated job discovery and proposal submission on freelance platforms

The platform runs on two physical machines (Dell 5810 + Vivobook) coordinated through Supabase, managed by an AI orchestrator (Frankie Prime), with a human CEO (Jay Schell) as final approver on all outbound deliverables.

---

## 2. Problem Statement

Jay Schell runs Human Led AI, an AI automation business targeting DFW contractors. Current challenges:
- **No consistent content pipeline** — social media and blog posts are manual and sporadic
- **No scalable service delivery** — Jay is the bottleneck for all client work
- **No passive lead generation** — no inbound content attracting prospects
- **Underutilized compute** — Dell 5810 workstation sits idle most hours of the day
- **Second machine (Vivobook) is disconnected** — no coordinated task delegation

**Goal:** Turn idle compute into a 24/7 revenue-generating operation with minimal human intervention.

---

## 3. Target Users

### Primary: Jay Schell (CEO)
- Reviews and approves all outbound content and deliverables
- Sets strategic direction
- Handles client communication on Fiverr/Upwork
- NOT a coder — all interfaces must be plain English

### Secondary: Frankie Prime (AI COO)
- Orchestrates all agents across both machines
- Manages task queue, scheduling, and quality control
- Reports to Jay via Telegram

### Tertiary: VC (AI Operations Manager)
- Executes delegated tasks from Prime
- Manages its own sub-agents on the Vivobook
- Reports to Prime (not directly to Jay unless escalated)

---

## 4. System Architecture

### 4.1 Hardware
| Machine | Role | Specs | Availability |
|---------|------|-------|-------------|
| Dell Precision 5810 | Primary — orchestration + heavy compute | Workstation-class, always-on | 24/7 |
| Vivobook (jasus-1) | Secondary — delegated tasks + mobile | Laptop, on when available | ~16h/day |

### 4.2 Software Stack
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent Runtime | OpenClaw | Agent orchestration, sub-agent spawning |
| Communication | Telegram | Jay ↔ Frankie interface |
| Database | Supabase (PostgreSQL) | Task queue, shared memory, vector storage |
| Networking | Tailscale | Machine-to-machine connectivity |
| Version Control | GitHub (PRIVATE repos) | Code and config storage |
| Content Delivery | humanledai.net | Blog and landing pages |
| Gig Platforms | Fiverr, Upwork | Revenue generation |

### 4.3 Org Hierarchy
```
JAY SCHELL (CEO)
├── FRANKIE PRIME (COO) — Dell 5810
│   ├── Content Machine Agents (5)
│   │   ├── SCOUT — scraper
│   │   ├── MINER — data aggregator
│   │   ├── FORGE — content writer
│   │   ├── BLAST — distributor/formatter
│   │   └── GUARD — QA/compliance
│   ├── Fiverr Gig Agents (6)
│   │   ├── SCRIBE — social media posts
│   │   ├── HUNTER — lead research
│   │   ├── BLOGGER — SEO blog posts
│   │   ├── INTEL — competitor analysis
│   │   ├── DIRECTOR — video scripts
│   │   └── PLANNER — content calendars
│   └── PROSPECTOR — auto-apply agent
└── VC (Operations Manager) — Vivobook
    ├── Research agents
    ├── Overflow gig workers
    └── Prospecting support agents
```

### 4.4 Concurrency Limits
| Machine | Max Concurrent Agents | Allocation |
|---------|----------------------|------------|
| Dell 5810 | 8 | 1 content chain + 6 Fiverr + 1 Frankie |
| Vivobook | 4-6 (TBD) | Delegated tasks from Prime |

---

## 5. Feature Requirements

### 5.1 Content Machine (PRIORITY 1)

#### 5.1.1 SCOUT — News Scraper
- **Sources:** YouTube transcripts (youtube-transcript-api), RSS feeds (TechCrunch, Verge, VentureBeat, Ars Technica, Wired), Reddit (r/artificial, r/ChatGPT), Google News (requires Brave Search API)
- **Schedule:** Every 6 hours (5 AM, 11 AM, 5 PM, 11 PM CST)
- **Output:** Raw JSON feed (10-50 items per run)
- **Model:** Haiku (~$0.10/run)
- **Dependencies:** youtube-transcript-api (installed), web_fetch (working), Brave Search API (NOT configured — need key)

#### 5.1.2 MINER — Data Aggregator
- **Input:** Scout's raw feed
- **Process:** Deduplicate, score relevance (0-10), categorize, extract key facts
- **Output:** Curated JSON (max 10 items, score 5+ only)
- **Model:** Haiku (~$0.05/run)
- **Scoring criteria:** Business impact on contractors/SMBs

#### 5.1.3 FORGE — Content Writer
- **Input:** Miner's curated feed
- **Output:** 4 content types per run:
  1. Daily Briefing (500 words, 3-5 stories)
  2. Deep Dive (800-1200 words, top story)
  3. Social Snippets (5-10 posts, multi-platform)
  4. Video Script (60-second recap, ~150 words)
- **Model:** Sonnet (~$0.30/run)
- **Voice:** Human Led AI brand — confident, approachable, zero jargon

#### 5.1.4 BLAST — Distributor
- **Input:** Forge's drafts
- **Output:** Platform-formatted files for: humanledai.net blog, LinkedIn, Twitter/X, Instagram, Facebook, YouTube Community
- **Includes:** SEO metadata, hashtags, image prompts, posting time recommendations
- **Model:** Haiku (~$0.05/run)
- **Phase 1:** Stage for manual posting. Phase 2: Auto-post via APIs.

#### 5.1.5 GUARD — QA Agent
- **Input:** All content from Blast
- **Checks:** Accuracy (sources cited), attribution (no plagiarism), platform compliance (char limits, banned hashtags), brand voice, legal (fair use, no defamation)
- **Output:** QA report with APPROVED / HOLD / REJECTED per piece
- **Model:** Haiku (~$0.03/run)

#### Content Machine Cost
- **Per run:** ~$0.53
- **Daily (1 run):** ~$0.53
- **Monthly:** ~$16

### 5.2 Fiverr/Upwork Gig Fulfillment (PRIORITY 2)

#### Available Gigs
| Gig | Agent | Model | AI Cost | Sell Price | Margin |
|-----|-------|-------|---------|-----------|--------|
| 30 social media posts | SCRIBE | Sonnet | $0.50 | $75-150 | 99% |
| 500 verified leads | HUNTER | Haiku | $0.30 | $100-200 | 99% |
| 10 SEO blog posts | BLOGGER | Sonnet | $1.00 | $150-300 | 99% |
| Competitor analysis | INTEL | Sonnet | $0.60 | $200-500 | 99% |
| 30 video scripts | DIRECTOR | Sonnet | $0.50 | $75-150 | 99% |
| 30-day content calendar | PLANNER | Haiku | $0.20 | $75-150 | 99% |

#### Fulfillment Flow
1. Jay receives order on Fiverr/Upwork
2. Jay sends brief to Frankie via Telegram
3. Frankie spawns appropriate agent with client brief
4. Agent produces deliverable
5. GUARD runs QA
6. Frankie packages and presents to Jay for review
7. Jay delivers to client

#### Revenue Projections (Conservative)
| Scenario | Gigs/Month | Avg Price | Monthly Revenue | AI Cost |
|----------|-----------|-----------|----------------|---------|
| Starting | 5 | $125 | $625 | $3 |
| Growing | 15 | $150 | $2,250 | $9 |
| Scaled | 30 | $175 | $5,250 | $18 |

### 5.3 Auto-Prospecting (PRIORITY 3)

#### PROSPECTOR Agent
- **Scans:** Upwork and Fiverr for jobs matching our capabilities
- **Filters:** Content writing, lead generation, SEO, social media, competitor research, video scripts
- **Scores:** Can we deliver? Is the pay worth it? (minimum $50/gig)
- **Writes:** Custom proposal tailored to each job posting
- **Phase 1:** Stages proposals for Jay's approval before submitting
- **Phase 2:** Auto-submits proposals (with spending limits)
- **Model:** Haiku for scanning, Sonnet for proposal writing
- **Schedule:** Every 2 hours during business hours

---

## 6. Supabase Task Queue Schema

### Table: `task_queue`
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| task_type | TEXT | content / fiverr / research / prospecting |
| assigned_to | TEXT | prime / vc |
| assigned_by | TEXT | jay / prime |
| status | TEXT | queued / in_progress / complete / failed / blocked |
| priority | INT | 1 (critical) to 5 (low) |
| title | TEXT | Short description |
| description | TEXT | Full task brief |
| agent | TEXT | Which agent handles this (SCOUT, SCRIBE, etc.) |
| input_data | JSONB | Client brief, config, parameters |
| output_path | TEXT | Where deliverable lives |
| result_summary | TEXT | What was produced |
| error_log | TEXT | If failed, why |
| created_at | TIMESTAMPTZ | When queued |
| started_at | TIMESTAMPTZ | When work began |
| completed_at | TIMESTAMPTZ | When finished |
| reviewed_by | TEXT | jay / prime / guard |
| review_status | TEXT | approved / rejected / revision_needed |

### Table: `agent_registry`
| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | Agent name (SCOUT, SCRIBE, etc.) |
| machine | TEXT | prime / vc |
| status | TEXT | idle / active / error |
| model | TEXT | haiku / sonnet / opus |
| last_run | TIMESTAMPTZ | Last execution time |
| total_runs | INT | Lifetime run count |
| total_cost | DECIMAL | Lifetime AI cost |
| success_rate | DECIMAL | % of successful runs |

### Rules
- Prime can write tasks for VC. VC cannot write tasks for Prime.
- Both machines read from same queue.
- No agent picks up a task already `in_progress` by another.
- Failed tasks auto-retry once, then alert Jay.
- All costs tracked per agent per run.

---

## 7. Communication Protocol

### Jay → Frankie (Telegram)
- "New Fiverr order: [brief]" → Frankie spawns agent
- "Run content pipeline" → Frankie triggers Scout chain
- "Status" → Frankie reports queue, active agents, costs

### Frankie → Jay (Telegram)
- Content ready for review → sends draft + QA report
- Fiverr deliverable ready → sends packaged output
- Prospector found good gigs → sends proposals for approval
- Errors/failures → immediate alert with diagnosis

### Frankie → VC (Supabase)
- Task delegation via task_queue table
- No direct messaging — database is the contract
- VC reads queue, picks up assigned tasks, writes results back

### VC → Frankie (Supabase)
- Task completion → updates status + result in task_queue
- Errors → writes to error_log column, Frankie monitors
- Never contacts Jay directly unless Prime is down

---

## 8. Security Requirements

- All GitHub repos PRIVATE (completed Feb 21)
- No API keys in code or markdown files — .env only
- .gitignore blocks all credential files (completed Feb 21)
- Supabase RLS enabled on all tables
- Task queue has row-level access (prime can read/write all, vc can only read/write own tasks)
- All Fiverr/Upwork credentials stored in .env, never in task descriptions
- Client data (briefs, deliverables) stored locally, not in Supabase
- Git history purged of all previously exposed keys (completed Feb 21)

---

## 9. Dependencies & Blockers

### Ready Now ✅
- youtube-transcript-api (Python, installed)
- RSS feed scraping (web_fetch, working)
- Reddit scraping (web_fetch on old.reddit.com)
- Content writing (Sonnet via OpenClaw)
- Lead generation scripts (outscraper, enrich, clean, consolidate)
- Obsidian vault (configured, syncing via OneDrive)
- Tailscale networking (Dell ↔ Vivobook connected)
- ffmpeg (installed for audio/video processing)
- Whisper transcription (OpenAI API, working)

### Need Configuration ⚠️
- Brave Search API key (free tier, 2K searches/month) — needed for SCOUT Google News + PROSPECTOR
- YouTube Data API key (free, 10K quota/day) — optional, transcript API works without it
- Fiverr account setup (Jay needs to create gig listings)
- Upwork account setup (Jay needs profile + connects)
- VC OpenClaw instance (needs reinstall/reconfigure on Vivobook)
- Supabase task_queue table (needs to be created)

### Future Enhancements 🔮
- Auto-posting APIs (GHL social planner, Buffer, or direct platform APIs)
- Remotion video generation from DIRECTOR scripts
- ElevenLabs voice generation from video scripts
- Newsletter automation (weekly digest via GHL email)
- Engagement monitoring (track post performance, feed back to FORGE)
- Client portal (dashboard for Fiverr clients to track progress)

---

## 10. Success Metrics

### Month 1 (Launch)
- [ ] Content machine running daily (auto, no intervention)
- [ ] 3+ Fiverr gigs listed and active
- [ ] First Fiverr revenue ($100+)
- [ ] humanledai.net blog has 30+ posts
- [ ] Social accounts posting 5x/week minimum

### Month 3 (Growth)
- [ ] 10+ Fiverr gigs fulfilled
- [ ] $1,000+ monthly Fiverr/Upwork revenue
- [ ] Content machine producing across all 6 platforms
- [ ] PROSPECTOR finding 5+ viable gigs/week
- [ ] VC handling 30%+ of task volume

### Month 6 (Scale)
- [ ] $3,000+/month from gig work
- [ ] Auto-posting live (Phase 2)
- [ ] Inbound leads from content (humanledai.net → GHL)
- [ ] 50+ blog posts indexed in Google
- [ ] Video content pipeline active (Remotion + ElevenLabs)

---

## 11. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|-----------|
| Fiverr/Upwork detects AI-generated content | Account ban | Medium | GUARD QA ensures quality. Human review before delivery. No copy-paste AI patterns. |
| Platform TOS changes blocking automation | Revenue loss | Low | Diversify across platforms. Build direct client relationships. |
| Content quality drops, damages brand | Reputation loss | Low | GUARD is mandatory. Jay reviews everything in Phase 1. |
| API costs spike unexpectedly | Budget overrun | Low | Haiku for most agents. Cost tracking per agent. Hard limits in config. |
| VC and Prime conflict on shared resources | Wasted compute | Medium | Supabase task queue is single source of truth. Clear hierarchy. No overlapping work. |
| Brave Search API rate limit hit | Scout degraded | Medium | RSS feeds work without it. Rotate queries. Cache results. |
| Client data leak | Legal liability | Low | Client data stays local. No Supabase storage of client briefs. .env for all keys. |
| Jay becomes bottleneck (approval queue) | Delivery delays | High | Phase 2 auto-approve for repeat clients. GUARD pre-clears routine content. |
| YouTube transcript API breaks | Scout degraded | Low | Fallback to web_fetch + browser automation. |
| Supabase downtime | Coordination loss | Low | Local memory files as fallback. Both machines can operate independently. |

---

## 12. Open Questions for Analysis

1. **Are we missing any high-margin Fiverr gig categories we could fulfill with existing tools?**
2. **Is the content machine schedule optimal (1x/day) or should we do 2x?**
3. **Should PROSPECTOR auto-apply immediately or always wait for Jay's approval?**
4. **What's the right split of work between Dell and Vivobook?**
5. **Are there platform compliance risks we haven't considered?**
6. **Should we build a client intake form/portal instead of manual Telegram briefs?**
7. **What's missing from the Supabase schema?**
8. **Are the revenue projections realistic or too conservative/aggressive?**
9. **What happens when we hit OpenClaw's 8-agent concurrency limit during peak load?**
10. **Should we add a MONITOR agent that tracks content performance and feeds data back?**

---

*This PRD is designed for external AI analysis. Feed it to Claude, GPT, or any reasoning model and ask: "What are we missing? Where are the blind spots? What would you change?"*
