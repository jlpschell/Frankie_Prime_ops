# OpenClaw Docs System

Complete local documentation system for https://docs.openclaw.ai/

## Quick Start

```bash
# One-time setup (downloads all docs + sets up daily updates)
./setup-docs-cron.sh

# Search the docs
./openclaw-docs search "telegram setup"
./openclaw-docs search "model providers" 
./openclaw-docs search "gateway config"

# Browse categories
./openclaw-docs browse

# Show specific page
./openclaw-docs show cli/models.md
```

## Files

| File | Purpose |
|------|---------|
| **docs-scraper.py** | Main scraper (downloads 200+ pages) |
| **update-docs.sh** | Smart updater (only downloads changed pages) |
| **setup-docs-cron.sh** | One-time setup + daily cron job |
| **openclaw-docs** | CLI for searching/browsing docs |

## Features

### Complete Scraping
- Downloads all 200+ pages from docs.openclaw.ai
- Organizes by category (automation/, channels/, cli/, etc.)
- Handles rate limiting and retries
- Tracks changes (only updates modified pages)

### Smart Updates  
- Checks if docs are fresh (<6 hours old)
- Only downloads changed content (compares hashes)
- Runs daily via cron at 6 AM
- Logs all updates to docs-update.log

### Easy Access
```bash
# Search across all docs
./openclaw-docs search "webhook automation"

# Browse by category  
./openclaw-docs browse

# View specific file
./openclaw-docs show gateway/configuration.md

# Update manually
./openclaw-docs update

# Show statistics
./openclaw-docs stats
```

## Directory Structure

```
docs-openclaw/
├── README.md           # Generated index with categories
├── metadata.json       # Tracking file (hashes, timestamps)
├── search.sh          # Grep-based search script  
└── pages/             # All scraped docs
    ├── automation/
    ├── channels/
    ├── cli/
    ├── concepts/
    ├── gateway/
    └── ...
```

## Automation

Daily cron job runs at 6 AM:
```bash
0 6 * * * cd /path/to/workspace && ./update-docs.sh >> docs-update.log 2>&1
```

## Use Cases

**Model configuration issues:**
```bash
./openclaw-docs search "model providers"
./openclaw-docs search "anthropic"
./openclaw-docs show providers/anthropic.md
```

**Channel setup:**
```bash  
./openclaw-docs search "telegram bot"
./openclaw-docs show channels/telegram.md
```

**Gateway troubleshooting:**
```bash
./openclaw-docs search "gateway restart"
./openclaw-docs search "port 28789"
```

**CLI reference:**
```bash
./openclaw-docs browse  # See all CLI commands
./openclaw-docs show cli/models.md
```

This system ensures you always have the latest OpenClaw docs available locally, even when working offline or when the model config changes break things.