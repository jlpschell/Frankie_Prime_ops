# Unsubscribe Agent - Gemini Commands

These are the commands Gemini uses to control the unsubscribe worker.

## Start Unsubscribe Run

```bash
# Full run (500 emails)
cd /home/plotting1/frankie-bot/workspace/unsubscribe-agent && nohup node worker.js > logs/run.log 2>&1 &

# Scan more emails
cd /home/plotting1/frankie-bot/workspace/unsubscribe-agent && nohup node worker.js --max=1000 > logs/run.log 2>&1 &

# Dry run (preview only)
cd /home/plotting1/frankie-bot/workspace/unsubscribe-agent && node worker.js --dry-run
```

## Check Status

```bash
# Get current status
cd /home/plotting1/frankie-bot/workspace/unsubscribe-agent && node worker.js --status

# Get progress of active run
cd /home/plotting1/frankie-bot/workspace/unsubscribe-agent && node worker.js --progress

# View live log
tail -f /home/plotting1/frankie-bot/workspace/unsubscribe-agent/logs/run.log
```

## View Results

```bash
# Latest scan results (senders found)
cat /home/plotting1/frankie-bot/workspace/unsubscribe-agent/logs/last-scan.json

# Find latest report
ls -lt /home/plotting1/frankie-bot/workspace/unsubscribe-agent/logs/unsubscribe-report-*.json | head -1
```

## Status File Meanings

The worker writes to `logs/worker-status.json`:

- `idle` - No runs yet
- `running` - Worker is active
- `scanning` - Finding emails with unsubscribe links
- `unsubscribing` - Processing links
- `complete` - Run finished
- `error` - Something broke

## Progress File

During active runs, `logs/worker-progress.json` contains:

```json
{
  "current": 15,
  "total": 100,
  "percent": 15,
  "currentSender": "newsletter@example.com",
  "timestamp": "2025-02-10T23:00:00.000Z"
}
```

## Exclusion List

Edit `/home/plotting1/frankie-bot/workspace/unsubscribe-agent/config.js` to add/remove exclusions.
Current exclusions: heygen, tiktok, chris lee, julian goldie, adt, skool
