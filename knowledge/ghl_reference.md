# GoHighLevel CRM Reference - Human Led AI

## Overview
GoHighLevel (GHL) is an all-in-one CRM and marketing automation platform. Your NotebookLM sources contain 21+ video transcripts covering the full platform.

---

## AI Employee (7 Components)

The AI Employee is a per-sub-account feature with seven components:

### 1. Voice AI
**What it does:** Handles inbound phone calls via AI agent

**Setup Modes:**
- **Basic Mode:** Quick answering service setup
  - Agent name, business name, language, voice selection
  - Initial answer message
  - Goal: Collect name, email, address, issue
  - Auto-assigns call summary as contact note
  - Email notifications on call completion

- **Advanced Mode:** Full prompt control
  - Knowledge base integration
  - Custom prompting (2,000 character limit)
  - 6 action types: Call transfer, trigger workflow, send SMS, book appointment, update contact field, custom API action

**Critical Settings (2025 Update):**
1. **UPGRADE YOUR BOT** - Look for upgrade button in top right
2. **Response Speed:** Set to "Normal" (NOT Fast - causes interruptions)
3. **Idle Time:** Increase to 6-7 seconds for elderly audiences
4. Test with 100+ calls before going live
5. Use Google Voice for testing (not built-in test feature)

**Best Practices:**
- Put critical info at TOP of prompt (AI searches top-down)
- Use words "critical" and "mandatory" for essential instructions
- Use Markdown formatting (no emojis, use hashtags and dashes)
- Use numbered steps to keep AI organized
- Edit prompts in Google Docs (version control, backup)
- Keep "during call" actions minimal (3-4 max) - latency adds up
- Put non-critical actions in "after call" section

**Pro Tip: Knowledge Base Hack**
Instead of web scraping messy sites:
1. Create a GHL funnel page
2. Paste all your knowledge as clean text
3. Scrape THAT funnel page URL
4. Result: Clean, organized knowledge base

**Outbound:** Expected fall 2025

### 2. Conversation AI
**What it does:** Handles text-based messaging (SMS, WhatsApp, live chat, DMs)

**Channels supported:**
- SMS
- WhatsApp
- Live Chat widget
- Instagram DMs
- Facebook DMs

**Key Settings:**
- Response delay (e.g., 2 seconds)
- Max messages: 25 (safety limit for bot loops)
- Shares knowledge base with Voice AI

**Actions available:**
- Book appointments
- Sunset conversations (exit gracefully)
- Update contact fields
- Trigger workflows
- Transfer to other bots (specialist handoffs)

### 3. Reviews AI
**What it does:** Auto-responds to Google reviews

**Setup:** Reputation → Settings → Reviews AI

**Pro Tips:**
- Inject keywords: "Be sure to include phrases like 'best paintball in Denver'"
- Add footer with CTA: "PS: Head to mysite.com/bonus for 10% off"
- Set and forget - works while you sleep

### 4. Funnel AI
**What it does:** Generates landing pages from prompts

**Current Status:** Beta - generates single page with copy and design
**Expected:** Full prompt-to-funnel builder by fall 2025

### 5. Content AI
**What it does:** AI writing assistance throughout the platform

**Features:**
- Generate with AI
- Improve writing
- Fix spelling/grammar
- Simplify writing
- Make longer/shorter

### 6. Workflow AI Assistant
**What it does:** Guided automation builder

**Rating:** B+ for learning builders
**Example:** "Build automation that sends email when contact created"

### 7. Ask AI
**What it does:** ChatGPT-style overlay for entire CRM

**Current Status:** Beta - least valuable feature currently
**Potential:** Could access sub-account analytics

---

## Voice AI Selling Strategy

**Don't sell "Voice AI" directly** - businesses guard phone numbers

**Bundle approach:**
1. Database reactivation (low-hanging fruit)
2. Reputation management (Google reviews)
3. Conversational AI + Voice AI as bonus

**Sales pitch:**
- Deploy in 7 days (not 4 months)
- Answer 100% of calls
- Frees you to do real work
- Never makes mistakes
- Knows everything about your business

**Never mention:**
- "GoHighLevel"
- What bot/model it is
- Technical details

---

## Key Platform Features for Human Led AI

### Custom Values & Custom Fields
- Essential for scaling (use in templates)
- Can use in Voice AI initial message

### Knowledge Base
- Shared between Voice AI and Conversation AI
- Web crawl or FAQ entry
- File upload coming fall 2025

### Workflows/Automations
- Trigger from voice/conversation actions
- Full automation capabilities

### Calendars
- Native booking through AI agents
- Set up separate test calendar for demos

---

## Resources in Your NotebookLM

| Notebook | Focus |
|----------|-------|
| gohighlevel crm | 21 source tutorials |
| GoHighLevel Mastery | Beginner all-in-one guide |
| GoHighLevel Technical Core | Deep technical implementation |
| How To Generate Leads With GoHighLevel | Lead gen methods |
| How To Call Your Ad Leads Within 2 Minutes | Speed-to-lead |
| Building an AI Voice Agent Agency | $0-$15K roadmap |

---

## Your Human Led AI Application

**Target:** DFW contractors
**Services:**
1. Voice agents (missed call → booked appointment)
2. Lead generation
3. Workflow automation
4. AI-powered customer service

**GHL handles:**
- CRM for contractor clients
- Voice AI for after-hours/overflow
- SMS/WhatsApp follow-up
- Review management
- Appointment booking
