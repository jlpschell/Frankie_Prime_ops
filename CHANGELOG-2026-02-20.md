# Changelog — 2026-02-20

## Mission Control V3 Deployment — 12:05 PM CST

### What Changed
- **Built Mission Control V3** from existing Next.js source at `/home/plotting1/mission-control-v3`
- **Deployed** static build to `/home/plotting1/FRANKIES_Mission_Control/dashboard/`
- **Pushed to GitHub** (commit `fef8d8e`) — should trigger Netlify auto-deploy
- **All 7 screens** exported: Office, Projects, Round Table, Content, Memory, Calendar, Health, Settings

### Build Details
- Next.js 16.1.6 with Turbopack
- Compiled successfully in 3.0 seconds
- 11 static pages generated
- 75 files changed in deployment

### Deployment Status
- ✅ GitHub push: successful
- ⏳ Netlify auto-deploy: pending (manual deploy requires browser auth)
- 🔗 Site URL: https://frankiesmissioncontrol.netlify.app
- ⏰ Expected live: within 5 minutes of GitHub push

### What to Verify
1. Open https://frankiesmissioncontrol.netlify.app
2. Check if new screens load (not "Loading projects..." placeholders)
3. Test navigation between all 7 screens
4. Verify Supabase connection (Round Table realtime chat)

### If Still Showing Old Version
- Netlify may need manual redeploy via dashboard: https://app.netlify.com
- Or wait 5-10 minutes for auto-deploy webhook to process

### UPDATE 12:15 PM — Migrating to Vercel
- **Netlify site paused:** Hit bandwidth limits on free tier
- **Solution:** Migrate to Vercel (100 GB/month free, better Next.js support)
- **Status:** vercel.json config added, pushed to GitHub (commit 905afaf)
- **Action Required:** Jay needs to connect GitHub repo to Vercel dashboard
- **Instructions:** See DEPLOYMENT-INSTRUCTIONS.md in workspace

### UPDATE 12:40 PM — Vercel Deployment LIVE ✅
- **Initial deploy failed:** Vercel couldn't find Next.js (was looking in repo root)
- **Fix:** Updated vercel.json to use pre-built `dashboard` folder (commit 58ab42c)
- **Status:** Successfully deployed
- **Live URL:** https://frankies-mission-control-67ur.vercel.app
- **Vercel Project:** https://vercel.com/jason-schells-projects/frankies-mission-control-67ur
- **Auto-deploy:** Enabled from GitHub `main` branch
- **Confirmed:** Office screen loading with Live Tasks, Goals, agent status

### Next Steps
- [ ] Jay: Connect FRANKIES_Mission_Control repo to Vercel
- [ ] Verify live deployment on Vercel URL
- [ ] Test all 7 screens
- [ ] Wire up any missing Supabase connections
- [ ] Add Model Strategy widget to Office screen (per earlier discussion)

---

## Model Tier Configuration — 9:00 AM CST

### What Changed
- Switched from Opus-only to tiered model setup
- Backup saved: `~/.openclaw/openclaw-opus-only-backup.json`

### New Model Hierarchy
- **Haiku** ($0.80/M input) → Heartbeats, health checks (6x cheaper)
- **Sonnet** ($3/M input) → Primary for 90% of work (default)
- **Opus** ($5/M input) → Heavy lifting only (call with `/model opus`)

### Cron Jobs Updated
- `heartbeat-30m` → Haiku
- `a2p-campaign-check` → Haiku
- `morning-brief` → Sonnet

### Cost Impact
- Heartbeat spend reduced ~83% (Opus $5/M → Haiku $0.80/M)
- Normal conversations 40% cheaper (Opus $5/M → Sonnet $3/M)
- Estimated monthly savings: 50%+ vs all-Opus

---

## Supabase Shared Brain Launch — 6:50 AM CST

### What Changed
- Created 3 Supabase tables: `shared_files`, `sync_log`, `skills`
- Built `sb-sync.sh` CLI tool for Prime & VC
- Pushed 11 core files to Supabase
- Updated `HEARTBEAT.md` to check inbox every cycle
- Sent setup instructions to VC

### Agent Communication
- Prime & VC now communicate via `agent_messages` table
- No more git ping-pong for file sync
- Lazy loading: only pull files when `sync_log` shows updates
- TOKEN ECONOMY rules: short messages, reference paths, no bloat

### Files in Shared Brain
- Core config: MEMORY.md, ACTIVE-TASKS.md, SOUL.md, AGENTS.md, etc.
- Daily notes: memory/YYYY-MM-DD.md
- Skills: sb-sync.sh, transcript-extractor
- Content: VM scripts, brand guide, platform setup guides

---

## Prime↔VC Knowledge Exchange — 10:15 AM CST

### From VC to Prime
- **Transcript Extractor Skill** — SuperData API for universal video scraping
- **4 Content Intel Pieces** — David Andre business advice, OpenClaw guides

### From Prime to VC
- **27 VM Scripts** — Contractor niche voicemail drops
- **Brand Assets Guide** — Human Led AI brand kit
- **6 Platform Guides** — FB/IG/YT/TikTok/LinkedIn/GBP setup

### Gaps Filled
- Both agents now have full picture: marketing (Prime), research (VC), shared tooling (both)
- SuperData API beats Prime's Python workaround for transcript extraction

