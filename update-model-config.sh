#!/bin/bash

# Update OpenClaw Model Configuration
# Adds cheap models: Gemini Flash (FREE), GPT-4o Mini, Groq Llama, Ollama Qwen

set -e

echo "🔧 Updating OpenClaw model configuration..."

# Backup current configs
echo "📁 Backing up current configs..."
cp ~/.openclaw/agents/main/agent/models.json ~/.openclaw/agents/main/agent/models.json.backup-$(date +%Y%m%d-%H%M)
cp ~/.openclaw/agents/main/agent/auth-profiles.json ~/.openclaw/agents/main/agent/auth-profiles.json.backup-$(date +%Y%m%d-%H%M)

# Apply new configs
echo "🚀 Applying new model configurations..."
cp models-config-update.json ~/.openclaw/agents/main/agent/models.json
cp auth-profiles-update.json ~/.openclaw/agents/main/agent/auth-profiles.json

# Restart OpenClaw to pick up new configs
echo "🔄 Restarting OpenClaw gateway..."
openclaw gateway restart

# Wait for restart
sleep 3

# Test new models
echo "✅ Testing model availability..."
openclaw models list

echo "🎉 Model configuration updated successfully!"
echo ""
echo "📊 New cost structure:"
echo "  FREE: Gemini 2.0 Flash, Groq Llama 3.3 70B, Ollama Qwen 2.5"
echo "  CHEAP: GPT-4o Mini (\$0.15/1M), Gemini 1.5 Flash (\$0.075/1M)"
echo "  MODERATE: GPT-4o (\$2.50/1M), Gemini 1.5 Pro (\$1.25/1M)" 
echo "  PREMIUM: Claude Sonnet (\$3/1M), Claude Opus (\$5/1M)"
echo ""
echo "🎯 Set default to Gemini Flash with: openclaw models default google/gemini-2.0-flash-exp"