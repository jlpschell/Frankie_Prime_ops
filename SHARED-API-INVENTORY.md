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
- SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjd2ZwZmpkYXVmeXlnd3h2dHR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA1ODcwNDksImV4cCI6MjA4NjE2MzA0OX0.vX8_61e6-AVUN200aTnfz3KOtlzfGSyF9x_-0bdqScA
- SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjd2ZwZmpkYXVmeXlnd3h2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDU4NzA0OSwiZXhwIjoyMDg2MTYzMDQ5fQ.hgslj4vngqBr950UrhG-2-5AaUNY1uvxOO9TcbHkB74

### Go High Level (Prime owns, VC read-only for dashboard)
- GHL_API_KEY=pit-aad2f6de-29c3-4814-98b8-8839ad265471
- GHL_LOCATION_ID=tabcgomNBVaWpWAkIXL8
- GHL_BASE_URL=https://services.leadconnectorhq.com
- Working scopes: contacts (read/write), conversations
- NOT working: campaigns (401), locations (401), phone/A2P (no API)

### ElevenLabs (Both — Prime renders VM audio, VC could too)
- ELEVENLABS_API_KEY=9a7ea3d8c90e8550990ec82da85a0f25e2a42c035081a942c12214bb50ee1e44
- Voice IDs: Eric=9T9vSqRrPPxIs5wpyZfK, Chris=iP95p4xoKVk53GoZ742B

### OpenAI (Both)
- OPENAI_API_KEY=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

### Gemini (Both — 3 keys for rotation)
- GEMINI_API_KEY=AIzaSyBucUyIMtwvPvR5DW58St_hdqbDfXgU2T4
- GEMINI_API_KEY_FALLBACK=AIzaSyB4FAJ64r_zsNt0EWqPzk9CUjcuzbIBfZg
- GEMINI_API_KEY_FLASH=AIzaSyDmXZGi5Cx_Z39VxZiq6ofeupOnJjH3Gng

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
- Prime Bridge: frankieHQ_prime_2026_d3llPr3c (port 3001)
- VC Bridge: frankieHQ_vc_2026_x9k2m
- Prime OpenClaw Hook: frankieHQ_prime_hook_2026

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
