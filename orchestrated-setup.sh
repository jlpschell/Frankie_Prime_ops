#!/bin/bash

# Orchestrated Model Strategy Setup
# Uses NVIDIA Kimi (FREE) + OpenAI Subscription ($20/mo) + Gemini (FREE) + Claude (emergency)

set -e

echo "🚀 Setting up Orchestrated Model Strategy"
echo "Goal: 97% cost reduction while preserving Claude quality"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check NVIDIA API key
if ! grep -q "NVIDIA_API_KEY" ~/.openclaw/.env; then
    echo "❌ NVIDIA_API_KEY missing from .env"
    echo "Get free key at: https://build.nvidia.com/moonshotai/kimi-k2.5"
    echo "Then add: NVIDIA_API_KEY=nvapi-[your-key]"
    echo ""
fi

echo "✅ Prerequisites checked"
echo ""

# Show current backups
echo "📁 Current backups:"
echo "Models: $(ls ~/.openclaw/agents/main/agent/models.json.backup-* | tail -1)"
echo "Auth: $(ls ~/.openclaw/agents/main/agent/auth-profiles.json.backup-* | tail -1)"
echo ""

# Apply orchestrated config
echo "🔧 Applying orchestrated model configuration..."
cp orchestrated-models-config.json ~/.openclaw/agents/main/agent/models.json
cp orchestrated-auth-profiles.json ~/.openclaw/agents/main/agent/auth-profiles.json

echo "🔗 Setting up OpenAI subscription auth..."
echo "Run this command manually: openclaw auth openai codex"
echo "(Follow the OAuth flow to connect your ChatGPT subscription)"
echo ""

echo "🔄 Restarting OpenClaw gateway..."
openclaw gateway restart

echo "⏳ Waiting for restart..."
sleep 3

echo "✅ Testing model availability..." 
openclaw models list

echo ""
echo "🎯 Set primary model to FREE NVIDIA Kimi:"
echo "openclaw models default nvidia/moonshotai/kimi-k2.5"
echo ""

echo "🎉 Orchestrated strategy deployed!"
echo ""
echo "💰 Cost structure:"
echo "  • 80% usage: COMPLETELY FREE (Kimi + Gemini + Groq)"
echo "  • 15% usage: $20/month flat (OpenAI subscription)"
echo "  • 5% usage: ~$50/month (Claude for critical tasks)"
echo "  • TOTAL: $70/month vs $2,700/month (97% savings)"
echo ""
echo "🔀 Fallback chain:"
echo "  1. NVIDIA Kimi K2.5 (FREE) → 2. Gemini Flash (FREE) → 3. OpenAI Sub ($20/mo) → 4. Claude (emergency)"
echo ""
echo "🚨 Next steps:"
echo "1. Get NVIDIA API key if missing"
echo "2. Run: openclaw auth openai codex"
echo "3. Set default: openclaw models default nvidia/moonshotai/kimi-k2.5"