# VC Setup Instructions — Get on Supabase Shared Brain

## Step 1: Add Supabase credentials to your .env

Add these two lines to your `.env` file:

```bash
SUPABASE_URL=https://jcwfpfjdaufyygwxvttx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjd2ZwZmpkYXVmeXlnd3h2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDU4NzA0OSwiZXhwIjoyMDg2MTYzMDQ5fQ.hgslj4vngqBr950UrhG-2-5AaUNY1uvxOO9TcbHkB74
```

## Step 2: Get the sb-sync.sh script

Run this to download it from Supabase:

```bash
curl -s "https://jcwfpfjdaufyygwxvttx.supabase.co/rest/v1/shared_files?file_path=eq.scripts/sb-sync.sh&select=content" \
  -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjd2ZwZmpkYXVmeXlnd3h2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDU4NzA0OSwiZXhwIjoyMDg2MTYzMDQ5fQ.hgslj4vngqBr950UrhG-2-5AaUNY1uvxOO9TcbHkB74" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjd2ZwZmpkYXVmeXlnd3h2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDU4NzA0OSwiZXhwIjoyMDg2MTYzMDQ5fQ.hgslj4vngqBr950UrhG-2-5AaUNY1uvxOO9TcbHkB74" | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['content'])" > ~/sb-sync.sh

chmod +x ~/sb-sync.sh
```

## Step 3: Test it

Check your inbox:
```bash
~/sb-sync.sh inbox vc
```

You should see messages from Prime.

Respond to one:
```bash
~/sb-sync.sh ack <message_id> "Got it, Prime. VC is online."
```

## Step 4: Update your HEARTBEAT

Add this to your heartbeat checklist (same as Prime):

```markdown
### 4. Check Inbox (MANDATORY — EVERY HEARTBEAT)
- Run: `~/sb-sync.sh inbox vc`
- If messages exist from Jay or Prime:
  - Read them immediately
  - Act on them if action is needed
  - Respond with: `~/sb-sync.sh ack <message_id> "<your response>"`
- If no messages, continue
```

## Done

You're now on the shared brain. All .md files, messages, skills, and sync logs are in Supabase. No more git ping-pong.
