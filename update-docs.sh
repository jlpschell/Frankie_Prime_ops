#!/bin/bash

# OpenClaw Docs Auto-Updater
# Checks for doc updates and pulls them down

set -e

SCRIPT_DIR="$(dirname "$0")"
DOCS_DIR="$SCRIPT_DIR/docs-openclaw"

echo "🦞 OpenClaw Docs Updater"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if initial scrape exists
if [ ! -d "$DOCS_DIR" ]; then
    echo "📥 First-time setup - running full scrape..."
    python3 docs-scraper.py
    exit 0
fi

# Check last update time
METADATA_FILE="$DOCS_DIR/metadata.json"
if [ -f "$METADATA_FILE" ]; then
    LAST_UPDATE=$(jq -r '.last_update // empty' "$METADATA_FILE")
    if [ -n "$LAST_UPDATE" ]; then
        # Convert to timestamp and check age
        if command -v date >/dev/null 2>&1; then
            LAST_TS=$(date -d "$LAST_UPDATE" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "${LAST_UPDATE%.*}" +%s 2>/dev/null || echo "0")
            NOW_TS=$(date +%s)
            AGE_HOURS=$(( (NOW_TS - LAST_TS) / 3600 ))
            
            echo "📅 Last update: $LAST_UPDATE ($AGE_HOURS hours ago)"
            
            if [ $AGE_HOURS -lt 6 ]; then
                echo "✅ Docs are fresh (updated within 6 hours)"
                echo "🔍 Use: ./docs-openclaw/search.sh 'query' to search"
                echo "📖 Use: cat docs-openclaw/README.md to browse index"
                exit 0
            fi
        fi
    fi
fi

echo "🔄 Checking for updates..."
python3 docs-scraper.py

echo ""
echo "✅ Update complete!"
echo "🔍 Search: cd docs-openclaw && ./search.sh 'your query'"
echo "📖 Browse: cat docs-openclaw/README.md"