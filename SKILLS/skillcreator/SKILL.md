---
name: skill-factory
description: Creates new agent skills from scratch. Use when user says "create a skill", "new skill", "build skill for X", or when a repeatable workflow should be codified as a skill.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Skill Factory

> Turn any workflow, pattern, or expertise into a reusable skill

## When to Use This Skill

- User explicitly asks for a new skill
- You identify a repeatable pattern worth capturing
- User describes a workflow they do often
- A domain needs structured instructions

---

## Skill Creation Workflow

### Step 1: Gather Requirements

Ask these questions (or infer from context):

```markdown
## Skill Spec
- **Name**: [kebab-case, gerund preferred: "testing-apis", "managing-servers"]
- **Purpose**: [One sentence: what problem does this solve?]
- **Triggers**: [Keywords that activate this skill]
- **Inputs**: [What does the agent need to start?]
- **Outputs**: [What should the agent produce?]
- **Tools needed**: [Read, Write, Bash, Glob, Grep, etc.]
```

### Step 2: Analyze Existing Skills

Before creating, scan for similar skills to avoid duplication:

```bash
ls -la /home/plotting1/frankie-bot/workspace/agent-skills/
```

Read 2-3 well-structured skills as templates:
- `parallel-agents/SKILL.md` — complex orchestration
- `systematic-debugging/SKILL.md` — process-driven
- `api-patterns/SKILL.md` — reference patterns

### Step 3: Generate the Skill

Create the folder structure:

```
agent-skills/
└── [skill-name]/
    ├── SKILL.md          # Required: Main instructions
    ├── resources/        # Optional: Templates, configs
    ├── scripts/          # Optional: Helper scripts
    └── examples/         # Optional: Reference implementations
```

### Step 4: Write SKILL.md

Follow this structure **exactly**:

```markdown
---
name: [skill-name]
description: [Third-person description with trigger keywords. Max 1024 chars.]
allowed-tools: [List of tools this skill needs]
---

# [Skill Title]

> [One-line tagline explaining the value]

## When to Use This Skill

✅ **Good for:**
- [Situation 1]
- [Situation 2]

❌ **Not for:**
- [Anti-pattern 1]
- [Anti-pattern 2]

---

## Workflow

[Step-by-step process with checkboxes]

```markdown
## Checklist
- [ ] Step 1
- [ ] Step 2
- [ ] Verify result
```

## Instructions

[The actual meat — commands, patterns, templates]

## Resources

[Links to supporting files in resources/, scripts/, examples/]
```

---

## Quality Standards

### Naming
- Folder: `kebab-case` (e.g., `api-testing`)
- File: `SKILL.md` (uppercase)
- name field: gerund form (`testing-apis` not `test-api`)

### Length
- SKILL.md: Under 500 lines
- If longer, split into `resources/ADVANCED.md`

### Clarity
- Assume the agent is smart — don't explain basics
- Include concrete examples, not abstract descriptions
- Use tables for options/comparisons
- Use code blocks for commands/templates

### Verification
After creating, run these checks:

```bash
# Verify file exists and is named correctly
ls -la agent-skills/[skill-name]/SKILL.md

# Check frontmatter is valid
head -20 agent-skills/[skill-name]/SKILL.md

# Ensure no duplicate skill names
grep -l "name: [skill-name]" agent-skills/*/SKILL.md
```

---

## Quick Templates

### Process Skill (step-by-step workflow)
Best for: debugging, deployment, review processes

### Reference Skill (patterns library)
Best for: API patterns, coding standards, design patterns

### Orchestration Skill (multi-agent coordination)
Best for: complex analysis, comprehensive reviews

### Tool Skill (wrapper for external tool)
Best for: CLI tools, integrations, scripts

---

## Output Format

When creating a skill, output:

1. **Folder path**: `agent-skills/[skill-name]/`
2. **SKILL.md content**: Full markdown
3. **Resource files** (if any): Templates, scripts
4. **Verification**: Commands run and results

---

## Anti-Patterns

❌ Writing generic instructions (be specific)
❌ Filename `skill.md` (must be `SKILL.md`)
❌ Missing frontmatter
❌ No trigger keywords in description
❌ Over 500 lines without splitting
❌ Explaining obvious concepts
❌ No verification step

---

## Example: Creating a "code-review" Skill

**User says**: "Create a skill for doing code reviews"

**Agent does**:
1. Creates `agent-skills/code-review/`
2. Writes `SKILL.md` with:
   - Frontmatter with triggers: "review", "PR", "pull request"
   - Checklist for security, performance, maintainability
   - Code examples for common issues
   - Output format for review comments
3. Creates `resources/review-checklist.md`
4. Verifies with `ls` and `head` commands
5. Reports completion

---

## Skill Library Location

All skills live in:
```
/home/plotting1/frankie-bot/workspace/agent-skills/
```

Current count: 25+ skills across dev, AI, content, and business domains.
