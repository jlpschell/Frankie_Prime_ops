#!/bin/bash

# NVIDIA Kimi K2.5 Setup for OpenClaw
# Completely FREE model with multimodal capabilities (text, image, video)

set -e

echo "🚀 Setting up NVIDIA Kimi K2.5 (100% FREE)"
echo ""

# Check if NVIDIA API key exists
if grep -q "NVIDIA_API_KEY" ~/.openclaw/.env; then
    echo "✅ NVIDIA_API_KEY found in .env"
else
    echo "❌ NVIDIA_API_KEY not found"
    echo ""
    echo "📋 TO GET YOUR FREE NVIDIA API KEY:"
    echo "1. Go to: https://build.nvidia.com/moonshotai/kimi-k2.5"
    echo "2. Click 'Login' (top right)"
    echo "3. Create/login to NVIDIA account"
    echo "4. Verify with phone number"
    echo "5. Click 'View Code' → 'Generate API Key'"
    echo "6. Copy the key (starts with nvapi-)"
    echo ""
    echo "Then add to ~/.openclaw/.env:"
    echo "NVIDIA_API_KEY=nvapi-[your-key-here]"
    echo ""
    echo "❌ Exiting. Add API key first, then re-run this script."
    exit 1
fi

echo "🔧 Backing up current configs..."
cp ~/.openclaw/agents/main/agent/models.json ~/.openclaw/agents/main/agent/models.json.backup-$(date +%Y%m%d-%H%M)
cp ~/.openclaw/agents/main/agent/auth-profiles.json ~/.openclaw/agents/main/agent/auth-profiles.json.backup-$(date +%Y%m%d-%H%M)

echo "🚀 Installing NVIDIA Kimi K2.5 config..."
cp nvidia-kimi-config.json ~/.openclaw/agents/main/agent/models.json
cp nvidia-auth-update.json ~/.openclaw/agents/main/agent/auth-profiles.json

echo "🔄 Restarting OpenClaw gateway..."
openclaw gateway restart

echo "⏳ Waiting for restart..."
sleep 3

echo "✅ Testing model availability..."
openclaw models list

echo ""
echo "🎉 NVIDIA Kimi K2.5 setup complete!"
echo ""
echo "📊 Model capabilities:"
echo "  • 1 Trillion parameters"
echo "  • Multimodal: text, image, video"
echo "  • 2M context window"
echo "  • Mixture-of-Experts architecture"
echo "  • COMPLETELY FREE (no rate limits mentioned)"
echo ""
echo "🎯 Set as default:"
echo "  openclaw models default nvidia/moonshotai/kimi-k2.5"
echo ""
echo "💰 Cost reduction: 100% (FREE vs $5/1M for Opus)"