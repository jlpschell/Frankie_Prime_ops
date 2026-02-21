# Shared API Inventory — Frankie Fleet
# Last updated: 2026-02-19 by [Prime]
# Both agents should have ALL of these in their .env files

## Division of Labor
- **Prime** = Professional / Business (GHL, leads, enrichment, outreach, marketing, revenue)
- **VC** = Personal / Hobby (trading, investments, social content, research, personal organization)
- **Shared** = Both need access (Supabase, Linear, Typefully, Notion, GitHub, dashboard)

## API Keys — Full Fleet Access

### Supabase (SHARED BRAIN — both MUST use)
- SUPABASE_URL=https://jcwfpfjdaufyygwxvttx.supabase.co
- SUPABASE_ANON_KEY=[REDACTED]
- SUPABASE_SERVICE_ROLE_KEY=[REDACTED]

### Go High Level (Prime owns, VC read-only for dashboard)
- GHL_API_KEY=[REDACTED - see .env]
- GHL_LOCATION_ID=tabcgomNBVaWpWAkIXL8
- GHL_BASE_URL=https://services.leadconnectorhq.com
- Working scopes: contacts (read/write), conversations
- NOT working: campaigns (401), locations (401), phone/A2P (no API)

### ElevenLabs (Both — Prime renders VM audio, VC could too)
- ELEVENLABS_API_KEY=9a7ea3d8c90e8550990ec82da85a0f25e2a42c035081a942c12214bb50ee1e44
- Voice IDs: Eric=9T9vSqRrPPxIs5wpyZfK, Chris=iP95p4xoKVk53GoZ742B

### OpenAI (Both)
- OPENAI_API_KEY=[REDACTED]

### Gemini (Both — 3 keys for rotation)
- GEMINI_API_KEY=[REDACTED - see .env]
- GEMINI_API_KEY_FALLBACK=[REDACTED - see .env]
- GEMINI_API_KEY_FLASH=[REDACTED - see .env]

### Google Workspace
- Personal (jlpschell@gmail.com):
  - GOOGLE_PERSONAL_CLIENT_ID=581850119904-bqpi8pcs0r841ji1244l0ei1na0b8rsc.apps.googleusercontent.com
  - GOOGLE_PERSONAL_CLIENT_SECRET=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
  - GOOGLE_PERSONAL_REFRESH_TOKEN=1//01p9OS16VjFRCCgYIARAAGAESNwF-L9IrCHrC2-XxanGNDUQgQ0k4oaPN_ECC6G05IPQqjzuemMQsN6iy78tvItdkgfwKL2ih9Ek
- Business (humanledai@gmail.com):
  - GOOGLE_BUSINESS_CLIENT_ID=581850119904-bqpi8pcs0r841ji1244l0ei1na0b8rsc.apps.googleusercontent.com
  - GOOGLE_BUSINESS_CLIENT_SECRET=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
  - GOOGLE_BUSINESS_REFRESH_TOKEN=1//0fXlSd9U66Lu3CgYIARAAGA8SNwF-L9IreEpamtfYDCv-XQZ_69pzDhOK32Wh0iVBHMDaMBZ8x-BDzmY6lHglru_13H73Ail9DSQ

### Outscraper (Prime owns — lead scraping)
- OUTSCRAPER_API_TOKEN=N2U3MTY4ZjU2NGMwNGEyOTk4MTZkYzNlYzQ1OTIzYTB8OTM3ZTc1MTA5YQ
- NOTE: Credits depleted as of 2026-02-19 3:50 AM — needs top-up

### Twilio (Prime owns — SMS/voice)
- TWILIO_ACCOUNT_SID=AC0082e2ed94cbc405c2d4400e4e6212d0
- TWILIO_AUTH_TOKEN=072d5838f878ef4b1c34e80745cd562e

### GitHub
- GITHUB_PAT — stored in /home/plotting1/frankie-bot/.env as GITHUB_PAT
- User: jlpschell

### Bridge API Tokens
- Prime Bridge: [REDACTED - see .env] (port 3001)
- VC Bridge: [REDACTED]
- Prime OpenClaw Hook: [REDACTED]

### Tailscale Endpoints
- Prime: https://plotting.tail4c8a54.ts.net (100.97.30.40)
- VC: https://jasus-1.tail4c8a54.ts.net (100.84.195.50)

## MISSING — Need from VC or Jay
- SuperData API key (VC has it: sd_cc309c...)
- Linear API key (VC setting up)
- Typefully API key (VC setting up)
- Notion API key (VC setting up)
- Brave Search API key (Prime needs for web_search tool)

## MISSING — Need from Jay
- GHL browser login (for A2P Trust Center checks via browser automation)
- Any upgraded GHL API token with phone/campaign scopes
