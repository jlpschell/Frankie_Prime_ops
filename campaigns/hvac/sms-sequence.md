# HVAC SMS Sequence
## DFW Campaign — February 2026

---

## SMS 1 — Initial (Day 2 after VM)
**Trigger:** 1 day after VM drop

```
Hey {{first_name}}, this is Jason. Left you a voicemail about helping HVAC companies in DFW stay booked year-round. Worth a quick chat?
```

---

## SMS 2 — Value Nudge (Day 4)
**Trigger:** 2 days after SMS 1, no response

```
{{first_name}} - just following up. I put together a free breakdown for HVAC owners on how to add 25-30% more service calls without chasing leads. Want me to send it over?
```

---

## SMS 3 — Breakup (Day 7)
**Trigger:** 3 days after SMS 2, no response

```
Hey {{first_name}}, last one from me. If filling your schedule during slow months isn't a problem for you, no worries. But if it is, I've got something that works. Just reply "info" and I'll send it.
```

---

## SMS 4 — Final Breakup (Day 10)
**Trigger:** 3 days after SMS 3, no response

```
{{first_name}} - closing the loop on this. If you ever want to chat about keeping your crews busy year-round, I'm here. Good luck out there.
```

---

## Merge Fields
- `{{company_name}}` — Business name from lead list (optional use)
- `{{first_name}}` — Contact first name (if available)

## Response Handling
- Any reply -> Move to "Hot" status in GHL
- "Stop" or "Unsubscribe" -> Remove from sequence, mark DNC
- Question -> Route to Jay for personal follow-up
