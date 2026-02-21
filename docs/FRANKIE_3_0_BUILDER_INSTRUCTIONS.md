# FRANKIE 3.0 — BUILDER INSTRUCTIONS
## How To Build This PRD (Read Before Touching Code)

**This file accompanies FRANKIE_3_0_PRD_FINAL.md**
**Read both. PRD = what to build. This file = how to build it.**

---

## MANDATORY SKILLS — USE ON EVERY TASK

### 1. continuity-check (EVERY response)
Before writing ANY code or making ANY change:
- Check: Have I already done this?
- Check: Did Jay already answer what I'm about to ask?
- Check: Am I planning again when I should be executing?
- Check: Is my response concise or am I padding?
- If you've provided the same deliverable twice, STOP. Reference the earlier version.
- After 2 planning documents, DEFAULT TO ACTION. No more plans.

### 2. compound-engineering (EVERY Phase 0/1/2 task)
Every numbered task in the PRD follows this loop:
1. **Plan** — Read the task. State what you're going to do in 3-5 bullet points. Get Jay's OK.
2. **Work** — Execute the plan. Write the code. Run the commands.
3. **Review** — Run the test listed in the PRD for that task. Show Jay the result.
4. **Compound** — Log what you learned. If something broke, note WHY so it doesn't repeat.

Do NOT skip Plan. Do NOT skip Review. The test must PASS before moving to the next task.

---

## SKILL-TO-TASK MAPPING

### Phase 0: Foundation

| Task | Skills To Use | How |
|------|--------------|-----|
| 0.1 Clean Supabase | compound-engineering | Plan the SQL → Execute → Review row count → Log |
| 0.2 Wire memory files into Telegram | compound-engineering | Plan the claude-bridge.ts changes → Build → Test with "Who is Benso?" → Log |
| 0.3 Session history | compound-engineering | Read existing code → Verify or fix → Test "brother = Ryan" → Log |
| 0.4 Memory write-back | compound-engineering | Plan extraction step → Build → Run Biscuit Test → Log |
| 0.5 Google auth | compound-engineering + dev-browser | Plan scope consolidation → Use dev-browser if OAuth flow needs browser → Test each account → Log |
| 0.6 Disable old Drive sync | compound-engineering | Find the code → Disable → Watch logs 5 min → Log |

### Phase 1: Frankie Works Alone

| Task | Skills To Use | How |
|------|--------------|-----|
| 1.1 Discord bot | compound-engineering | Plan Discord.js setup → Build transport layer → Test message/response → Log |
| 1.2 Skill auto-discovery | compound-engineering | Plan index.json loading in claude-bridge.ts → Build → Test cold email trigger → Log |
| 1.3 Goal system | compound-engineering | Plan Supabase table + /goal command → Build → Test store/retrieve → Log |
| 1.4 Auto-task generation | compound-engineering | Plan morning-brief.ts changes → Build → Test 4-task output → Log |
| 1.5 Heartbeat runner | compound-engineering + doe-automation-builder | Use DOE framework to design the heartbeat as an agentic workflow. Directive = HEARTBEAT.md checklist. Orchestration = 30-min schedule + data gathering. Execution = alert or stay silent. |
| 1.6 Email management | compound-engineering | Plan multi-account email functions → Build → Test read/draft/send → Log |
| 1.7 Calendar | compound-engineering | Plan calendar functions → Build → Test read/create → Log |

### Phase 2: Frankie Delegates

| Task | Skills To Use | How |
|------|--------------|-----|
| 2.1 Sub-agent architecture | compound-engineering + doe-automation-builder | Use DOE for each sub-agent: Directive = SKILL.md, Orchestration = manager routing, Execution = claude -p call with timeout |
| 2.2 GHL integration | compound-engineering + sales-pipeline-analyzer | Use sales-pipeline-analyzer to understand pipeline data patterns. Build GHL API functions with compound loop. |
| 2.3 Dashboard | compound-engineering + dev-browser | Build NextJS app with compound loop. Use dev-browser to verify each page renders correctly. |
| 2.4 GitHub | compound-engineering | Plan git commands → Build /commit and /diff handlers → Test → Log |

---

## RALPH — AUTONOMOUS EXECUTION (OPTIONAL BUT POWERFUL)

The PRD can be converted to Ralph's prd.json format. This lets Frankie execute tasks autonomously in sequence without Jay pasting prompts between each one.

**When to use Ralph:**
- Phase 0 tasks 0.1-0.3 are straightforward and can run autonomously
- Phase 0 tasks 0.4-0.5 need Jay's involvement (Biscuit Test, OAuth browser flow) — don't Ralph these

**How:**
1. After reading the PRD, run: "Convert Phase 0 tasks 0.1 through 0.3 into Ralph prd.json format"
2. Ralph will create a structured task list Frankie can execute in sequence
3. Tasks requiring Jay's input get flagged as manual checkpoints

---

## EXECUTION RULES

1. **One task at a time.** Finish 0.1 before starting 0.2. No parallel work.
2. **Show the test result.** Every task in the PRD has a TEST table. Run the test. Show Jay the output. Pass or fail — no "I think it works."
3. **If a test fails, fix it before moving on.** Do not skip to the next task hoping it resolves itself.
4. **Log every task completion.** Append to workspace/memory/YYYY-MM-DD.md:
   ```
   - [HH:MM] Phase 0.1 COMPLETE — Supabase cleaned: 17 memories, library table created, threshold set to 0.35
   ```
5. **If you don't know, say so.** Don't fabricate "I fixed it." Jay will verify. Trust but verify is a non-negotiable rule.
6. **Read files before claiming they exist or don't exist.** Use ls and head. Don't guess.

---

## LAUNCH SEQUENCE

When Jay gives you the go-ahead:

1. Read workspace/FRANKIE_3_0_PRD_FINAL.md (the full PRD)
2. Read this file (builder instructions)
3. Start Phase 0, Task 0.1
4. Follow the compound-engineering loop: Plan → Work → Review → Compound
5. Show Jay each test result before moving to the next task
6. Do not skip ahead. Do not plan Phase 1 until Phase 0 gate check passes.

---

*Builder Instructions v1.0 — February 13, 2026*
