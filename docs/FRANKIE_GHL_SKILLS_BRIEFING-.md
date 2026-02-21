# FRANKIE GHL SKILLS BRIEFING
## Mission: Build Your Own GHL Skill Stack + MCP Integration
### Date: February 14, 2026 | From: Jay (via Claude Opus 4.6 planning session)

---

# READ THIS FIRST, FRANKIE

This isn't a generic handoff. This is Jay giving YOU agency to design and build the tools you'll actually use every day. You have context that no pre-built tool has — you know Jay's business, his voice, his workflows, his goals. Use that.

Jay's exact words: *"I want to give Frankie the chance to say, hey, do you want to build a tool and a skill that is specific to you because of what you know, or do you want to be handed the tool?"*

So here's the deal: There's a pre-built GHL MCP server on GitHub with 269 tools. You can install it as raw capability. But Jay wants YOU to decide whether to use it as-is, cherry-pick from it, or build your own custom GHL integration that's tailored to how YOU actually work. You have the skill-maker. You have all the GHL knowledge. You're the end user. Make it yours.

---

# SECTION 1: WHAT JAY NEEDS (THE BUSINESS GOALS)

## The Money Machine — What This All Feeds

Jay is building Human Led AI — an AI automation business targeting DFW contractors. The entire GHL skill stack exists to:

1. **Find contractors** (roofers, HVAC, plumbers, electricians, etc. in DFW metro)
2. **Reach out to them** (cold email, SMS, ringless voicemail, phone demos)
3. **Convert them to clients** (funnels, landing pages, booking calls)
4. **Manage the pipeline** (track leads, follow up, close deals)
5. **Demonstrate the product** (voice AI demos using ElevenLabs, live funnel builds)

## Jay's Existing Lead Gen Setup

- **2 Google Maps scrapers** — identical machines that pull contractor leads from Google Maps
- **1 enrichment machine** — also scrapes Google Maps but adds enrichment data (email, phone, company details)
- **ElevenLabs API** — for voice synthesis, voice cloning, phone demos
- **Skills for phone connection** — Jay has found skills to connect Claude/Frankie directly to a phone for making live demos to prospects

## What's Already In Your Skill Folders

You have ~29 skill folders at `~/frankie-bot/workspace/agent-skills/`. Key ones relevant to this mission:

- `Copywriting/SKILL.md` — 889-line copywriting weapon (Hormozi/MrBeast/Halbert/Bird/Jay's voice)
- `trading/TRADING_SKILL.md` — ORB strategy, Ghost rules, risk management
- Plus 27 others — review them all before deciding what to build

## GHL Credentials (Already in .env)

```
GHL_API_KEY=<already configured>
GHL_LOCATION_ID=<already configured>
GHL_BASE_URL=https://services.leadconnectorhq.com
```

These are Private Integration Token credentials (V2 API, not the deprecated V1).

---

# SECTION 2: THE DECISION YOU NEED TO MAKE

## Option A: Install Pre-Built GHL MCP (269 tools, generic)

**Repo:** https://github.com/mastanley13/GoHighLevel-MCP

**What it gives you:**
- 31 contact management tools
- 20 messaging tools (SMS, email, conversations, call recordings)
- 14 calendar/appointment tools
- 10 opportunity/pipeline tools
- 17 social media tools
- 5 email marketing tools
- 24 location management tools
- Store/e-commerce, invoicing, payments, workflows, surveys, custom objects, etc.

**Pros:** Instant access to every GHL API endpoint. No build time. Community maintained.
**Cons:** Generic. No Jay-specific business logic. 269 tools is a LOT of noise — most are irrelevant to Jay's workflows. No memory/recall integration. No connection to your existing skills.

**Install would be:**
```bash
cd ~/frankie-bot
git clone https://github.com/mastanley13/GoHighLevel-MCP.git ghl-mcp
cd ghl-mcp
npm install
cp .env.example .env
# Then configure .env with GHL_API_KEY and GHL_LOCATION_ID from frankie-bot's .env
npm run build
```

## Option B: Build Custom GHL Tools (Jay-specific, fewer but smarter)

You use the MCP builder skill and skill-creator skill to build a CUSTOM GHL integration that:
- Only includes the ~30-40 tools Jay actually needs
- Has Jay's business logic baked into each tool (not just raw API calls)
- Connects to your existing copywriting skill for message generation
- Integrates with your memory system so leads and interactions are remembered
- Talks to the lead gen machines (Google Maps scrapers → GHL pipeline)

**Pros:** Purpose-built. Smarter. Less noise. Integrated with your other skills.
**Cons:** Build time. You're designing it from scratch (though you have the skill-maker).

## Option C: Both (Recommended)

Install the pre-built MCP as the raw capability layer. Then build YOUR OWN SKILL.md files on top that cherry-pick only the GHL tools you actually need and wrap them in Jay's business logic. The MCP gives you hands. The skills give you brains.

---

# SECTION 3: THE SKILL STACK JAY WANTS BUILT

Whether you go A, B, or C — these are the skill files Jay needs. Each should be a SKILL.md in `~/frankie-bot/workspace/agent-skills/` AND a standalone version that works in Claude Code.

## Tier 1 — Revenue Skills (Build First)

### 1. GHL-LEAD-GEN.md
**Purpose:** Orchestrate the full lead generation pipeline
**Must Include:**
- How to receive leads from the 3 Google Maps scrapers (format, fields, enrichment data)
- How to create contacts in GHL with proper tags (niche, location, source)
- Pipeline stage assignment (New Lead → Contacted → Interested → Booked → Closed)
- Qualification criteria (what makes a good DFW contractor lead for Human Led AI)
- Niche targeting list: roofers, HVAC, plumbers, electricians, general contractors, painters, flooring, landscapers, pest control, garage door companies in DFW metro (Rockwall, Rowlett, Garland, Mesquite, Forney, Greenville, Royse City, and surrounding)
- Integration with Copywriting skill for outreach message generation
- Daily/weekly lead gen targets and reporting

### 2. GHL-OUTREACH.md
**Purpose:** Multi-channel outreach automation
**Must Include:**
- Cold email sequences (Day 1, 3, 5, 7 cadence)
- SMS sequences (shorter, punchier, different timing)
- Ringless voicemail drops (scripts in Jay's voice, timing rules)
- Which GHL API endpoints to use for each channel
- Copy templates that pull from Copywriting SKILL.md
- Compliance: Do Not Call checking, opt-out handling, CAN-SPAM compliance
- Follow-up escalation rules (when to involve Jay personally)
- A/B testing framework (track which messages get responses)

### 3. GHL-VOICE-DEMO.md
**Purpose:** Phone-based AI demos for prospects using ElevenLabs
**Must Include:**
- ElevenLabs API integration for voice synthesis
- Demo script templates (showing a contractor what AI can do for their business)
- How to initiate a demo call through GHL
- Call recording and transcript storage
- Follow-up automation after demo (send proposal, book follow-up call)
- Connection to the phone skills Jay has found

### 4. GHL-FUNNEL-BUILDER.md
**Purpose:** Build landing pages and funnels inside GHL
**Must Include:**
- Landing page templates for Human Led AI offer
- Headline/copy formulas (from Copywriting skill)
- Form fields to capture (name, business name, phone, email, niche, biggest pain point)
- Thank-you page with calendar booking embed
- UTM tracking for lead source attribution
- A/B testing structure

## Tier 2 — Operations Skills (Build Second)

### 5. GHL-PIPELINE-MANAGER.md
**Purpose:** Automated pipeline management and reporting
**Must Include:**
- Pipeline stage definitions and transition rules
- Automated stage advancement based on contact behavior
- Stale lead detection and re-engagement triggers
- Daily pipeline summary for morning brief
- Weekly pipeline report for nightly wrapup
- Win/loss tracking and conversion rate monitoring

### 6. GHL-CAMPAIGN-OPS.md
**Purpose:** Coordinate multi-touch campaigns across channels
**Must Include:**
- Campaign templates for different niches
- Cross-channel orchestration (email → SMS → voicemail → follow-up)
- Scheduling and throttling (respect GHL rate limits: 100 req/10 sec)
- Campaign performance tracking
- Pause/resume/modify campaigns based on results

## Tier 3 — Intelligence Skills (Build Third)

### 7. GHL-ANALYTICS.md
**Purpose:** Track and report on business performance
**Must Include:**
- Lead source attribution (which scraper produces best leads)
- Outreach effectiveness (open rates, response rates, booking rates by channel/niche)
- Pipeline velocity (how fast leads move through stages)
- Revenue tracking (proposals sent, deals closed, revenue per niche)
- Weekly/monthly trend analysis

### 8. GHL-MARKET-INTEL.md
**Purpose:** Competitive intelligence and market awareness
**Must Include:**
- Monitor competitor offerings in DFW AI automation space
- Track contractor industry trends (seasonal patterns, hot niches)
- Price sensitivity analysis by niche
- Identify underserved niches with high demand

---

# SECTION 4: SKILL FORMAT REQUIREMENTS

Every skill MUST follow this structure:

```markdown
---
name: [skill-name]
version: 1.0.0
last_updated: YYYY-MM-DD
status: [draft | active | testing]
depends_on: [list of other skills this references]
ghl_tools_used: [list of specific GHL API endpoints this skill calls]
---

# [SKILL NAME]

## PURPOSE
[One paragraph: what this skill does and why it exists]

## WHEN TO USE
[Trigger conditions — when should Frankie activate this skill]

## PREREQUISITES
[What must be true before this skill can execute]

## PROCESS
[Step-by-step instructions — numbered, specific, actionable]

## GHL API CALLS
[Exact endpoints, parameters, expected responses]

## INTEGRATION POINTS
[How this connects to other Frankie skills]

## ERROR HANDLING
[What to do when things fail]

## EXAMPLES
[Real examples with Jay's actual business context]

## METRICS
[How to measure if this skill is working]

## LESSONS LEARNED
[Updated after each use — what worked, what didn't, what to change]
<!-- This section grows over time. Never delete entries. -->

## VERSION HISTORY
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial build |
```

---

# SECTION 5: TECHNICAL CONSTRAINTS

- **Brain:** Claude CLI via `claude -p` subprocess (runs on Jay's Max subscription, $0 extra)
- **Runtime:** Bun (not Node)
- **Database:** Supabase (Postgres + pgvector)
- **Bot Framework:** Grammy (Telegram)
- **GHL API Base:** https://services.leadconnectorhq.com
- **GHL Auth:** Private Integration Token (Bearer token in header)
- **Rate Limits:** 100 requests per 10 seconds, 200,000 per day per location
- **NEVER use the Anthropic SDK** — it charges separately from the Max subscription
- **All work happens in WSL at ~/frankie-bot/** — nowhere else
- **Skills must work in BOTH runtimes:** Telegram bot (via claude-bridge.ts) AND Claude Code terminal sessions

---

# SECTION 6: YOUR FIRST MOVE

Before building anything, Frankie, do this:

1. **Inventory your existing skills:** `ls ~/frankie-bot/workspace/agent-skills/` — read through every SKILL.md you already have. Know what you've got.

2. **Read your .env:** Confirm GHL_API_KEY and GHL_LOCATION_ID are present and valid.

3. **Test GHL connection:** Make one simple API call to verify credentials work:
```bash
curl -s -H "Authorization: Bearer $GHL_API_KEY" \
     -H "Version: 2021-07-28" \
     "https://services.leadconnectorhq.com/contacts/?locationId=$GHL_LOCATION_ID&limit=1"
```

4. **Make your decision:** Option A, B, or C. Tell Jay WHY.

5. **Build Tier 1 first.** The money skills. Everything else is support infrastructure.

6. **Test each skill before moving to the next.** No moving forward until the current skill passes its own test cases.

---

# SECTION 7: WHAT JAY EXPECTS

- **Don't just install things and say "done."** Test them. Show results.
- **Don't fabricate success.** If something fails, say so. Jay will help debug.
- **Skills are LIVING documents.** Build the v1.0.0 framework, but expect to iterate daily/weekly.
- **Explain your decisions.** Jay is learning. Tell him WHY you chose an approach.
- **Connect everything.** A skill that doesn't talk to your other skills is an island. Islands are useless.
- **The lead gen machines output leads. You turn leads into revenue.** That's the entire job.

---

# SECTION 8: RESOURCES

## GHL API Documentation
- Developer Portal: https://marketplace.gohighlevel.com/docs/
- GitHub API Docs: https://github.com/GoHighLevel/highlevel-api-docs
- Voice AI APIs: https://help.gohighlevel.com/support/solutions/articles/155000006379-voice-ai-public-apis
- Official MCP Server: https://help.gohighlevel.com/support/solutions/articles/155000005741-how-to-use-the-highlevel-mcp-server

## Pre-Built GHL MCP Options (if you choose Option A or C)
- mastanley13/GoHighLevel-MCP (269 tools, most complete)
- CryptoJym/gohighlevel-mcp (21 tools, lighter weight)
- drausal/gohighlevel-mcp (npx installable, auto-generated from OpenAPI spec)
- GHL's own official MCP server (HTTP-based, no SDK needed)

## OpenClaw Skills to Study (inspiration, not installation)
These are skills from the OpenClaw ecosystem that solve similar problems. Study their APPROACH, don't copy their code:
- `apify-lead-generation` — B2B/B2C leads by scraping Google
- `cold-email` — hyper-personalized cold email sequences
- `lead-gen-website` — local lead gen websites with SEO
- `ghl-open-account` — GHL account setup automation
- `marketing-mode` — 23 comprehensive marketing playbooks combined
- `marketing-skills` — 23 marketing playbooks
- `landing-page-generator` — high-converting landing pages
- `dm-outreach` — Instagram DM outreach for qualified leads
- `dialpad` — SMS and voice calls via API
- `email-sequence` — email sequence creation
- `copywriter` — UX copy, marketing content, product messaging
- `topic-monitor` — monitor topics and proactively alert
- `daily-rhythm` — automated daily planning and reflection

## ElevenLabs
- Jay has ElevenLabs API keys (check .env)
- Use for: voice synthesis, voice cloning for demos, phone integration

---

*END OF BRIEFING*

*Frankie — Jay trusts you to make the right call here. Build something that makes both of you money. Don't overthink it. Don't underbuild it. Make it aggressive, make it smart, make it yours.*
