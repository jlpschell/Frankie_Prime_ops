# Workspace Rules Skill

## Before Building/Installing ANYTHING:

### Check INVENTORY.md First:
**Location:** `/home/plotting1/.openclaw/workspace/INVENTORY.md`
1. Check INVENTORY.md — lists all packages, scripts, services
2. Check `frankie-bot/src/library/` — existing services  
3. Check `frankie-bot/workspace/scripts/` — existing scripts
4. **If exists = USE IT.** Do not rebuild.

**Rebuilding existing tools = VIOLATION**

### Check .env Before Asking for Credentials:
**Locations:** 
- `/home/plotting1/.openclaw/.env`
- `/home/plotting1/frankie-bot/.env`

**Both files contain ALL API keys and tokens.**
**Asking Jay for keys that exist in .env = VIOLATION**

### Available Keys:
- Anthropic, OpenAI, Groq, Gemini
- Telegram/Discord bot tokens
- Supabase (URL + keys)
- GHL API key + location ID
- Google OAuth (3 accounts)
- GitHub PAT, Notion API
- ElevenLabs API key

## Rule: Check first, never ask Jay for what you can access.