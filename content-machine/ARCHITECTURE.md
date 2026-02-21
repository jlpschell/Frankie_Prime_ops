# 🏭 Content Machine — Architecture

## Mission
Automated AI news content pipeline for humanledai.net — scrape, process, create, distribute, QA.
**Niche:** AI news that affects businesses and individuals (not dev/research — real-world impact)

## Agent Squad (5 Sub-Agents, orchestrated by Frankie Prime)

```
                    ┌─────────────┐
                    │   FRANKIE   │
                    │ Orchestrator│
                    └──────┬──────┘
                           │
        ┌──────┬───────┬───┴───┬──────┐
        ▼      ▼       ▼       ▼      ▼
    ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
    │SCOUT ││MINER ││FORGE ││BLAST ││GUARD │
    │Scrape││Data  ││Write ││Post  ││QA    │
    └──────┘└──────┘└──────┘└──────┘└──────┘
```

### 🔍 SCOUT — The Scraper
**Job:** Find AI news from multiple sources daily
**Model:** Haiku (cheap, fast, pattern matching)
**Sources:**
- YouTube (AI channels: Matt Wolfe, AI Explained, Fireship, The AI Grip)
- Twitter/X (AI influencers, OpenAI, Anthropic, Google accounts)
- RSS feeds (TechCrunch AI, The Verge AI, Ars Technica, VentureBeat)
- Reddit (r/artificial, r/ChatGPT, r/LocalLLaMA)
- Google News (AI business impact queries)
**Output:** Raw feed items → `content-machine/inbox/YYYY-MM-DD-raw.json`
**Schedule:** Every 6 hours (4x daily)
**Cost target:** ~$0.10/run

### ⛏️ MINER — The Data Aggregator
**Job:** Deduplicate, rank by business relevance, extract key facts
**Model:** Haiku (classification + extraction)
**Input:** Scout's raw feed
**Process:**
1. Deduplicate across sources (same story from 5 outlets → 1 entry)
2. Score relevance (0-10): Does this affect a business owner or individual?
3. Extract: headline, summary, source, impact category, affected industries
4. Tag: #voice-ai, #automation, #regulation, #jobs, #tools, #funding
**Output:** Curated feed → `content-machine/curated/YYYY-MM-DD-curated.json`
**Schedule:** Runs after Scout completes
**Cost target:** ~$0.05/run

### 🔨 FORGE — The Content Writer
**Job:** Turn curated items into publishable content
**Model:** Sonnet (quality writing matters here)
**Input:** Miner's curated feed
**Output types:**
1. **Daily Briefing** — "AI News That Matters" (3-5 stories, 500 words)
2. **Deep Dive** — 1 story expanded (800-1200 words, business angle)
3. **Social Snippets** — 5-10 short-form posts (Twitter, LinkedIn, Instagram captions)
4. **Video Script** — 60-second news recap script (for Remotion/ElevenLabs)
**Output:** `content-machine/drafts/YYYY-MM-DD/` (separate files per type)
**Schedule:** Runs after Miner completes
**Cost target:** ~$0.30/run
**Voice:** Human Led AI brand — plain English, contractor-friendly, "here's why this matters to YOUR business"

### 📡 BLAST — The Distributor
**Job:** Format and stage content for each platform
**Model:** Haiku (templating, no creativity needed)
**Input:** Forge's drafts
**Platforms:**
1. humanledai.net blog (markdown → CMS-ready)
2. LinkedIn company page (professional tone)
3. Twitter/X (thread format)
4. Instagram (caption + image prompt for openai-image-gen)
5. Facebook Business (community tone)
6. YouTube Community tab (teaser for video)
**Output:** `content-machine/ready/YYYY-MM-DD/` (platform-specific files)
**Schedule:** Runs after Forge completes
**Cost target:** ~$0.05/run
**NOTE:** Does NOT auto-post. Stages content for review. Auto-posting is Phase 2.

### 🛡️ GUARD — The QA Agent
**Job:** Verify all content follows platform rules before distribution
**Model:** Haiku (checklist-based, fast)
**Checks:**
1. **Accuracy** — Claims match source material? No hallucinated stats?
2. **Attribution** — Sources credited? No plagiarism?
3. **Platform compliance:**
   - Twitter: <280 chars, no banned hashtags, proper @mentions
   - LinkedIn: Professional tone, no clickbait, proper formatting
   - Instagram: Caption length OK, hashtag count <30
   - Facebook: No engagement bait ("like if you agree"), community standards
   - Blog: SEO meta present, images have alt text, links work
4. **Brand voice** — Matches Human Led AI tone? No jargon?
5. **Legal** — No copyright issues, fair use for quotes, no defamation
**Output:** QA report + approved/flagged status → `content-machine/qa/YYYY-MM-DD-report.md`
**Schedule:** Runs after Blast completes
**Cost target:** ~$0.03/run

---

## Daily Pipeline Flow

```
5:00 AM  → SCOUT runs (scrape all sources)
5:15 AM  → MINER runs (dedupe, rank, extract)
5:30 AM  → FORGE runs (write all content types)  
6:00 AM  → BLAST runs (format for platforms)
6:15 AM  → GUARD runs (QA everything)
6:30 AM  → FRANKIE reviews QA report → flags issues or approves
7:00 AM  → Jay gets morning brief with content ready to post
```

**Total daily cost estimate: ~$0.53/day = ~$16/month**

---

## File Structure

```
content-machine/
├── ARCHITECTURE.md          ← this file
├── agents/
│   ├── SCOUT.md             ← scraper task definition
│   ├── MINER.md             ← aggregator task definition
│   ├── FORGE.md             ← writer task definition
│   ├── BLAST.md             ← distributor task definition
│   └── GUARD.md             ← QA task definition
├── config/
│   ├── sources.json         ← Scout's source list
│   ├── brand-voice.md       ← Forge's writing guidelines
│   └── platform-rules.md   ← Guard's compliance checklist
├── inbox/                   ← Scout's raw scrapes
├── curated/                 ← Miner's processed feed
├── drafts/                  ← Forge's written content
├── ready/                   ← Blast's platform-formatted content
└── qa/                      ← Guard's QA reports
```

---

## Limits & Guardrails
- Max 8 concurrent sub-agents (configured in openclaw.json)
- All agents use Haiku except Forge (Sonnet for quality)
- No auto-posting in Phase 1 — everything staged for Jay's approval
- No paid APIs for scraping — web_fetch + web_search + RSS only
- Content must ALWAYS tie back to "why this matters for businesses"
- Guard must pass before anything goes live

## Phase 2 (Future)
- Auto-posting via platform APIs (GHL social planner, Buffer, etc.)
- Video generation (Remotion + ElevenLabs from Forge's scripts)
- Engagement monitoring (track what performs, feed back to Forge)
- Newsletter automation (weekly digest email via GHL)
