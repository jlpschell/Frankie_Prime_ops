#!/bin/bash

# Setup daily cron job to update OpenClaw docs

SCRIPT_DIR="$(realpath $(dirname "$0"))"
CRON_SCRIPT="$SCRIPT_DIR/update-docs.sh"

echo "🕒 Setting up OpenClaw docs auto-update"

# Make scripts executable
chmod +x "$SCRIPT_DIR/update-docs.sh"
chmod +x "$SCRIPT_DIR/docs-scraper.py"

# Create cron job entry
CRON_ENTRY="0 6 * * * cd $SCRIPT_DIR && ./update-docs.sh >> $SCRIPT_DIR/docs-update.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "update-docs.sh"; then
    echo "✅ Cron job already exists"
else
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "✅ Added daily cron job at 6 AM"
fi

echo "📋 Cron job: Updates docs daily at 6 AM"
echo "📝 Log file: $SCRIPT_DIR/docs-update.log"
echo "🔍 Manual update: ./update-docs.sh"

# Run initial scrape
echo ""
echo "🚀 Running initial docs scrape..."
./update-docs.sh