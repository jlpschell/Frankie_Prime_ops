# QuantCrawler + Ghost Trading Platform Reference

## Overview
**Creator:** Aaron (Automate With Aaron)
**Website:** quantcrawler.com
**Purpose:** AI-powered trading analysis + automated execution

---

## QuantCrawler

### What It Is
AI chart analysis platform that provides:
- Entry points, stop losses, and profit targets
- Trade tracking and P&L analytics
- Built-in trade journal
- Multi-market coverage (Futures, Forex, Crypto, Options)

### Pricing
- **Free trial:** 30 days
- **Monthly:** $9.99/month
- **Lifetime membership:** Exclusive perks + Bulletproof indicator

### Key Features

#### 1. Chart Analyzers
- **Futures:** Screenshot-based (15m, 5m, 1m charts required)
- **Forex/Crypto/Options:** Auto-pull by ticker symbol
- Each analysis provides:
  - Direction (Long/Short/Stay Away)
  - Entry, stop loss, profit targets
  - Confidence level
  - Time frame confluence (2/3 or 3/3 alignment)
  - Option 1: Standard R:R
  - Option 2: Tighter risk (single contract)
  - Option 3: Chart-based (support/resistance)

#### 2. Chrome Extension
- Keyboard shortcut: Ctrl+Shift+Q
- Captures 15m, 5m, 1m charts automatically
- Auto-launches analyzer after 3 captures

#### 3. Trade Journal
- Auto-populates from analysis
- Tracks actual entry/exit
- Calculates P&L
- Performance analytics dashboard

#### 4. Prop Firm Database
Which firms allow bots:
| Firm | Bot Policy |
|------|------------|
| Apex | Eval only |
| Topstep | All stages allowed |
| Alpha Futures | NO BOTS (will lose account) |
| Take Profit Trader | Eval only |
| My Funded Futures | Allowed |
| Fiverr | Allowed |
| E8 | Allowed |

#### 5. TradingView Indicators
- Liquidity + Opening Range Break signals
- Session liquidity level tracking
- 622+ users have saved it

#### 6. Additional Tools
- Position size calculators
- Lot size calculators
- Crypto calculators
- Session times reference
- Trading psychology PDF
- ORB strategy guide
- Market prep template
- Glossary for beginners

---

## Ghost

### What It Is
Automated trade execution platform that:
- Receives TradingView alerts via webhook
- Executes trades on connected broker accounts
- Manages positions with stop loss and take profit
- Supports copy trading across multiple accounts

### Timeline
- **Feb 1, 2026:** Lifetime member beta launch
- **March 1, 2026:** Full public release

### Pricing
- Currently lifetime-member exclusive
- Project X API (for Topstep): $25/month (promo code "TOPSTEP" for 50% off)

### Supported Brokers
1. **TradeOfEight:** Apex, Lucid, Alpha Futures, others
2. **Project X:** Topstep only (requires API key)
3. **TradeLocker:** Forex
4. **CTrader:** Coming soon
5. **Coinbase:** Crypto
6. **Tunix:** Additional

### Key Features

#### 1. Setup Wizard
5-step guided setup:
1. Welcome screen
2. Connect broker (OAuth login)
3. Select tickers
4. Set max daily loss limit
5. Enable demo mode or go live

#### 2. Ticker Configuration
Per-ticker settings:
- Strategy name
- Contract quantity
- Stop loss distance (points)
- Take profit distance (points)
- "No take profit" option (let runners run)
- Trading hours restrictions (3 windows)

#### 3. Copy Trader Mode
- Connect multiple broker accounts
- One signal executes across all selected accounts
- Mix TradeOfEight + Project X + TradeLocker

#### 4. Webhook Integration
For Bulletproof strategy:
1. Right-click chart → Add Alert
2. Select BPV 1.0.3 strategy
3. Delete default message
4. Paste Ghost strategy message
5. Add Ghost webhook URL to notifications
6. Ghost settings OVERRIDE TradingView payload (contracts, SL, TP)

#### 5. Dashboard Controls
- **Start/Stop Ghost:** Master on/off
- **Sync button:** Force sync with broker
- **Ghost Vanish:** Emergency close all + shutdown
- Position monitoring
- User ID for support tickets

#### 6. Contrarian Mode
- Flips signals (long → short, short → long)
- For strategies that typically reverse on you

#### 7. AI Automation Tab
- Not yet released (5-7 days after launch)
- QuantCrawler integration coming

### AI Support Bot
- Built-in chatbot knows all Ghost documentation
- Escalates to Aaron's phone/email after 17+ min issues
- For urgent matters only (account connection issues, not trade sizing questions)

### Critical Setup Notes
1. **Must replace TradingView alert message** with Ghost strategy message
2. Settings in Ghost override TradingView payload
3. If position shows in broker but not Ghost dashboard → SYNC + submit ticket
4. Watch trades during beta period
5. Demo mode must be unchecked for live trading

---

## Integration Flow

```
TradingView Alert
      ↓
   Webhook
      ↓
    Ghost
      ↓
  Broker API
      ↓
Trade Executed
```

## Your Setup Path
1. QuantCrawler for analysis confirmation
2. Bulletproof indicator for signals
3. TradingView alerts configured
4. Ghost for execution
5. Multiple prop accounts via copy trader
