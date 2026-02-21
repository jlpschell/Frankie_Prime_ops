---
name: ghl-mastery
description: GoHighLevel CRM expert. Use for GHL setup, Voice AI agents, Conversation AI, workflows, API integrations, SaaS configuration, calendar booking, AI employee components. Triggers: "GHL", "GoHighLevel", "HighLevel", "voice agent", "AI employee", "LC phone".
allowed-tools: Read, Write, Bash, Glob, Grep, WebFetch, WebSearch
---

# GHL Mastery

> Complete GoHighLevel expertise — from sub-account setup to advanced Voice AI automation

## When to Use This Skill

**Good for:**
- Setting up Voice AI agents (inbound + outbound)
- Configuring Conversation AI (SMS, WhatsApp, chat, DMs)
- Building workflows with AI triggers
- API integrations and webhooks
- SaaS sub-account management
- Calendar and booking configuration
- Prompt engineering for AI agents
- Troubleshooting GHL issues

**Not for:**
- General CRM theory (this is GHL-specific)
- Non-GHL platforms

---

## GHL Architecture Overview

```
Agency Level (SaaS Mode)
└── Sub-Accounts (Locations)
    ├── Contacts
    ├── Opportunities/Pipelines
    ├── Calendars
    ├── Workflows
    ├── AI Employee (per sub-account)
    │   ├── Voice AI
    │   ├── Conversation AI
    │   ├── Reviews AI
    │   ├── Funnel AI
    │   ├── Content AI
    │   ├── Workflow AI Assistant
    │   └── Ask AI
    ├── Funnels/Websites
    └── Campaigns
```

---

## AI Employee Components (2026)

### 1. Voice AI (Inbound + Outbound)

**Inbound Setup:**
```markdown
Settings → Voice AI → Create Agent
1. Name the agent
2. Select voice (40+ options)
3. Set initial greeting
4. Configure knowledge base
5. Add actions (transfer, workflow, SMS, book, update field, API)
6. Set response speed to "Normal" (NOT Fast)
7. Increase idle time to 6-7 seconds for older demographics
```

**Outbound Setup (NEW 2026):**
```markdown
Workflow → Add Action → Outbound Voice AI Call
1. Select agent
2. Choose phone number
3. Configure trigger (form submit, missed call, etc.)
4. Register for outbound (Settings → AI Agents → Enable Outbound)
```

**Outbound Limits:**
- 1 call per number per day
- Max 4 calls per number in 2 weeks
- Calls only 10 AM - 6 PM (contact's timezone)
- Automatic DNC list checking

**Critical Settings:**
| Setting | Recommended | Why |
|---------|-------------|-----|
| Response Speed | Normal | Fast causes interruptions |
| Idle Time | 6-7 seconds | Elderly/slower speakers |
| Max Actions During Call | 3-4 | Latency stacks |
| Prompt Location | Top-loaded | AI searches top-down |

**Prompt Best Practices:**
- Put critical info at TOP of prompt
- Use words "critical" and "mandatory" for must-follow rules
- Markdown formatting (hashtags, dashes — no emojis)
- Numbered steps for sequences
- Edit prompts in Google Docs (version control)
- Test with 100+ calls before going live
- Use Google Voice for testing (not built-in test)

**Knowledge Base Hack:**
```markdown
Instead of scraping messy client websites:
1. Create a GHL funnel page
2. Paste all knowledge as clean text
3. Scrape THAT funnel URL
4. Result: Clean, organized knowledge base
```

**Action Types:**
1. **Call Transfer** — route to human
2. **Trigger Workflow** — fire automation
3. **Send SMS** — immediate text
4. **Book Appointment** — native calendar booking (NEW 2026)
5. **Update Contact Field** — capture info
6. **Custom API Action** — external systems

### 2. Conversation AI

**Channels:**
- SMS
- WhatsApp
- Live Chat widget
- Instagram DMs
- Facebook DMs

**Key Settings:**
| Setting | Value | Notes |
|---------|-------|-------|
| Response Delay | 2 seconds | Feels natural |
| Max Messages | 25 | Safety limit for loops |
| Shared Knowledge Base | Yes | Same as Voice AI |

**Actions:**
- Book appointments
- Sunset conversations (exit gracefully)
- Update contact fields
- Trigger workflows
- Transfer to specialist bots

### 3. Reviews AI

**Setup:** Reputation → Settings → Reviews AI

**Optimization:**
```markdown
1. Inject keywords: "Include phrases like 'best [service] in [city]'"
2. Add footer CTA: "PS: Visit mysite.com/offer for 10% off"
3. Auto-responds to Google reviews
4. Set and forget
```

### 4. Funnel AI

**Current:** Beta — generates single pages from prompts
**Coming:** Full prompt-to-funnel builder

### 5. Content AI

**Available everywhere:**
- Generate with AI
- Improve writing
- Fix spelling/grammar
- Simplify writing
- Make longer/shorter

### 6. Workflow AI Assistant

**How to use:** Natural language to automation
```
"Build automation that sends email when contact created"
```

**Rating:** B+ for learning, good for simple automations

### 7. Ask AI

**What it is:** ChatGPT-style overlay for entire CRM
**Current:** Beta
**Potential:** Sub-account analytics access

---

## Workflows

### Workflow Triggers

| Trigger Type | Use Case |
|--------------|----------|
| Contact Created | Lead capture |
| Form Submitted | Funnel actions |
| Appointment Booked | Confirmation flow |
| Tag Added | Segmentation actions |
| Opportunity Stage Changed | Pipeline automation |
| Inbound Call | Voice AI fallback |
| Voice AI Action | Bot-triggered workflows |

### AI Agent Workflow Patterns

**Pattern 1: Lead Response**
```
Form Submit → Wait 30s → Outbound Voice AI Call → If No Answer → SMS Follow-up
```

**Pattern 2: Missed Call Recovery**
```
Missed Call → Immediate SMS → Wait 5min → Outbound Voice AI Call
```

**Pattern 3: Appointment Reminder**
```
Appointment -24h → SMS Reminder → Appointment -1h → SMS Reminder
```

**Pattern 4: Review Request**
```
Opportunity Won → Wait 7 days → SMS Review Request → Reviews AI monitors response
```

---

## API Integration

**API Docs Location:** `/jay/human_led_ai/go_high_level/highlevel-api-docs-main/`

**Key Endpoints:**

| Endpoint | Use |
|----------|-----|
| `/contacts` | Create, update, search contacts |
| `/calendars` | Get availability, book appointments |
| `/conversations` | Send messages, get history |
| `/workflows` | Trigger workflows via API |
| `/opportunities` | Manage pipeline deals |
| `/locations` | Sub-account management |

**OAuth Setup:**
```markdown
1. Create app in GHL Marketplace
2. Get client_id and client_secret
3. OAuth 2.0 flow for access tokens
4. Refresh tokens before expiry (24h default)
```

**Webhook Events:**
- ContactCreate, ContactUpdate, ContactDelete
- AppointmentCreate, AppointmentUpdate, AppointmentDelete
- OpportunityStageUpdate, OpportunityStatusUpdate
- InboundMessage, OutboundMessage
- InvoicePaid, InvoiceCreate

---

## SaaS Mode

**Agency Setup:**
```markdown
Settings → SaaS → Enable SaaS Mode
1. Set billing (Stripe integration)
2. Create pricing tiers
3. Configure sub-account provisioning
4. Set feature limits per tier
```

**Snapshots:**
```markdown
Create → Settings → Snapshots → Create Snapshot
1. Select what to include (workflows, funnels, calendars)
2. Save template
3. Apply to new sub-accounts for instant setup
```

---

## Troubleshooting

### Voice AI Issues

| Problem | Solution |
|---------|----------|
| Bot interrupts caller | Set response speed to Normal |
| Bot doesn't wait for answer | Increase idle time to 6-7s |
| Bot hallucinating | Reduce prompt length, be explicit |
| Actions not firing | Check trigger conditions match exactly |
| Call quality poor | Use LC Phone (not Twilio) |

### Common Mistakes

1. **Writing vague prompts** — Be extremely explicit
2. **Too many during-call actions** — Latency stacks, keep to 3-4
3. **Not testing with real calls** — Built-in test isn't accurate
4. **Conflicting workflow triggers** — One trigger per action type
5. **Overloading knowledge base** — Keep it focused and clean

---

## Selling Voice AI

**Don't sell "Voice AI" directly** — businesses guard phone numbers

**Bundle approach:**
1. Database reactivation (low-hanging fruit)
2. Reputation management (Google reviews)
3. Conversational AI + Voice AI as bonus

**Pitch points:**
- Deploy in 7 days (not 4 months)
- Answer 100% of calls
- Never makes mistakes
- Knows everything about your business

**Never mention:**
- "GoHighLevel"
- Technical bot/model details
- That it's AI (unless required)

---

## Quick Reference

### Phone Numbers
- Use LC Phone (GHL's Twilio), not direct Twilio
- Voice AI requires LC Phone connection

### Pricing (2026)
- AI Employee Unlimited: $97/month (unlimited LLM usage)
- Text/Voice usage: Standard LC rates
- Outbound Voice Engine: Consumption-based (was free through Dec 2025)

### Resources

**Local files:**
- API Docs: `/jay/human_led_ai/go_high_level/highlevel-api-docs-main/`
- Reference: `/knowledge/ghl_reference.md`
- NotebookLM Sources: `/drive_sync/takeout/extracted/Takeout/NotebookLM/gohighlevel crm/`

**External:**
- GHL Support: help.gohighlevel.com
- GHL Ideas/Changelog: ideas.gohighlevel.com
- GHL Marketplace: marketplace.gohighlevel.com

---

## Checklist: New Voice AI Agent

```markdown
- [ ] Define agent purpose (inbound/outbound/both)
- [ ] Select voice and name
- [ ] Write initial greeting (identify as AI if preferred)
- [ ] Build prompt in Google Docs first
- [ ] Put critical instructions at TOP of prompt
- [ ] Create knowledge base (clean funnel page method)
- [ ] Configure actions (limit during-call to 3-4)
- [ ] Set response speed to Normal
- [ ] Increase idle time to 6-7 seconds
- [ ] Create supporting workflows
- [ ] Test with Google Voice (100+ calls before live)
- [ ] Monitor and iterate on prompt
```

## Checklist: Outbound Campaign

```markdown
- [ ] Register for outbound calling (Settings → AI Agents → Enable)
- [ ] Wait for approval (KYC check)
- [ ] Create workflow trigger (form submit, missed call, etc.)
- [ ] Add Outbound Voice AI Call action
- [ ] Select agent and phone number
- [ ] Configure follow-up actions (no answer, voicemail)
- [ ] Test with internal numbers first
- [ ] Monitor dashboard for sentiment and success rates
```
