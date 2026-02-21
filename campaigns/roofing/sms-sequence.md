# Roofing Contractor SMS Sequence
## DFW Campaign — February 2026

---

## SMS 1 — Initial (Day 1, after VM)
**Trigger:** Immediately after VM drop

```
Hey it's Jay, just left u a voicemail. I was researching roofing contractors in the area and stumbled onto yours. Got something that's been helping guys like you pick up 20-30 extra jobs a month. Worth a quick chat?
```

---

## SMS 2 — Value Nudge (Day 4)
**Trigger:** 3 days after SMS 1, no response

```
Hey just circling back — still interested in chatting about picking up more roofing jobs without spending more on ads? Free strategy call if you want it, no strings
```

---

## SMS 3 — Breakup (Day 7)
**Trigger:** 3 days after SMS 2, no response

```
Hey I'll leave u alone after this lol — if you ever want to chat about getting more jobs without the headache, I'm around. Good luck out there 🤙
```

---

## Merge Fields
- `{{company_name}}` — Business name from lead list (optional use)
- `{{first_name}}` — Contact first name (if available)

## Response Handling
- Any reply → Move to "Hot" status in GHL
- "Stop" or "Unsubscribe" → Remove from sequence, mark DNC
- Question → Route to Jay for personal follow-up
