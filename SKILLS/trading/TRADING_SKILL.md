# Trading Skill — Frankie Bot

Frankie uses this document as the single source of truth for Jay's trading strategies,
Ghost webhook configuration, indicator tuning methodology, and risk management rules.

---

## 1. ORB (Opening Range Breakout) Strategy

The Open Range Breakout is Jay's core intraday strategy.

### Rules

1. **Mark the opening range**: At **9:30 AM ET**, mark the 15-minute candle from high wick to low wick. This zone is the "opening range."
2. **Drop to 5-minute timeframe** after the 15-min candle closes (9:45 AM).
3. **Wait for confirmation**: A 5-min candle **body** must **close** above or below the zone.
   - Wick pokes don't count — the body must close outside.
4. **Enter in direction of breakout**:
   - Close above the zone → Long
   - Close below the zone → Short
5. No re-entries once the first breakout triggers. One shot per session.

---

## 2. Ghost Webhook Rules

Ghost automates trade execution from TradingView alerts. These rules are **non-negotiable**.

### Critical Rules

| Rule | Detail |
|------|--------|
| **One webhook per ticker** | Each ticker gets its OWN unique webhook URL. Never reuse a webhook across tickers. |
| **One layout per ticker** | Each ticker needs its OWN TradingView layout/panel. Never share panels between tickers. |
| **Indicator isolation** | Changing indicator settings in one panel **overwrites ALL alerts** in that panel. Always use separate layouts. |
| **Ticker symbols** | Use bare symbols only: `MGC`, `MNQ`, `ES`, `XAUUSD`, `BTC` — **no contract dates** (not MGC1!, not MNQH2025, etc.) |

### Webhook Setup Checklist (per ticker)
1. Create a new TradingView layout for the ticker
2. Add the indicator with ticker-specific settings (see Section 4)
3. Create a new Ghost webhook for this ticker
4. Set the alert on the indicator → point to the new webhook
5. Verify in Ghost dashboard that the webhook is receiving signals
6. Never touch this layout's indicator settings again without understanding it resets all alerts

---

## 3. Bulletproof Indicator Fine-Tuning Methodology

Every ticker behaves differently. Settings must be tuned **per ticker** using backtests.

### Parameters to Tune (per ticker)
- **Contracts**: Position size (number of contracts)
- **Direction**: Long only, short only, or both
- **Mode**: Aggressive vs. balanced
- **Session filter**: NY only, Asia+London, all sessions
- **Stop multiplier**: ATR-based (e.g., 0.5x, 1.0x, 1.5x, 2.0x)
- **TP1 multiplier**: First profit target (risk:reward)
- **TP2 multiplier**: Runner target (risk:reward)

### Backtesting Windows
Run every settings change through **three** time windows:

| Window | Purpose |
|--------|---------|
| **30-day** | Recent market regime — is it working NOW? |
| **90-day** | Medium-term — does it survive regime changes? |
| **365-day** | Full year — does it hold through all conditions? |

### Acceptance Criteria
A setting is "good" only if it hits ALL of these across all three windows:

- ✅ **Win rate ≥ 60%**
- ✅ **Profit factor ≥ 2.5**
- ✅ **Max drawdown within account limits** (see Section 5)

If ANY window fails, the settings need adjustment before going live.

---

## 4. Known Good Settings (from backtests)

These are the currently validated settings. Update this section when settings change.

### SIL (Silver)
| Parameter | Value |
|-----------|-------|
| Contracts | 2 |
| Direction | Both (long + short) |
| Mode | — |
| Session | All |
| Stop multiplier | 2.0x |
| TP1 | 1.7 |
| TP2 | 2.5 |

### NQ (Nasdaq Futures) — 5-min
| Parameter | Value |
|-----------|-------|
| Contracts | 5 |
| Direction | Both |
| Mode | Aggressive |
| Session | NY only |
| Stop multiplier | 0.5x |
| TP1 | 1.5 |
| TP2 | 4.0 |

### GC (Gold Futures) — 1-min
| Parameter | Value |
|-----------|-------|
| Contracts | 2 |
| Direction | Both |
| Mode | Balanced |
| Session | NY only |
| Stop multiplier | 2.0x |
| TP1 | 3.0 |
| TP2 | 4.0 |

### MGC (Micro Gold) — 5-min
| Parameter | Value |
|-----------|-------|
| Contracts | 10 (micros) |
| Direction | Both |
| Mode | Balanced |
| Session | Asia + London only |
| Stop multiplier | 1.5x |
| TP1 | 1.5 |
| TP2 | 2.5 |

### MNQ (Micro Nasdaq) — 1-min
| Parameter | Value |
|-----------|-------|
| Contracts | 8 (micros) |
| Direction | Both |
| Mode | Balanced |
| Session | NY only |
| Stop multiplier | 2.0x |
| TP1 | 2.2 |
| TP2 | 4.0 |

---

## 5. Risk Rules

### Prop Firm Rules

| Firm | Automation Allowed? | Notes |
|------|---------------------|-------|
| **Apex** | ❌ NO — manual only | Do NOT run Ghost on Apex accounts. Will result in account termination. |
| **Topstep** | ✅ Yes, 100% | Full automation via Ghost is allowed. |
| **Lucid** | ✅ Yes, 100% | Full automation via Ghost is allowed. |

> **⚠️ CRITICAL**: Drawdown limits vary by account size. Always check the specific account's max drawdown before setting position sizes.

### Loss Management
- **Max consecutive losses before pausing: 2–3**
- After 2 consecutive losses: review settings, check if market regime changed
- After 3 consecutive losses: **pause automation**, manually review all trades
- Resume only after identifying the issue (bad settings, regime change, data feed issue)

### Drawdown Monitoring
- Frankie tracks drawdown per account in real-time
- Alerts Jay when drawdown reaches **70%** of the account limit
- **Hard stop alert** at **85%** of limit — strongly recommends pausing
- All drawdown data is in the `trades` table, grouped by `account`

---

## 6. Tickers to Track

Only these tickers are actively traded:

- **MGC** — Micro Gold
- **MNQ** — Micro Nasdaq
- **ES** — S&P 500 E-mini
- **XAUUSD** — Spot Gold (forex)
- **BTC** — Bitcoin

No other tickers should be added without explicit instruction from Jay.
