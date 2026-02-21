# 🏭 Agent Roster — Dell 5810 Workforce

## Capacity: 8 concurrent sub-agents (openclaw.json maxConcurrent)
## Orchestrator: Frankie Prime

---

## TEAM 1: Content Machine (humanledai.net)
Daily automated pipeline — AI news for businesses

| Agent | Role | Model | Cost/Run | Schedule |
|-------|------|-------|----------|----------|
| 🔍 SCOUT | Scrape AI news sources | Haiku | $0.10 | Every 6h |
| ⛏️ MINER | Dedupe, rank, tag | Haiku | $0.05 | After Scout |
| 🔨 FORGE | Write content (all formats) | Sonnet | $0.30 | After Miner |
| 📡 BLAST | Format for platforms | Haiku | $0.05 | After Forge |
| 🛡️ GUARD | QA + compliance | Haiku | $0.03 | After Blast |

**Daily cost: ~$0.53 | Monthly: ~$16**
**Runs as a chain: Scout → Miner → Forge → Blast → Guard → Jay reviews**

---

## TEAM 2: Fiverr Gig Workers
On-demand agents — spawned when orders come in

| Agent | Fiverr Gig | Model | Cost/Gig | Price |
|-------|-----------|-------|----------|-------|
| ✍️ SCRIBE | "30 days of AI social media posts" | Sonnet | ~$0.50 | $75-150 |
| 🎯 HUNTER | "500 verified leads in your niche" | Haiku | ~$0.30 | $100-200 |
| 📝 BLOGGER | "10 SEO blog posts for your site" | Sonnet | ~$1.00 | $150-300 |
| 📊 INTEL | "Competitor analysis report" | Sonnet | ~$0.60 | $200-500 |
| 🎬 DIRECTOR | "AI video scripts (30 scripts)" | Sonnet | ~$0.50 | $75-150 |
| 📅 PLANNER | "30-day content calendar" | Haiku | ~$0.20 | $75-150 |

**Profit margin: 95%+ (AI cost is pennies, Fiverr price is dollars)**
**All output goes through GUARD for QA before delivery**

---

## TEAM 3: Internal Ops (always running)
| Agent | Role | Model | Schedule |
|-------|------|-------|----------|
| 🤖 FRANKIE | Orchestrator, Jay's right hand | Opus/Sonnet | Always on |
| 💓 HEARTBEAT | System health checks | Haiku | Every 30min |

---

## How It Works

### Content Machine (daily, automated)
```
Frankie spawns Scout at 5 AM
  → Scout finishes → Frankie spawns Miner
    → Miner finishes → Frankie spawns Forge
      → Forge finishes → Frankie spawns Blast
        → Blast finishes → Frankie spawns Guard
          → Guard finishes → QA report to Jay
            → Jay approves → content goes live
```

### Fiverr Gigs (on-demand)
```
Jay gets Fiverr order for "30 social media posts"
  → Jay tells Frankie "new Scribe job: [client niche]"
    → Frankie spawns SCRIBE with client brief
      → SCRIBE produces 30 posts
        → Frankie spawns GUARD for QA
          → GUARD approves → Frankie packages for delivery
            → Jay delivers on Fiverr
```

### Parallel Capacity
- Content machine uses 1 agent at a time (chain, not parallel)
- Fiverr gigs can run 6 concurrent jobs while content machine runs
- Peak load: 1 content agent + 6 Fiverr agents + Frankie = 8 (max)
- If overloaded: Fiverr jobs queue, content machine has priority

---

## Spawn Commands (for Frankie)

### Content Machine
```
sessions_spawn(task="Run SCOUT agent per content-machine/agents/SCOUT.md", model="haiku", label="scout")
sessions_spawn(task="Run MINER agent per content-machine/agents/MINER.md", model="haiku", label="miner")
sessions_spawn(task="Run FORGE agent per content-machine/agents/FORGE.md", model="sonnet", label="forge")
sessions_spawn(task="Run BLAST agent per content-machine/agents/BLAST.md", model="haiku", label="blast")
sessions_spawn(task="Run GUARD agent per content-machine/agents/GUARD.md", model="haiku", label="guard")
```

### Fiverr Gigs
```
sessions_spawn(task="Run SCRIBE: [client brief]", model="sonnet", label="scribe-[client]")
sessions_spawn(task="Run HUNTER: [niche + location]", model="haiku", label="hunter-[client]")
sessions_spawn(task="Run BLOGGER: [topic + keywords]", model="sonnet", label="blogger-[client]")
```
