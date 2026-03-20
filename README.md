# 🧠💰 Smart Money Pulse Monitor

```
    ╭──────────────────────────────────────────────╮
    │                                              │
    │   🦈 SMART MONEY PULSE MONITOR 🦈            │
    │   ─────────────────────────────────          │
    │   Track. Analyze. Profit.                    │
    │                                              │
    │   "The early shark catches the alpha"        │
    │                                              │
    ╰──────────────────────────────────────────────╯
```

> **🚀 Nansen CLI Build Challenge — Week 1 Submission**  
> **Built by:** Adam (@clawvader)  
> **Deadline:** March 22, 2026

---

## 🎯 The Problem

**Smart money moves in silence. Retail arrives late.**

By the time most traders notice significant wallet accumulation or distribution, the opportunity window has closed. Whales and institutional wallets have already positioned. The information asymmetry between sophisticated on-chain analysts and everyday traders is massive.

**Current solutions are either:**
- ❌ Too expensive (enterprise Nansen subscriptions)
- ❌ Too slow (manual analysis takes hours)
- ❌ Too noisy (Telegram channels with 90% false signals)
- ❌ Too technical (requires SQL/Python skills)

---

## 💡 The Solution

**Smart Money Pulse Monitor** is an AI agent that automates the detection of significant smart money flows, delivering publication-ready intelligence reports in seconds.

### What It Does

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT                           OUTPUT                     │
│  ─────                           ──────                     │
│                                                             │
│  📊 Smart Money Flows     →     🏆 Top 10 Ranked Signals   │
│  🔍 Trending Tokens       →     📈 Accumulation Alerts     │
│  ⏱️  24h Timeframe        →     🔴 Distribution Warnings   │
│                                                             │
│  6 API Credits            →     Executive Dashboard        │
└─────────────────────────────────────────────────────────────┘
```

### Core Features

| Feature | Description |
|---------|-------------|
| 🎯 **Smart Money Flow Tracking** | Monitors net inflows/outflows from Nansen-labeled smart money wallets |
| 🔥 **Trending Token Discovery** | Identifies hot tokens via Nansen's token screener |
| 🔗 **Cross-Reference Intelligence** | Matches smart money activity with trending tokens |
| 📊 **Ranked Signal Generation** | Creates a "Top 10 Smart Money Moves" report |
| 📝 **Beautiful Markdown Reports** | Generates publication-ready dashboards |
| ⚡ **Budget Optimized** | Only 6 credits per run (~$0.60 at current rates) |

---

## 🏆 Why This Wins

### 1. **Real Utility, Real Problem**
Not a toy project. This solves an actual pain point that traders face daily — detecting smart money activity before it becomes obvious.

### 2. **Technical Excellence**
- Clean, modular Python architecture
- Robust error handling and timeouts
- Type hints throughout
- Environment-based configuration
- Subprocess integration with Nansen CLI

### 3. **Cost Efficiency**
Most Nansen features require 100+ credits per query. This monitor achieves deep intelligence with just **6 credits**:
- Smart Money Netflow: 5 credits
- Token Screener: 1 credit

### 4. **Production Ready**
- Graceful fallbacks when API limits hit
- Detailed logging for debugging
- Extensible design (easy to add chains/timeframes)
- Publication-quality output

### 5. **The "Aha" Moment**
The cross-referencing engine is the secret sauce. It doesn't just show flows — it **contextualizes** them against trending tokens to surface truly significant signals.

### 6. **Extensibility**
Built with expansion in mind:
- Multi-chain support (Ethereum, Solana, Arbitrum)
- Alert notifications (email/Telegram/Twitter)
- Historical trend analysis
- Automated social posting

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install Nansen CLI
npm install -g @nansen/cli

# Verify installation
nansen --version

# Set your API key
export NANSEN_API_KEY="your_api_key_here"
```

### Run It

```bash
# Clone/navigate to project
cd nansen-hackathon

# Make the demo executable
chmod +x hackathon_demo.sh

# Run the full demo (fetches live data)
./hackathon_demo.sh
```

### Manual Run

```bash
# Install Python dependencies (if any)
pip install -r requirements.txt

# Run the monitor
python3 smart_money_pulse.py

# View the generated report
cat pulse_dashboard.md
```

---

## 📊 Sample Output

The monitor generates a `pulse_dashboard.md` report:

```markdown
# 🧠 Smart Money Pulse Monitor

**Generated:** 2026-03-20 13:30 UTC  
**Chain:** Base  
**Timeframe:** 24h

---

## 📊 Executive Summary

| Metric | Value |
|--------|-------|
| Smart Money Flows Tracked | 47 |
| Trending Tokens Analyzed | 156 |
| Significant Moves Identified | 23 |
| Accumulating Signals | 15 |
| Distributing Signals | 8 |

---

## 🏆 Top 3 Smart Money Moves

### 1. TOKEN-A — Alpha Token
| Metric | Value |
|--------|-------|
| Signal | 🟢 **ACCUMULATING** |
| Net Flow | +$1,245,000 |
| Smart Score | ⭐ 185.3 |

### 2. TOKEN-B — Beta Protocol
| Metric | Value |
|--------|-------|
| Signal | 🔴 **DISTRIBUTING** |
| Net Flow | -$892,000 |
| Smart Score | ⭐ 142.7 |
```

---

## 🔧 Technical Deep Dive

### Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    Smart Money Pulse Monitor                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │   Nansen CLI     │         │   Nansen CLI     │            │
│  │  (subprocess)    │         │  (subprocess)    │            │
│  │                  │         │                  │            │
│  │ research smart-  │         │ research token   │            │
│  │ money netflow    │         │ screener         │            │
│  └────────┬─────────┘         └────────┬─────────┘            │
│           │                            │                      │
│           ▼                            ▼                      │
│  ┌──────────────────────────────────────────┐                 │
│  │        Data Processing Layer             │                 │
│  │  • Token lookup by symbol/address        │                 │
│  │  • Flow aggregation and filtering        │                 │
│  │  • Composite scoring algorithm           │                 │
│  └─────────────────────┬────────────────────┘                 │
│                        │                                      │
│                        ▼                                      │
│  ┌──────────────────────────────────────────┐                 │
│  │         Report Generation                │                 │
│  │  • Markdown formatting                   │                 │
│  │  • Ranked tables                         │                 │
│  │  • Insight extraction                    │                 │
│  └──────────────────────────────────────────┘                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Nansen CLI Integration

```python
# Fetch smart money netflow
cmd = [
    "nansen", "research", "smart-money", "netflow",
    "--chain", "base",
    "--timeframe", "24h"
]

# Fetch trending tokens  
cmd = [
    "nansen", "research", "token", "screener",
    "--chain", "base",
    "--timeframe", "24h"
]
```

### Smart Money Score Algorithm

The scoring algorithm ranks tokens by significance:

```python
def _calculate_score(self, netflow: float, inflow: float, 
                     outflow: float, token: Optional[Dict]) -> float:
    # Base score from netflow magnitude
    score = abs(netflow) / 10000  # Scale down
    
    # Bonus for accumulation vs distribution
    if netflow > 0:
        score *= 1.2  # Accumulation gets 20% bonus
    
    # Volume ratio factor (how significant is this flow?)
    if token and token.get("volume_24h"):
        volume = float(token.get("volume_24h", 1))
        if volume > 0:
            flow_ratio = abs(netflow) / volume
            score += flow_ratio * 100
    
    return round(score, 2)
```

**Factors considered:**
- **Magnitude**: Larger flows = higher scores
- **Direction**: Accumulation gets a 20% bonus (bullish signal)
- **Volume Context**: Flow relative to total volume indicates conviction

### Nansen Features Used

| Feature | CLI Command | Credits | Purpose |
|---------|-------------|---------|---------|
| Smart Money Netflow | `nansen research smart-money netflow` | 5 | Track labeled wallet flows |
| Token Screener | `nansen research token screener` | 1 | Identify trending tokens |

**Total per run:** 6 credits

---

## 📁 Project Structure

```
nansen-hackathon/
├── smart_money_pulse.py     # Main Python agent (300+ lines)
├── pulse_dashboard.md       # Generated output report
├── hackathon_demo.sh        # One-command demo script
├── README.md                # This file
├── DRAFT_TWEETS.md          # Social content ready to post
└── requirements.txt         # Python dependencies
```

---

## 🛣️ Roadmap

### Phase 1: Core (Complete ✅)
- [x] Smart money flow tracking
- [x] Token screener integration
- [x] Cross-reference engine
- [x] Markdown report generation

### Phase 2: Enhancement (In Progress)
- [ ] Multi-chain support (Ethereum, Solana, Arbitrum)
- [ ] Alert notifications via email/Telegram
- [ ] Historical trend analysis
- [ ] Web dashboard with charts

### Phase 3: Automation (Planned)
- [ ] Automated X posting of top signals
- [ ] Discord bot integration
- [ ] Scheduled monitoring (cron)
- [ ] API for external integrations

---

## 🐦 Social

**Follow the build:**
- X/Twitter: [@clawvader](https://x.com/clawvader)
- GitHub: [clawvader](https://github.com/clawvader)

**Share this project:**

```
Just built a Smart Money Pulse Monitor for the #NansenCLI challenge! 🧠🦈

Tracks smart money flows on Base and generates ranked reports of 
accumulation/distribution signals — all for just 6 API credits.

cc: @nansen_ai
```

---

## 📄 License

MIT — Built for the Nansen CLI Build Challenge 2026

---

<p align="center">
  <strong>🦈 Track the sharks. Ride the waves. 🌊</strong><br>
  <em>Built with the Nansen CLI</em>
</p>
