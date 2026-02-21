# FRANKIE 3.0 — BUILD STATUS
## Last Updated: February 14, 2026 8:00 AM Central

**This is the live status file. Update this as tasks complete. Do not create new planning docs.**

---

## PHASE 0: FOUNDATION

| Task | Code | Tested | Status |
|------|------|--------|--------|
| 0.1 Clean Supabase | ✅ | ✅ All 3 pass | DONE — 17 memories, library table exists, threshold 0.35 |
| 0.2 Wire memory files | ✅ | ⚠️ Logs confirmed, Telegram untested | CODE DONE — SOUL.md ✅ MEMORY.md ✅ daily logs ✅. Minor: tag says `<long_term_memory_file>` not `<long_term_memory>`. Needs Telegram test. |
| 0.3 Session history | ✅ | ⚠️ Logging added, untested in Telegram | CODE DONE — getHistory() wired to buildPrompt(). Needs "brother = Ryan" Telegram test. |
| 0.4 Memory write-back | ✅ | ❌ Biscuit test NOT run | CODE DONE — Claude CLI extraction + daily log append built. One extraction worked (Ryan). Full Biscuit test (learn → restart → cold recall) never executed. THIS IS THE MOST IMPORTANT TEST. |
| 0.5 Google auth | ❌ | ❌ | NOT STARTED — Requires Jay in browser for OAuth flows. Auth still split across two GCP projects. humanledai@gmail.com and jason@humanledai.net not authed. Biggest blocker for Phase 1. |
| 0.6 Disable Drive sync | ✅ | ⚠️ Untested (need 5 min log watch) | CODE DONE — startDriveSync() commented out in relay.ts. |

## BLOCKING ISSUES RIGHT NOW

1. **Frankie (Telegram bot) must be started in a SEPARATE terminal from Claude Code.** Claude Code sets a CLAUDECODE environment variable. Frankie's brain is `claude -p` which is a nested Claude session. Starting Frankie inside Claude Code = crash. Fix: open a new WSL terminal, run `cd ~/frankie-bot && unset CLAUDECODE && bun run src/relay.ts > /tmp/frankie-bot.log 2>&1 &`
2. **Google auth (0.5) requires Jay's browser.** Claude Code can prep code changes but Jay must run OAuth flows manually.

## TELEGRAM TESTS TO RUN (in order)

Start Frankie in separate terminal first:
```
cd ~/frankie-bot && unset CLAUDECODE && bun run src/relay.ts > /tmp/frankie-bot.log 2>&1 &
```

Then test in Telegram:

| # | Send This | Expected Answer | Pass? |
|---|-----------|----------------|-------|
| 0.2a | "What are my 12-month goals?" | Goals from SOUL.md (scale HLAI, quit Alacrity, build Frankie, master GHL) | ☐ |
| 0.2b | "Who is Patti Baker?" | GAIG account manager | ☐ |
| 0.2c | "What's my cat's name?" | Benso/Benson, tuxedo cat | ☐ |
| 0.3a | "My brother's name is Ryan" then "What's my brother's name?" | Ryan (same session) | ☐ |
| 0.4a | "Remember that my dog's name is Biscuit" | Confirms stored | ☐ |
| 0.4b | Kill bot, restart, send "What's my dog's name?" | Biscuit (cold recall) | ☐ |
| 0.6a | Watch logs 5 min: `tail -f /tmp/frankie-bot.log` | No ACCESS_TOKEN_SCOPE errors | ☐ |

## WHAT'S PARTIALLY BUILT (Phase 1 head starts)

- Goals table schema exists in setup.sql
- Morning brief already fires at 5:30 AM, already queries goals — just needs auto-task generation
- Google API email/calendar functions work for personal account — multi-account routing not built
- SKILL-INDEX.json exists with 23 skills + triggers — just needs wiring into claude-bridge.ts
- Discord bot: NOTHING built
- Heartbeat runner: NOTHING built

## KNOWN DRIFT FROM PRD

- 0.2: XML tag is `<long_term_memory_file>` instead of `<long_term_memory>` — minor, functional
- 0.4: PRD says extraction prompt returns JSON with [{content, category}] — verify Claude Code built it that way

## NEXT ACTIONS (in order)

1. Start Frankie in separate terminal (not Claude Code)
2. Run all 7 Telegram tests above
3. If tests pass → mark Phase 0 tasks as tested
4. Run Biscuit test (the big one)
5. Prep code for 0.5 Google auth (Claude Code can do this)
6. Jay runs OAuth flows in browser
7. Test all 3 accounts
8. Phase 0 gate check → sign off
9. Begin Phase 1

---

*Do not create new planning documents. Update THIS file.*
