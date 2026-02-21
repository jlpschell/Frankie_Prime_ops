---
name: step-by-step-guide
description: >
  IKEA-style step-by-step task guide for presenting instructions to Jay.
  Use this skill whenever a task requires action from Jay (terminal commands,
  browser steps, file downloads, approvals) or involves coordinated work between
  Frankie and Jay. Triggers include: setup procedures, deployment steps, config
  changes, troubleshooting walkthroughs, multi-step installations, any task where
  Jay needs to do something in a specific order, or when Jay asks "how do I do this"
  or "walk me through it." Also use when explaining what Frankie is about to do
  automatically so Jay can follow along. Do NOT use for simple Q&A, single-command
  answers, or tasks Frankie handles entirely on his own without Jay's involvement.
---

# Step-by-Step Guide Skill

Present every multi-step task as a clear, numbered walkthrough. Each step shows WHO does it, WHAT to do, and WHY (one sentence max).

## Step Format

Every step uses one of these role tags:

```
🧑 JAY — Something Jay does manually (terminal, browser, approval)
🦍 FRANKIE — Something Frankie handles automatically
⏸️ CHECKPOINT — One side needs the other before continuing
⚠️ WARNING — Something that can go wrong if skipped
✅ DONE — Confirmation that a phase is complete
```

## Rules

1. **One action per step.** Never combine "do X and then Y" into one step.
2. **Terminal commands get their own code block.** Always copy-paste ready. Never make Jay type freehand.
3. **Say what success looks like.** After any command, tell Jay what output to expect.
4. **WHY in one sentence.** Jay learns the process, but explanations don't bloat the guide.
5. **No jargon without a plain English parenthetical.** Example: "sandbox (the safety container that isolates Frankie's tools)"
6. **Number every step sequentially.** No sub-steps like 3a, 3b. If it needs sub-steps, it's multiple steps.
7. **Group steps into phases** with a short title when there are more than 5 steps.
8. **If a step can fail, say what failure looks like** and what to do about it in the same step.

## Example Output

```
## Phase 1: Backup (Safety Net)

**Step 1** 🧑 JAY
Run this in your WSL terminal to save a copy of your current config:
    cp ~/.openclaw/openclaw.json ~/.openclaw/backups/openclaw_backup.json
**Why:** If anything breaks, you paste this file back and you're exactly where you started.

**Step 2** ⏸️ CHECKPOINT
Confirm the backup exists:
    ls ~/.openclaw/backups/
You should see: `openclaw_backup.json` in the list.
If you don't see it → the copy failed. Re-run Step 1.

## Phase 2: Deploy

**Step 3** 🦍 FRANKIE
I'm updating the config to add sandbox security settings.
**Why:** This puts all of my tool usage inside a safety container so I can't accidentally modify your files.

**Step 4** 🧑 JAY
Restart the gateway so the new config takes effect:
    openclaw gateway
**What success looks like:** You see "Health OK" and no red error text.
**If it fails:** Run `cat ~/.openclaw/openclaw.json` and paste the output — I'll find the problem.

**Step 5** ✅ DONE
Config is hardened. Frankie is running with sandbox protection.
```

## When to Use Phases

- **5 or fewer steps** → No phases needed, just numbered steps
- **6-12 steps** → Group into 2-3 phases
- **13+ steps** → Group into logical phases, add a summary at the top listing all phases

## Summary Block (For Long Guides)

When a guide has 3+ phases, start with:

```
## What We're Doing
1. **Backup** — Save current state (2 steps)
2. **Deploy Files** — Copy new files into workspace (3 steps)  
3. **Verify** — Make sure everything works (2 steps)
Total: ~5 minutes
```

## Adapting to Context

- **Jay is in a hurry:** Skip the WHY lines. Just steps and commands.
- **Jay asks "why":** Expand the WHY into 2-3 sentences for that specific step.
- **Something failed:** Switch to troubleshooting mode — show the diagnostic command, what to look for, and the fix, each as separate steps.
- **Jay says "just tell me what to paste":** Strip to bare commands only, one per step, no explanation.
