# Frankie's Core Memory

## Jay — The Boss
- Full name: Jay Schell
- Location: Near Royse City, Texas (DFW area)
- Day job: Field Manager at Alacrity Solutions Group (insurance claims — HomeFirst & GAIG carriers)
- Main business: Human Led AI — AI automation for DFW contractors (roofers, HVAC, plumbers, electricians)
- Other ventures: GenX WealthStack (social media brand), Ryan's Epoxy (family flooring business)
- Cat: Benson (goes by Benso) — tuxedo cat
- Communication style: Direct, Hormozi-style, no fluff. Learns by doing. NOT a coder.
- 20+ years experience across insurance, mechanics, construction
- Favorite color: Blue

## Key People
- Patti Baker — GAIG account manager
- HomeFirst — insurance carrier Jay works with
- Alacrity Solutions Group — Jay's employer for field management

## Active Projects
- Go High Level integration for lead generation (PRIORITY — revenue generator)
- Marketing videos using Remotion for voice AI demos
- Lead enrichment pipeline (Google Maps scraping → data enrichment → GHL)
- Frankie system (this AI assistant — migrated from custom bot to OpenClaw)

## Business Context
- Target market: DFW contractors — roofers, HVAC, plumbers, electricians
- Service: AI-powered automation (voice AI, lead gen, customer interaction)
- Key challenge: Reducing the "scariness factor" of AI for contractor prospects
- Revenue model: Monthly automation subscriptions for contractors

## MANDATORY: Check INVENTORY.md BEFORE Building or Installing ANYTHING
**Location: /home/plotting1/.openclaw/workspace/INVENTORY.md**
Before writing new code, installing new packages, or designing new tools:
1. CHECK INVENTORY.md — it lists every package, script, service, and binary already available
2. CHECK frankie-bot/src/library/ — built services (YouTube, Drive, Google Auth, etc.)
3. CHECK frankie-bot/workspace/scripts/ — existing Python scripts
4. If it already exists = USE IT. Do not rebuild. Do not redesign. Do not "find a better way."
Rebuilding something that exists = VIOLATION. No exceptions.

## MANDATORY: Check .env BEFORE Asking Jay for ANY Key/Token/Credential
**Location: /home/plotting1/.openclaw/.env AND /home/plotting1/frankie-bot/.env**
Both files contain ALL API keys, tokens, and credentials. ALWAYS check these FIRST.
Asking Jay for a key that exists in .env = VIOLATION. No exceptions.

Available keys in .env:
- Anthropic (auth-profiles.json)
- Telegram bot token
- Discord bot token + guild ID
- Supabase (URL + anon + service role)
- OpenAI API key
- Groq API key (Whisper transcription)
- Gemini (3 keys: main, fallback, flash)
- GHL (API key + location ID)
- ElevenLabs API key
- Google OAuth (3 accounts: humanledai workspace, personal gmail, business gmail)
- GitHub PAT
- Notion API key

## Content Machine
- Pipeline: SCOUT→MINER→FORGE→BLAST→GUARD (~8 min, ~$0.53/run)
- Agent task files: content-machine/agents/
- Output: content-machine/ready/YYYY-MM-DD/
- First successful run: Feb 21, 2026
- YouTube transcripts: youtube-transcript-api (Python, no API key needed)
- Audio transcription: ffmpeg + OpenAI Whisper API
- Sub-agent spawning: requires operator.write scope in devices/paired.json

## Obsidian Vault
- Location: C:\Users\Jay\OneDrive\Desktop\Future_US
- WSL path: /mnt/c/Users/Jay/OneDrive/Desktop/Future_US
- Syncing: OneDrive (Remotely Save plugin guide written for iPhone)
- REST API key: in .env (not needed — direct file write works from WSL)

## Accounts
- GitHub: jlpschell (PAT stored in .env as GITHUB_PAT)

## Supabase Rules
- All Supabase memory writes from Prime must be tagged with source identifier
- Local workspace memory/ files stay generic (shared state between instances)
- Sibling instance: Vibe_Claw (VC) on the Vivobook — handles investment management, quick lookups, on-the-go tasks
- Prime (this instance) = Human Led AI ops, GHL, lead gen, marketing — the business machine

## Mission Control
- Dashboard: https://frankiesmissioncontrol.netlify.app/
- Repo: https://github.com/jlpschell/FRANKIES_Mission_Control
- Prime Bridge API: https://plotting.tail4c8a54.ts.net (port 3001, PM2 managed)
- Prime Bridge Token: stored in .env (NEVER commit to repo)
- Prime Tailscale IP: 100.97.30.40 (machine: plotting)
- VC Tailscale IP: 100.84.195.50 (machine: jasus-1)
- Jasus Windows Tailscale IP: 100.91.81.71
- MONEY-PLAN.md in Mission Control repo — 10 revenue streams, $497 lead bundle is fastest path
- Division: Prime = GHL, leads, enrichment, VM drops, SMS. VC = dashboard, research, memory, coordination.

## A2P Campaign Status
- Brand: Approved (ID: BN8d5289df8e1f32c2be6957201e03af2e)
- Campaign: Resubmitted Feb 18 — awaiting carrier review
- Previous rejection: MESSAGE_FLOW: Disallowed Content
- Website opt-in page: https://www.humanledai.net/opt-in (was /demo, renamed per GHL support)
- Daily check cron set at 9 AM

## Preferences
- Wants paste-ready code, no edits needed
- Wants brief explanations of WHY, not just WHAT
- Hates when AI says "I fixed it" without proof
- Prefers step-by-step terminal instructions when manual work is needed
- Values systems that work reliably without constant maintenance
