---
name: doe-automation-builder
description: Build agentic AI workflows using the DOE (Directive, Orchestration, Execution) framework. Use when users want to automate repetitive business tasks, solve workflow bottlenecks, or create AI-powered solutions without traditional coding. Handles full lifecycle from problem analysis through cloud deployment using Anti-gravity IDE, Claude Sonnet 4.5, and Modal. Best for multi-step automations involving APIs, data processing, content generation, or scheduled tasks.
---

# DOE Automation Builder

This skill guides you through building automated workflows using the DOE (Directive, Orchestration, Execution) framework - a method for creating AI-powered automations using natural language as "universal translation" instead of traditional coding.

## Core Philosophy

**The Three Layers:**
1. **Directive (General)**: You provide instructions in plain English - the "what" and "why"
2. **Orchestration (Colonel)**: Claude acts as project manager - decides tactics, handles errors, asks clarifying questions
3. **Execution (Soldier)**: Python scripts do deterministic work - API calls, data processing, no hallucinations

**Why This Works:**
Natural language instructions are flexible and maintainable. When requirements change, you update the directive, not code. The AI translates your intent into reliable execution.

## When to Use This Skill

Trigger this skill when you need to:
- Automate repetitive business tasks or manual workflows
- Solve workflow bottlenecks or time-consuming processes
- Build multi-step automations involving multiple APIs or data sources
- Create content generation pipelines (like social media, reports, videos)
- Deploy automated tasks that run on schedules or triggers

**Example Use Cases:**
- Scanning LinkedIn/X for AI news → generating video scripts → creating HeyGen avatars
- Processing insurance claims data → flagging priorities → assigning work
- Monitoring stock prices → analyzing conditions → sending alerts
- Scraping content → transforming data → publishing to multiple platforms

## Step 1: Problem Intake & Analysis

Start by understanding the problem through conversation. Ask probing questions to uncover:

**Core Questions:**
1. "What task are you trying to automate?"
2. "What triggers this task? (schedule, event, manual start)"
3. "What's the input data and where does it come from?"
4. "What's the desired output and where does it go?"
5. "How do you know when it's done correctly?"

**Listen for:**
- Repetitive manual steps ("I do this every day...")
- Multiple tools/platforms involved ("I copy from X to Y...")
- Time-sensitive operations ("I need to check every hour...")
- Quality bottlenecks ("This takes too long to do manually...")

**Your Job:**
Translate messy problem descriptions into structured thinking. Example:

*User says:* "I need to find trending AI posts on LinkedIn and make videos about them"

*You clarify:*
- Input: LinkedIn posts tagged with certain hashtags
- Process: Extract post content → summarize → write script → generate video
- Output: 30-45 second video files ready for posting
- Trigger: Run daily at 6am
- Success criteria: 3-5 relevant videos, scripts under 100 words, factually accurate

## Step 2: Environment Setup

Guide setup of the Anti-gravity IDE workspace with proper DOE structure.

**Initial Setup Checklist:**

```
Project Root/
├── directives/          # Natural language SOPs (you write these)
│   └── [task-name].md
├── execution/           # Python scripts (Claude writes these)
│   └── [task-name].py
├── .tmp/               # Temporary files and data
├── .env                # API keys and secrets
└── agents.md           # Claude's education file (system prompt)
```

**Step-by-step instructions:**

1. **Open Anti-gravity** and create new project folder
2. **Create the education file** (`agents.md`):
   - Explain DOE framework to future Claude instances
   - Include operating principles
   - Reference this skill for procedural knowledge

3. **Create directory structure**:
   - Make `directives/`, `execution/`, and `.tmp/` folders
   - Initialize `.env` file for credentials

4. **Setup credentials**:
   - Identify which APIs the automation will use
   - Obtain API keys (guide through this process)
   - Store securely in `.env` with proper variable names

See `references/environment-setup.md` for detailed Anti-gravity configuration examples.

## Step 3: Writing Directives

Help the user write clear, comprehensive SOPs in natural language. These go in `directives/[task-name].md`.

**Directive Template Structure:**

```markdown
# [Task Name] Automation

## Objective
[One sentence: what should this accomplish?]

## Input Requirements
- Data source: [where data comes from]
- Format: [JSON, CSV, API response, etc.]
- Required fields: [list the necessary data points]

## Process Steps
1. [First step in plain English]
   - Sub-detail if needed
2. [Second step]
3. [Continue...]

## Quality Criteria (Definition of Done)
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2
- [ ] Criterion 3

## Error Handling
- If [condition], then [action]
- Common failure modes: [list potential issues]

## Output Specification
- Format: [file type, API destination, etc.]
- Location: [where it should be saved/sent]
- Naming convention: [how to name output files]
```

**Writing Guidelines:**

- **Be specific about data**: Don't say "get posts" - say "get posts from last 24 hours with >100 likes"
- **Include examples**: Show sample input and expected output
- **Define quality**: How do you grade success? What makes output "good enough"?
- **Anticipate failures**: What could go wrong? How should it recover?

**Voice-to-Directive Workflow:**

Since speaking is 3-5x faster than typing, encourage voice input:
1. User describes task verbally (use voice transcription)
2. You convert raw transcript into structured directive
3. User reviews and refines
4. Save to `directives/[task-name].md`

See `references/directive-examples.md` for complete real-world examples.

## Step 4: Building Execution Scripts

Once the directive is clear, guide Claude (that's you!) to write the Python scripts in `execution/`.

**Script Generation Process:**

1. **Analyze the directive** - Break down into discrete functions
2. **Identify tools needed** - Which APIs, libraries, data formats?
3. **Design modular structure** - Separate concerns, reusable functions
4. **Write deterministic code** - No AI guessing in execution layer

**Code Structure Pattern:**

```python
# execution/[task-name].py
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment
API_KEY = os.getenv('API_KEY')

def fetch_data(source, filters):
    """Deterministic data retrieval"""
    # No AI inference here - pure API calls
    pass

def transform_data(raw_data, rules):
    """Deterministic transformation"""
    # Follow explicit rules from directive
    pass

def validate_output(data, criteria):
    """Check against quality criteria"""
    # Return True/False based on directive's definition of done
    pass

def main():
    """Orchestrate the workflow"""
    # Step 1: Fetch
    raw = fetch_data(...)
    
    # Step 2: Transform
    processed = transform_data(raw, ...)
    
    # Step 3: Validate
    if validate_output(processed, ...):
        # Step 4: Save/Send
        deliver_output(processed)
    else:
        handle_failure()

if __name__ == "__main__":
    main()
```

**Key Principles:**

- **No hallucinations**: Use exact API specifications, don't guess endpoints
- **Error handling**: Try/except blocks with informative messages
- **Logging**: Print progress so user can debug
- **Configuration**: Use .env for secrets, never hardcode

**Testing Workflow:**

1. Run script locally in Anti-gravity terminal
2. Verify outputs match directive's success criteria
3. Test edge cases and error conditions
4. Iterate until reliable

## Step 5: Self-Annealing (Error Recovery)

Build self-healing capability into the workflow. When scripts fail, they should fix themselves.

**Self-Annealing Loop:**

```
1. Script encounters error
   ↓
2. Script logs detailed error message
   ↓
3. Claude reads error log
   ↓
4. Claude diagnoses root cause
   ↓
5. Claude updates execution script
   ↓
6. Claude updates directive (if needed) to prevent recurrence
   ↓
7. Rerun with fixes
```

**Implementation Pattern:**

Add to execution scripts:

```python
def handle_error(error, context):
    """Log detailed error for Claude to diagnose"""
    error_log = {
        'timestamp': datetime.now(),
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context,
        'stack_trace': traceback.format_exc()
    }
    
    # Save to .tmp/errors.json
    with open('.tmp/errors.json', 'a') as f:
        json.dump(error_log, f)
        f.write('\n')
    
    # Notify user
    print(f"Error logged. Ask Claude to diagnose .tmp/errors.json")
```

**Diagnostic Process:**

When user says "the script failed":
1. Read `.tmp/errors.json`
2. Identify root cause (API changed? Bad data? Missing credential?)
3. Fix execution script
4. Update directive if architectural change needed
5. Re-run and verify fix

**Common Failure Patterns:**

- API rate limits → Add retry with exponential backoff
- Data format changes → Update parsing logic
- Missing edge cases → Add validation and handling
- Credential expiry → Add refresh token logic

## Step 6: Modal Deployment (Cloudifying)

Once the workflow is stable locally, deploy to Modal for automated execution.

**When to Deploy:**

- Workflow runs reliably 3+ times without errors
- All edge cases are handled
- User wants scheduled or triggered execution

**Modal Setup Process:**

1. **Install Modal CLI**:
   ```bash
   pip install modal
   modal setup
   ```

2. **Convert script to Modal function**:
   - Add Modal decorators
   - Define schedule or webhook trigger
   - Specify secrets and dependencies

3. **Deploy and test**:
   - Deploy to Modal cloud
   - Test with sample trigger
   - Monitor logs

See `references/modal-deployment.md` for complete deployment patterns and examples.

**Deployment Checklist:**

- [ ] Script runs locally without errors
- [ ] All credentials in .env
- [ ] Edge cases handled
- [ ] Logging implemented
- [ ] Modal account setup
- [ ] Dependencies listed
- [ ] Schedule or trigger defined
- [ ] Deployed and tested
- [ ] Monitoring configured

## Common Automation Patterns

**Content Generation Pipeline:**
1. Scan source (social media, news, RSS)
2. Filter/rank by relevance
3. Transform to target format (script, summary, video)
4. Generate assets (images, audio, video)
5. Publish or queue for review

**Data Processing Workflow:**
1. Extract from source (API, database, file)
2. Transform (clean, enrich, calculate)
3. Validate (check quality criteria)
4. Load to destination (database, sheet, notification)

**Monitoring & Alerting:**
1. Check condition (price, metric, status)
2. Compare against thresholds
3. Take action if triggered (alert, trade, escalate)
4. Log for historical tracking

**Multi-Platform Sync:**
1. Pull from source of truth
2. Transform to each platform's format
3. Push to destinations
4. Verify delivery
5. Handle conflicts/failures

## Troubleshooting Guide

**"Claude isn't understanding my directive"**
- Add concrete examples of input/output
- Break complex steps into smaller sub-steps
- Define ambiguous terms explicitly

**"The execution script keeps failing"**
- Check API credentials in .env
- Verify API endpoint URLs and parameters
- Add debug logging to see where it breaks
- Test each function independently

**"Output quality is inconsistent"**
- Tighten quality criteria in directive
- Add validation checks in execution script
- Use deterministic transformations, not AI generation in execution layer
- Review edge cases in test data

**"It works locally but not in Modal"**
- Verify all dependencies listed in Modal config
- Check secrets are configured in Modal dashboard
- Review Modal logs for specific error
- Test with minimal example first

## Success Metrics

Track these to measure automation effectiveness:

- **Time saved**: Manual time - automated time
- **Error rate**: Failed runs / total runs
- **Quality score**: Outputs meeting criteria / total outputs
- **Maintenance burden**: Hours spent fixing / month
- **ROI**: Value created / setup + maintenance cost

## Next Steps After Building

1. **Document the automation**: Update directive with lessons learned
2. **Monitor performance**: Set up alerts for failures
3. **Iterate improvements**: Refine based on real usage
4. **Scale or replicate**: Apply DOE pattern to new tasks

## Philosophy Reminder

The DOE framework succeeds because it separates concerns:
- **You** provide domain knowledge and business logic (Directive)
- **Claude** handles decision-making and adaptation (Orchestration)  
- **Python** executes reliably and deterministically (Execution)

Natural language becomes the interface between human intent and machine execution. When you need to change behavior, update the directive in English, not code.
