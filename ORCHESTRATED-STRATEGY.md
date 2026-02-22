# Orchestrated Cost Strategy — Best of All Worlds

## The Game Plan
**Use ALL the free/cheap options, preserve Claude for critical work only.**

## Tiered Strategy:

### Tier 1: FREE Models (Primary Usage 80%)
- **NVIDIA Kimi K2.5** — 1T params, multimodal, 2M context, COMPLETELY FREE
- **Gemini 2.0 Flash** — FREE with rate limits
- **Groq Llama 3.3 70B** — FREE tier (30 req/min)
- **Ollama Qwen 3.8B** — Local, offline, FREE

### Tier 2: OpenAI Subscription (Secondary 15%)  
- **FLAT $20/month** instead of per-token costs
- Use ChatGPT Plus subscription with `openclaw auth openai codex`
- **GPT-4o** and **GPT-4o Mini** available
- Confirmed OK by Sam Altman per OpenClaw founder

### Tier 3: Claude API (Emergency Only 5%)
- **Only for critical reasoning** when free models fail
- **Only for final review/polish** of important work
- Keep Opus for `/reasoning` mode only

## Cost Breakdown:
| Model/Service | Monthly Cost | Usage % | 
|---------------|--------------|---------|
| NVIDIA Kimi K2.5 | $0 | 60% |
| Gemini Flash | $0 | 20% |  
| OpenAI Subscription | $20 | 15% |
| Claude API | ~$50 | 5% |
| **TOTAL** | **$70/month** | vs **$2,700/month** current |

## Fallback Chain:
1. **NVIDIA Kimi** → 2. **Gemini Flash** → 3. **OpenAI Subscription** → 4. **Claude API**

**97% cost reduction while preserving Claude quality when you need it.**