# OpenClaw Reference — Frankie Prime Operations Guide

Last updated: 2026-02-18

---

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Config Structure](#config-structure)
- [Update Process](#update-process)
- [Workspace Safety](#workspace-safety)
- [Telegram Config](#telegram-config)
- [Discord Config](#discord-config)
- [Heartbeat System](#heartbeat-system)
- [Cron Jobs](#cron-jobs)
- [Memory System](#memory-system)
- [Session Management](#session-management)
- [Skills System](#skills-system)
- [Key CLI Commands](#key-cli-commands)
- [Common Troubleshooting](#common-troubleshooting)

---

## Architecture Overview

OpenClaw is a single **Gateway daemon** that owns all messaging channels and agent logic.

**How it works:**
- One long-lived Gateway process runs on the host (our Dell/WSL2 box)
- It connects to Telegram, Discord, WhatsApp, etc. via their respective APIs
- Clients (CLI, web UI, macOS app) connect to the Gateway over **WebSocket** on port `18789` (default)
- **Nodes** (phones, other machines) also connect via WebSocket with `role: node`
- The Gateway is the single source of truth for sessions, config, and state

**Key paths on disk:**
| What | Where |
|------|-------|
| Config | `~/.openclaw/openclaw.json` |
| Credentials | `~/.openclaw/credentials/` |
| Sessions | `~/.openclaw/agents/<agentId>/sessions/` |
| Cron jobs | `~/.openclaw/cron/jobs.json` |
| Workspace | `~/.openclaw/workspace` (our working dir) |
| Skills (managed) | `~/.openclaw/skills/` |
| Skills (workspace) | `~/.openclaw/workspace/skills/` |
| Memory DB | `~/.openclaw/memory/<agentId>.sqlite` |

**Wire protocol:** WebSocket, JSON text frames. First frame must be `connect`. Auth token required for non-loopback connections.

---

## Config Structure

Config lives at `~/.openclaw/openclaw.json` (JSON5 format — comments and trailing commas OK).

### Config Hot Reload
The Gateway watches the config file and auto-applies most changes. Default mode is `hybrid`:
- **Hot-applies without restart:** channels, agents, models, hooks, cron, heartbeat, sessions, tools, browser, skills, UI, logging
- **Requires restart:** `gateway.*` (port, bind, auth, TLS), `discovery`, `canvasHost`, `plugins`

In `hybrid` mode, restart-required changes are handled automatically.

### Editing Config
- `openclaw config get <path>` — read a value
- `openclaw config set <path> <value>` — write a value
- `openclaw configure` — interactive wizard
- Direct edit `~/.openclaw/openclaw.json` — auto-detected via file watcher
- Control UI at `http://127.0.0.1:18789` has a Config tab

### Strict Validation
Config must match the schema exactly. Unknown keys = Gateway refuses to start. Run `openclaw doctor` to diagnose, `openclaw doctor --fix` to repair.

### Config Includes
Split large configs with `$include`:
```json5
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
}
```

### Environment Variables
Loaded from: process env > `~/.openclaw/.env` > CWD `.env`. Inline env vars in config via `env: { KEY: "value" }`. Reference env vars in config strings: `"${VAR_NAME}"`.

---

## Update Process

### What Changes During an Update
- **REPLACED:** The OpenClaw package code (npm module or git source)
- **NOT TOUCHED:** `~/.openclaw/openclaw.json`, `~/.openclaw/credentials/`, `~/.openclaw/workspace/`, `~/.openclaw/agents/*/sessions/`, `~/.openclaw/cron/`
- **Config migrations** may be applied by `openclaw doctor` (deprecated keys renamed, etc.)

### How to Update

**Preferred method (re-run installer):**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
# Add --no-onboard to skip the wizard
```

**Global npm install:**
```bash
npm i -g openclaw@latest
openclaw doctor
openclaw gateway restart
openclaw health
```

**From source:**
```bash
openclaw update
# Or manually: git pull && pnpm install && pnpm build && openclaw doctor
```

### Post-Update Checklist
1. `openclaw doctor` — migrate config, check health
2. `openclaw gateway restart` — restart the daemon
3. `openclaw health` — verify everything is running

### Rollback
```bash
# Pin to a specific version
npm i -g openclaw@<version>
openclaw doctor
openclaw gateway restart
```

### Update Channels
```bash
openclaw update --channel beta    # beta channel
openclaw update --channel stable  # stable channel
openclaw update --channel dev     # bleeding edge
```

---

## Workspace Safety

The workspace (`~/.openclaw/workspace`) is **never touched by updates**. It's your agent's home directory.

### Standard Workspace Files
| File | Purpose | Loaded When |
|------|---------|-------------|
| `AGENTS.md` | Operating instructions, memory protocol | Every session |
| `SOUL.md` | Persona, tone, boundaries | Every session |
| `USER.md` | Who the user is | Every session |
| `IDENTITY.md` | Agent name, vibe, emoji | Every session |
| `TOOLS.md` | Notes about tools (guidance only) | Every session |
| `HEARTBEAT.md` | Checklist for heartbeat runs | Heartbeat runs |
| `BOOT.md` | Startup checklist on gateway restart | Gateway restart |
| `MEMORY.md` | Curated long-term memory | Main session only |
| `memory/YYYY-MM-DD.md` | Daily logs | Session start |

### What's NOT in the workspace (lives under `~/.openclaw/`)
- `openclaw.json` (config)
- `credentials/` (OAuth, API keys)
- `agents/*/sessions/` (transcripts)
- `skills/` (managed skills)

### Bootstrap file limits
- Per file: `bootstrapMaxChars` (default 20,000)
- Total across all files: `bootstrapTotalMaxChars` (default 24,000)
- Disable auto-creation: `agents.defaults.skipBootstrap: true`

---

## Telegram Config

### Quick Setup
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",        // or env TELEGRAM_BOT_TOKEN
      dmPolicy: "pairing",        // pairing | allowlist | open | disabled
      allowFrom: ["tg:123456"],   // numeric Telegram user IDs
      groups: { "*": { requireMention: true } },
    },
  },
}
```

### Key Telegram Options
| Option | What it does | Default |
|--------|-------------|---------|
| `dmPolicy` | Who can DM the bot | `pairing` |
| `allowFrom` | Allowlist (numeric IDs, `tg:` prefix OK) | — |
| `groupPolicy` | Group access control | `allowlist` |
| `groups.*` | Per-group settings | — |
| `requireMention` | Require @mention in groups | `true` |
| `streamMode` | Draft streaming | `partial` |
| `textChunkLimit` | Max chars per message | `4000` |
| `linkPreview` | Show link previews | `true` |
| `mediaMaxMb` | Max inbound media size | `5` |
| `replyToMode` | Reply threading | `off` |
| `reactionNotifications` | Which reactions notify | `own` |
| `capabilities.inlineButtons` | Inline keyboard scope | `allowlist` |
| `customCommands` | Extra bot menu entries | — |
| `historyLimit` | Group context history | `50` |
| `configWrites` | Allow config changes from Telegram | `true` |

### Telegram Privacy Mode
If bot needs to see ALL group messages: BotFather → `/setprivacy` → Disable. Then remove + re-add bot to each group.

### Finding Your Telegram User ID
1. DM the bot
2. `openclaw logs --follow` → read `from.id`

### Forum Topics
- Topics get isolated session keys: `...:topic:<threadId>`
- Per-topic config: `groups.<chatId>.topics.<threadId>.*`

---

## Discord Config

### Quick Setup
```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",    // or env DISCORD_BOT_TOKEN
      dmPolicy: "pairing",
      guilds: {
        "123456789012345678": {
          requireMention: false,
          channels: {
            general: { allow: true },
          },
        },
      },
    },
  },
}
```

### Required Discord Developer Portal Settings
- **Message Content Intent** — MUST be enabled
- **Server Members Intent** — recommended
- OAuth scopes: `bot`, `applications.commands`
- Permissions: View Channels, Send Messages, Read Message History, Embed Links, Attach Files

### Key Discord Options
| Option | What it does | Default |
|--------|-------------|---------|
| `dmPolicy` | DM access control | `pairing` |
| `groupPolicy` | Guild access control | `allowlist` |
| `guilds.*` | Per-guild settings | — |
| `requireMention` | Require @mention | `true` |
| `allowBots` | Process bot messages | `false` |
| `textChunkLimit` | Max chars per message | `2000` |
| `maxLinesPerMessage` | Split tall messages | `17` |
| `historyLimit` | Context history | `20` |
| `mediaMaxMb` | Max media size | `8` |
| `replyToMode` | Reply threading | `off` |
| `actions.reactions` | Allow reactions | `true` |
| `actions.moderation` | Allow mod actions | `false` |

### Discord Targets
- DM: `user:<id>`
- Guild channel: `channel:<id>`
- Bare numeric IDs are rejected

---

## Heartbeat System

Heartbeat runs periodic agent turns so the model can surface things that need attention.

### Config
```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",           // interval (0m disables)
        target: "last",         // last | telegram | discord | none | <channel>
        to: "123456789",        // optional: specific recipient
        model: "...",           // optional: cheaper model for heartbeats
        activeHours: {          // optional: restrict to certain hours
          start: "08:00",
          end: "24:00",
        },
      },
    },
  },
}
```

### How It Works
1. Every `every` interval, Gateway sends the heartbeat prompt to the agent
2. Agent reads `HEARTBEAT.md` (if it exists) and checks for pending tasks
3. If nothing to report: replies `HEARTBEAT_OK` (suppressed, no message sent)
4. If something needs attention: sends the alert to `target`

### Key Points
- Heartbeats run **full agent turns** — shorter intervals = more tokens
- Empty `HEARTBEAT.md` (just headers) = heartbeat skipped to save API calls
- `target: "none"` runs the heartbeat but doesn't deliver externally
- `ackMaxChars: 300` — replies under this length with `HEARTBEAT_OK` are suppressed
- Active hours checked against configured timezone

### Visibility Controls (per-channel)
```json5
channels: {
  defaults: { heartbeat: { showOk: false, showAlerts: true } },
  telegram: { heartbeat: { showOk: true } },  // show OK on Telegram
}
```

---

## Cron Jobs

Cron is the Gateway's built-in scheduler. Jobs persist across restarts.

### Two Execution Styles
1. **Main session** (`sessionTarget: "main"`): enqueues a system event, runs on next heartbeat
2. **Isolated** (`sessionTarget: "isolated"`): dedicated agent turn in `cron:<jobId>`, with optional delivery

### CLI Examples
```bash
# One-shot reminder (20 minutes from now)
openclaw cron add --name "Reminder" --at "20m" --session main \
  --system-event "Check the thing" --wake now --delete-after-run

# Recurring morning brief
openclaw cron add --name "Morning brief" --cron "0 7 * * *" \
  --tz "America/Chicago" --session isolated \
  --message "Summarize overnight updates." \
  --announce --channel telegram --to "123456789"

# List/manage
openclaw cron list
openclaw cron run <jobId>
openclaw cron edit <jobId> --message "Updated prompt"
openclaw cron runs --id <jobId>   # run history
```

### Config
```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
  },
}
```

### Storage
- Jobs: `~/.openclaw/cron/jobs.json`
- Run history: `~/.openclaw/cron/runs/<jobId>.jsonl`

### Schedule Types
- `at`: one-shot timestamp (ISO 8601)
- `every`: fixed interval (milliseconds)
- `cron`: 5-field cron expression with optional timezone

### Delivery (Isolated Jobs)
- `announce`: delivers output to target channel + posts summary to main session
- `none`: internal only

---

## Memory System

Memory is **plain Markdown in the workspace**. The model only "remembers" what's written to disk.

### Memory Files
- `memory/YYYY-MM-DD.md` — Daily log (append-only). Read today + yesterday at session start.
- `MEMORY.md` — Curated long-term memory. Only loaded in main/private sessions.

### Automatic Memory Flush
Before auto-compaction, OpenClaw runs a silent agent turn reminding the model to write durable notes:
```json5
{
  agents: {
    defaults: {
      compaction: {
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
        },
      },
    },
  },
}
```

### Vector Memory Search
- Enabled by default
- Indexes `MEMORY.md` + `memory/*.md`
- Supports semantic search via embeddings
- Auto-selects provider: local > openai > gemini > voyage
- Tools: `memory_search` (semantic search), `memory_get` (read file by path)
- Hybrid search (BM25 + vector) available for exact + semantic matching

### Memory Search Config
```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai",           // openai | gemini | voyage | local
        model: "text-embedding-3-small",
        query: {
          hybrid: { enabled: true, vectorWeight: 0.7, textWeight: 0.3 },
        },
      },
    },
  },
}
```

### QMD Backend (Experimental)
Local-first search sidecar combining BM25 + vectors + reranking. Set `memory.backend = "qmd"`.

---

## Session Management

### Session Scoping
- `dmScope: "main"` (default) — all DMs share one session (fine for single user)
- `dmScope: "per-channel-peer"` — isolate per channel + sender (recommended for multi-user)
- `dmScope: "per-peer"` — isolate by sender across channels

### Session Keys
- DM (main scope): `agent:<agentId>:main`
- DM (per-channel-peer): `agent:<agentId>:<channel>:dm:<peerId>`
- Group: `agent:<agentId>:<channel>:group:<id>`
- Telegram topic: `...group:<id>:topic:<threadId>`
- Cron: `cron:<jobId>`
- Webhook: `hook:<uuid>`

### Reset Policies
```json5
{
  session: {
    reset: {
      mode: "daily",     // daily | idle
      atHour: 4,         // daily reset hour (local time)
      idleMinutes: 120,  // optional idle timeout
    },
  },
}
```
- Both daily and idle can be set; whichever expires first wins
- `/new` or `/reset` in chat forces a new session
- `/new <model>` resets and switches model

### Session Storage
- Store: `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- Transcripts: `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

### Send Policy
Block delivery for specific session types:
```json5
{
  session: {
    sendPolicy: {
      rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }],
      default: "allow",
    },
  },
}
```

### Context Pruning
Prunes old tool results from in-memory context (doesn't modify JSONL history):
```json5
{
  agents: {
    defaults: {
      contextPruning: { mode: "cache-ttl", ttl: "1h" },
    },
  },
}
```

---

## Skills System

Skills teach the agent how to use tools. Each skill is a directory with a `SKILL.md`.

### Skill Locations (precedence high→low)
1. `<workspace>/skills/` — workspace skills (per-agent)
2. `~/.openclaw/skills/` — managed/local skills (shared across agents)
3. Bundled skills — shipped with OpenClaw

### Config
```json5
{
  skills: {
    entries: {
      "skill-name": {
        enabled: true,
        apiKey: "KEY",
        env: { API_KEY: "KEY" },
      },
      "unwanted-skill": { enabled: false },
    },
    allowBundled: ["gemini", "peekaboo"],  // optional bundled allowlist
  },
}
```

### Gating
Skills are filtered at load time based on:
- `requires.bins` — binaries must be on PATH
- `requires.env` — env vars must exist
- `requires.config` — config paths must be truthy
- `enabled: false` in config — explicitly disabled

### ClawHub
Browse and install skills: https://clawhub.com
```bash
clawhub install <skill-slug>
clawhub update --all
```

---

## Key CLI Commands

### Gateway Management
```bash
openclaw gateway status           # check if running
openclaw gateway start            # start (background)
openclaw gateway stop             # stop
openclaw gateway restart          # restart
openclaw gateway                  # start foreground (logs to stdout)
```

### Health & Diagnostics
```bash
openclaw health                   # quick health check
openclaw doctor                   # full diagnostic + repair
openclaw doctor --fix             # auto-fix issues
openclaw status                   # show sessions, store path
openclaw logs --follow            # tail logs
```

### Config
```bash
openclaw config get <path>        # read config value
openclaw config set <path> <val>  # write config value
openclaw config unset <path>      # remove config value
openclaw configure                # interactive wizard
openclaw onboard                  # full setup wizard
```

### Sessions
```bash
openclaw sessions --json          # dump all sessions
openclaw sessions --active 60     # active in last 60 min
```

### Channels & Pairing
```bash
openclaw channels status          # channel health
openclaw channels status --probe  # deep probe
openclaw pairing list <channel>   # pending pairing requests
openclaw pairing approve <channel> <code>  # approve pairing
```

### Cron
```bash
openclaw cron list                # list all jobs
openclaw cron add ...             # create job
openclaw cron edit <id> ...       # edit job
openclaw cron run <id>            # force run
openclaw cron runs --id <id>      # run history
```

### Messages
```bash
openclaw message send --channel telegram --target 123 --message "hi"
```

### System
```bash
openclaw system event --text "Check something" --mode now
openclaw update                   # update OpenClaw
openclaw update --channel beta    # switch update channel
```

### Chat Commands (send in chat)
| Command | What it does |
|---------|-------------|
| `/new` | Reset session |
| `/new <model>` | Reset + switch model |
| `/model <name>` | Switch model |
| `/status` | Show session status |
| `/stop` | Abort current run |
| `/compact` | Compress context |
| `/context list` | Show system prompt contents |
| `/send on/off` | Toggle delivery |
| `/activation always/mention` | Toggle group activation |
| `/reasoning on/off/stream` | Toggle reasoning display |
| `/tts off/always` | Toggle text-to-speech |
| `/elevated on/off` | Toggle elevated exec |

---

## Common Troubleshooting

### Gateway Won't Start
- Config validation failed → `openclaw doctor` to see errors, `--fix` to repair
- Port in use → check for other instances, change `gateway.port`

### Bot Not Responding
1. `openclaw health` — is gateway running?
2. `openclaw channels status` — is the channel connected?
3. `openclaw logs --follow` — what's happening?
4. Check `dmPolicy` and `allowFrom` — is the sender authorized?

### Telegram Bot Ignores Group Messages
- Check `requireMention` setting
- Disable privacy mode: BotFather → `/setprivacy` → Disable
- Remove + re-add bot to group after changing privacy
- Verify group is in `channels.telegram.groups`

### Discord Bot Ignores Messages
- Enable **Message Content Intent** in Developer Portal
- Check `groupPolicy` and guild allowlist
- Verify channel is listed if `guilds.*.channels` exists

### Config Changes Not Taking Effect
- Most changes hot-reload automatically
- `gateway.*` changes need restart: `openclaw gateway restart`
- Verify with `openclaw config get <path>`

### Session Context Getting Too Long
- `/compact` in chat to compress
- Configure `contextPruning` for automatic tool result trimming
- Check `compaction.memoryFlush` to save notes before compaction

### Heartbeat Not Running
- Check `heartbeat.every` isn't `0m`
- Check `activeHours` — might be outside the window
- Check `HEARTBEAT.md` isn't empty (just headers = skipped)
- `openclaw logs --follow` and look for heartbeat events

### After Update Issues
1. `openclaw doctor` — always first step
2. `openclaw gateway restart`
3. `openclaw health`
4. If still broken: rollback with `npm i -g openclaw@<previous-version>`
