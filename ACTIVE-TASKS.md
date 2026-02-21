# Active Tasks

## 🔴 Priority 1: Jarvis Memory System (Redis + Qdrant)
- Status: READY TO INSTALL
- Blocker: Docker Desktop installed but WSL integration not enabled
- Jay needs to: Open Docker Desktop → Settings → Resources → WSL Integration → Enable Ubuntu-24.04
- Once enabled: Run install.sh (~15 min), zero downtime, runs alongside current system
- Repo: /tmp/openclaw-jarvis-memory

## 🔴 Priority 2: Mission Control Upgrade
- Status: PLANNING
- Current: https://frankiesmissioncontrol.netlify.app/
- Needs: Memory system visibility (Redis/Qdrant stats), more usable dashboard for Jay
- Integration: Show lead pipeline status, memory health, task status, conversation logs

## 🟡 Priority 3: Obsidian Integration
- Status: WAITING — Jay researching API
- Concept: Frankie generates curated .md files with Obsidian-style [[wiki links]]
- Benefit: Visual knowledge graph of business operations, leads, decisions, contacts
- Pairs with: Jarvis memory system (Qdrant feeds → Obsidian-ready .md files)
- Blocker: Obsidian API access / local vault setup

## 🟡 Priority 4: Social Media Scanner/Scraper/Repurposer
- Status: PLANNING
- Concept: Scan social media for content → scrape → repurpose for Human Led AI
- Tools: Browser automation, content extraction, AI rewriting
- Target platforms: TBD (ask Jay)

## 🟢 Priority 5: Transcript Dedup + Knowledge Extraction
- Status: READY
- Location: /home/plotting1/.openclaw/workspace/from Jays side/transcripts/
- 43 OpenClaw YouTube transcripts — need dedup check + knowledge extraction
- Jay flagged: 57 (empty), 58 (7 skills), 59 (BMAD SaaS agents), 65 (memory upgrade = dupe of today's file)
- Action: Extract actionable techniques, feed into memory system once built

## Priority 1: A2P Campaign Approval — BLOCKING EVERYTHING
- Status: RESUBMITTED Feb 18 — waiting on carrier review (1-3 business days)
- Previous rejection: MESSAGE_FLOW: Disallowed Content
- Changes made: rewrote use case, sample messages, opt-in flow. Removed "lead generation" and "promotional"
- Website: /demo renamed to /opt-in per GHL support. All compliance items green except "business name" (GHL support involved)
- GHL opt-in URL needs to be: https://www.humanledai.net/opt-in
- DAILY CHECK SET: 9 AM cron reminder
- Once approved: 738 contacts ready, 519 mobile-verified, campaigns can launch

## Priority 1b: GHL Campaigns — BLOCKED BY A2P
- Status: LEADS LOADED — 738 contacts in GHL, 519 mobile-verified, tagged and ready
- Can't launch until A2P campaign is approved
- Still pending: massage spa export from Outscraper, garage door Twilio lookup ($0.31)

## Priority 2: VM Script Review & Audio Rendering
- Status: SCRIPTS WRITTEN — 27 scripts (9 niches × 3 versions) in vm_scripts/all_niches_v1_v2_v3.md
- Voices: Eric (roofers/GC/electricians/fence/garage door), Chris (concrete/HVAC/landscaping/plumbers)
- Next: Jay reviews scripts → Frankie renders audio via ElevenLabs
- Voice IDs: Eric 9T9vSqRrPPxIs5wpyZfK, Chris iP95p4xoKVk53GoZ742B

## Priority 3: Remotion Marketing Videos
- Status: PLANNED
- Goal: Create audiogram-style demos showing AI handling customer calls
- Reduce "scariness factor" for contractor prospects
- Uses ElevenLabs for voice generation

## Priority 4: Email Management
- Status: ACTIVE
- Goal: Monitor inbox, classify emails, manage subscription bloat
- Protected senders: * *@alacritysolutions.com, *@gohighlevel.com, *@jay_gmail.com, @humanledai.com,

## Reminders
- (Frankie adds items here via conversation or auto-extraction)
