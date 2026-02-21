#!/bin/bash
# === FRANKIE PRIME — SKILLS INSTALL ===
# Paste this entire block into your terminal and hit Enter.

cd ~/.openclaw/workspace

clawhub install obsidian
clawhub install sherpa-onnx-tts
clawhub install summarize
clawhub install notion
clawhub install voice-call
clawhub install nano-pdf
clawhub install nano-banana-pro
clawhub install codexbar
clawhub install mcporter
clawhub install goplaces
clawhub install gog
clawhub install github
clawhub install gh-issues
clawhub install gemini-cli
clawhub install clawhub
clawhub install openai-whisper-api
clawhub install groq-voice

echo "Skills installed. Restarting gateway..."
openclaw gateway restart
echo "Done. Frankie is back up."
