#!/usr/bin/env python3
import os
import json
import requests

OPENROUTER_API_KEY = os.environ.get('OPENCLAW_OPENROUTER_API_KEY')

prompt = """Write 3 natural-sounding voicemail scripts for HVAC companies in DFW.

Requirements:
- Casual, conversational tone
- Include "umm" or natural pauses ("...")
- Speaker introduces himself as Jason
- Mentions helping HVAC companies get 25% more jobs in 45 days
- Says "on autopilot" casually
- Ends with "give me a call back or send me a quick text for more info"
- Sound like a real person leaving a voicemail, not a script

Return only the 3 scripts, numbered 1-3."""

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openrouter/pony-alpha",
        "messages": [{"role": "user", "content": prompt}]
    }
)

result = response.json()

if 'choices' in result:
    content = result['choices'][0]['message']['content']
    print("\n🦍 PONY ALPHA OUTPUT:\n")
    print("=" * 60)
    print(content)
    print("\n" + "=" * 60)
    
    usage = result.get('usage', {})
    print(f"\n📊 Tokens: {usage.get('prompt_tokens', 0)} in / {usage.get('completion_tokens', 0)} out")
    print(f"💰 Cost: $0.00 (FREE)")
else:
    print("❌ Error:", result)

