#!/usr/bin/env python3
"""
Simple cost tracker for OpenClaw sessions.
Logs token usage and estimated costs.
"""
import json
import os
from datetime import datetime

COST_LOG = "memory/cost_tracking.jsonl"

# Current pricing (update as needed)
PRICING = {
    "openrouter/anthropic/claude-sonnet-4.5": {
        "input": 0.003,   # per 1K tokens
        "output": 0.015
    },
    "google/gemini-flash-latest": {
        "input": 0.0,
        "output": 0.0
    },
    "openrouter/pony-alpha": {
        "input": 0.0,
        "output": 0.0
    }
}

def log_session_cost(model, tokens_in, tokens_out, notes=""):
    """Log a session's cost"""
    pricing = PRICING.get(model, {"input": 0, "output": 0})
    
    cost_in = (tokens_in / 1000) * pricing["input"]
    cost_out = (tokens_out / 1000) * pricing["output"]
    total_cost = cost_in + cost_out
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_in": round(cost_in, 4),
        "cost_out": round(cost_out, 4),
        "total_cost": round(total_cost, 4),
        "notes": notes
    }
    
    os.makedirs(os.path.dirname(COST_LOG), exist_ok=True)
    with open(COST_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    return entry

def get_daily_costs(days=7):
    """Get cost summary for last N days"""
    if not os.path.exists(COST_LOG):
        return {}
    
    daily_totals = {}
    
    with open(COST_LOG, 'r') as f:
        for line in f:
            entry = json.loads(line.strip())
            date = entry['timestamp'][:10]  # YYYY-MM-DD
            
            if date not in daily_totals:
                daily_totals[date] = {
                    "total_cost": 0,
                    "tokens_in": 0,
                    "tokens_out": 0,
                    "sessions": 0
                }
            
            daily_totals[date]["total_cost"] += entry["total_cost"]
            daily_totals[date]["tokens_in"] += entry["tokens_in"]
            daily_totals[date]["tokens_out"] += entry["tokens_out"]
            daily_totals[date]["sessions"] += 1
    
    return daily_totals

if __name__ == "__main__":
    # Log current session
    log_session_cost(
        model="openrouter/anthropic/claude-sonnet-4.5",
        tokens_in=181000,
        tokens_out=394,
        notes="Gmail cleanup + voicemail generation session"
    )
    
    # Show summary
    print("\n📊 Cost Tracking Summary\n")
    print("=" * 60)
    
    daily = get_daily_costs()
    for date, data in sorted(daily.items(), reverse=True)[:7]:
        print(f"\n{date}:")
        print(f"  💰 Total: ${data['total_cost']:.4f}")
        print(f"  📊 Tokens: {data['tokens_in']:,} in / {data['tokens_out']:,} out")
        print(f"  🔄 Sessions: {data['sessions']}")
    
    print("\n" + "=" * 60)
    print(f"✅ Cost log: {COST_LOG}")
