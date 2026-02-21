#!/bin/bash
# ElevenLabs TTS wrapper - auto-pulls API key from openclaw.json

set -e

# Usage check
if [ $# -lt 2 ]; then
    echo "Usage: $0 \"text to speak\" output.mp3"
    exit 1
fi

TEXT="$1"
OUTPUT="$2"

# Auto-detect API key from openclaw.json
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: openclaw.json not found at $CONFIG_FILE"
    exit 1
fi

# Extract API key using jq
API_KEY=$(jq -r '.skills.entries.sag.apiKey // empty' "$CONFIG_FILE")

if [ -z "$API_KEY" ]; then
    echo "Error: ElevenLabs API key not found in openclaw.json"
    echo "Expected path: skills.entries.sag.apiKey"
    exit 1
fi

# ElevenLabs config
VOICE_ID="${ELEVENLABS_VOICE_ID:-21m00Tcm4TlvDq8ikWAM}"  # Default: Rachel
MODEL_ID="${ELEVENLABS_MODEL:-eleven_monolingual_v1}"
API_URL="https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID"

# Make request
echo "Generating speech..."
echo "Voice ID: $VOICE_ID"
echo "Output: $OUTPUT"

HTTP_CODE=$(curl -w "%{http_code}" -o "$OUTPUT" -X POST "$API_URL" \
  -H "xi-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"$TEXT\",\"model_id\":\"$MODEL_ID\"}" \
  --silent)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Success! Audio saved to: $OUTPUT"
    
    # Show file info
    if command -v file &> /dev/null; then
        file "$OUTPUT"
    fi
    
    if command -v ls &> /dev/null; then
        ls -lh "$OUTPUT"
    fi
else
    echo "❌ Error: API returned HTTP $HTTP_CODE"
    cat "$OUTPUT"  # Show error message
    rm -f "$OUTPUT"
    exit 1
fi
