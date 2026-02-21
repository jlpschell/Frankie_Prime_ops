# Gmail Filters Setup — Manual Instructions

**Created:** 2026-02-20 9:15 PM  
**Purpose:** Auto-label your 18 saved domains so they stay organized and don't get trashed

---

## How to Create Filters

1. Go to Gmail → Settings (gear icon) → "See all settings"
2. Click "Filters and Blocked Addresses"
3. Click "Create a new filter"
4. For each filter below:
   - Paste the "From" criteria
   - Click "Create filter"
   - Check "Apply the label" → select/create the label
   - Check "Skip the Inbox (Archive it)" if you want it out of inbox
   - Click "Create filter"

---

## Filter 1: AI Services

**From:** `anthropic.com OR openai.com OR groq.co OR claude.com OR heygen.com OR earlyaidopterscommunity.com OR firstmovers.ai`

**Action:**
- Apply label: **AI**
- Skip inbox: ❌ No (keep these visible)

**Why:** Important AI service emails, product updates, billing

---

## Filter 2: Financial/Banking

**From:** `pennymac.com OR texanscu.org OR cash.app`

**Action:**
- Apply label: **Bills**
- Skip inbox: ❌ No (need to see these)

**Why:** Mortgage, credit union, payments

---

## Filter 3: Health/Medical

**From:** `cignahealthcare.com OR express-scripts.com`

**Action:**
- Apply label: **Health**
- Skip inbox: ✅ Yes (archive, check when needed)

**Why:** Insurance, prescriptions

---

## Filter 4: Tech Services

**From:** `hostinger.com OR clean.email OR ccstrategic.io OR ccsend.com`

**Action:**
- Apply label: **Tech/Services**
- Skip inbox: ✅ Yes (not urgent)

**Why:** Hosting, email tools, newsletters

---

## Filter 5: Misc Keep

**From:** `att-mail.com OR audible.com OR elegoo.com OR openclassactions.com`

**Action:**
- Apply label: **Misc**
- Skip inbox: ✅ Yes (low priority)

**Why:** Telecom, audiobooks, 3D printing, class actions

---

## What This Does

✅ **Keeps your inbox clean** — only urgent stuff stays  
✅ **Nothing gets lost** — everything is labeled and searchable  
✅ **Weekly cleanup works** — these domains are auto-protected from trash  

---

## Already Auto-Protected

These are NEVER touched by the cleanup script (even without filters):

- `google.com`, `gmail.com`
- `skool.com`
- `customercenter.net`, `supabase.com`, `stripe.com`, `x.ai`
- `experian.com`, `northwestregisteredagent.com`
- Any **starred** emails

---

**Next time:** If you add more domains to save, update `/tmp/your_unsub_list.txt` to exclude them.
