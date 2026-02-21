#!/bin/bash
# Frankie File Mover — checks Jay's drop folder and copies to workspace
# Two-way:
#   from-jay/  → Jay drops files, Prime grabs them to workspace/inbox/
#   from-prime/ → Prime puts files, Jay picks them up from Windows

WINDOWS_BASE="/mnt/c/Users/Jay/Desktop/Frankie_C_Openclaw_Claude/Prime Files"
FROM_JAY="$WINDOWS_BASE/from-jay"
FROM_PRIME="$WINDOWS_BASE/from-prime"
INBOX="/home/plotting1/.openclaw/workspace/inbox"

mkdir -p "$FROM_JAY" "$FROM_PRIME" "$INBOX"

# Count files in Jay's drop folder (not dirs, not hidden)
count=$(find "$FROM_JAY" -maxdepth 1 -type f ! -name '.*' 2>/dev/null | wc -l)

if [ "$count" -gt 0 ]; then
    echo "FOUND $count file(s) from Jay:"
    for f in "$FROM_JAY"/*; do
        [ -f "$f" ] || continue
        fname=$(basename "$f")
        cp "$f" "$INBOX/$fname"
        echo "  ✅ $fname → inbox/"
    done
    # Move originals to a processed subfolder so we don't re-grab
    mkdir -p "$FROM_JAY/.processed"
    for f in "$FROM_JAY"/*; do
        [ -f "$f" ] || continue
        mv "$f" "$FROM_JAY/.processed/"
    done
else
    echo "NO_NEW_FILES"
fi
