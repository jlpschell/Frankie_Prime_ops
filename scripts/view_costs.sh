#!/bin/bash
echo ""
echo "📊 OpenClaw Cost Tracking"
echo "============================================================"
echo ""

if [ ! -f memory/cost_tracking.jsonl ]; then
    echo "No cost data logged yet."
    exit 0
fi

# Summary by date
echo "💰 Daily Costs:"
cat memory/cost_tracking.jsonl | python3 -c "
import json, sys
from collections import defaultdict

daily = defaultdict(lambda: {'cost': 0, 'tokens_in': 0, 'tokens_out': 0})

for line in sys.stdin:
    entry = json.loads(line.strip())
    date = entry['timestamp'][:10]
    daily[date]['cost'] += entry['total_cost']
    daily[date]['tokens_in'] += entry['tokens_in']
    daily[date]['tokens_out'] += entry['tokens_out']

for date in sorted(daily.keys(), reverse=True)[:7]:
    d = daily[date]
    print(f'  {date}: \${d[\"cost\"]:.4f} ({d[\"tokens_in\"]:,} in / {d[\"tokens_out\"]:,} out)')

total = sum(d['cost'] for d in daily.values())
print(f'\n💵 Total Spend: \${total:.4f}')
"

echo ""
echo "============================================================"
echo "📝 Log file: memory/cost_tracking.jsonl"
