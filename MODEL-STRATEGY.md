# Model Cost Strategy — Token Conservation

## Current Spend Problem
- Opus 4-6: $5/1M input, $25/1M output → BLEEDING MONEY
- Sonnet 4-5: $3/1M input, $15/1M output → Still expensive  
- Loading full workspace context every message = 20k+ tokens = $0.10+ per exchange

## Tiered Model Strategy

### Tier 1: Free/Ultra-Cheap (Daily Tasks)
**Use for:** Heartbeats, simple Q&A, file operations, memory search, basic coding

**Models to add:**
- **Gemini 2.0 Flash** (FREE up to 2M tokens/min) — `google/gemini-2.0-flash`
- **Ollama Qwen 3.5** (FREE, local) — `ollama/qwen2.5:7b`
- **Groq Llama 3.3 70B** (FREE tier: 30 req/min) — `groq/llama-3.3-70b`
- **OpenAI GPT-4o Mini** ($0.15/1M input, $0.60/1M output) — `openai/gpt-4o-mini`

### Tier 2: Moderate Cost (Complex Tasks)
**Use for:** Content generation, code reviews, planning, analysis

**Models to add:**
- **OpenAI GPT-4o** ($2.50/1M input, $10/1M output) — `openai/gpt-4o`
- **Gemini 1.5 Pro** ($1.25/1M input, $5/1M output) — `google/gemini-1.5-pro`

### Tier 3: Premium (Only When Needed)
**Use for:** Complex reasoning, critical decisions, quality review

**Keep:**
- **Claude Sonnet 4-5** ($3/1M input, $15/1M output) — current fallback
- **Claude Opus 4-6** ($5/1M input, $25/1M output) — only for `/reasoning` or explicit requests

## Context Loading Rules (ENFORCED)

### Default Behavior:
- **NO auto-loading** workspace files
- **Memory-first** — always search memory before loading files
- **Surgical loading** — only what's needed for the specific task
- **Token budgets** — enforce limits by task type

### Task Type Budgets:
| Task | Max Context | Model | Rationale |
|------|-------------|-------|-----------|
| Heartbeat | 2k tokens | Gemini Flash | Status check only |
| Simple Q&A | 5k tokens | GPT-4o Mini | Quick responses |
| Memory recall | 20k tokens | Gemini 1.5 Pro | Search + retrieval |
| Complex tasks | 50k tokens | GPT-4o or Sonnet | Build/analyze |
| Reasoning | Full context | Opus | Only when explicitly needed |

## Implementation Plan

1. **Add model configs** to OpenClaw models.json
2. **Set Gemini Flash as default** for routine operations
3. **Create model selection logic** based on task type
4. **Add Ollama local models** for offline/free processing
5. **Monitor usage** with cost tracking

Want me to implement this config now?