<div align="center">

# 🧠💰 Smart Money Pulse Monitor

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Nansen-CLI%20Challenge-purple" alt="Nansen CLI Challenge">
  <img src="https://img.shields.io/badge/Base-L2-blue" alt="Base L2">
</p>

**Track whale wallets. Spot accumulation. Trade with conviction.**

[Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [Contributing](#-contributing)

<img src="docs/dashboard.jpg" alt="Smart Money Pulse Dashboard" width="800"/>

</div>

---

## 🎯 The Problem

**Smart money moves in silence. Retail arrives late.**

By the time most traders notice significant wallet accumulation or distribution, the opportunity window has closed. Whales and institutional wallets have already positioned. The information asymmetry between sophisticated on-chain analysts and everyday traders is massive.

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/clawvader-tech/smart-money-pulse.git
cd smart-money-pulse

# 2. Set your Nansen API key
export NANSEN_API_KEY="your_api_key_here"

# 3. Run the monitor
python3 smart_money_pulse.py
```

That's it! The monitor will generate a `pulse_dashboard.md` report with the top 10 smart money signals.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Money Tracking** | Monitor netflow from Nansen-labeled whale wallets |
| 📊 **Trend Analysis** | Cross-reference with trending tokens on Base |
| 🧮 **AI Scoring** | Composite algorithm ranks signals by conviction |
| 📝 **Auto Reports** | Beautiful markdown dashboards generated automatically |
| ⚡ **Real-time** | 24h timeframe for timely signals |
| 🎯 **Clear Signals** | Accumulation 🟢 / Distribution 🔴 indicators |
| 🔗 **Base Native** | Optimized for Base L2 ecosystem |
| 🖥️ **CLI First** | Simple, fast command-line interface |

---

## ⛓️ Supported Chains

| Chain | Status | Features |
|-------|--------|----------|
| **Base** | ✅ Production | Full smart money tracking |
| **Base Sepolia** | ✅ Testnet | Development & testing |
| Ethereum | 🚧 Planned | Coming soon |
| Arbitrum | 🚧 Planned | Coming soon |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 Smart Money Pulse Monitor                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐         ┌──────────────┐     ┌────────────┐  │
│   │ Nansen API  │────────▶│   Cross-     │────▶│  Markdown  │  │
│   │ Smart Money │         │  Reference   │     │ Dashboard  │  │
│   │   Netflow   │         │    Engine    │     │            │  │
│   └─────────────┘         └──────────────┘     └────────────┘  │
│          │                                              │       │
│          │         ┌──────────────┐                     │       │
│   ┌──────┴──┐      │   Scoring    │                     │       │
│   │ Nansen  │─────▶│  Algorithm   │─────────────────────┘       │
│   │ Tokens  │      └──────────────┘                             │
│   └─────────┘                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### How It Works

1. **Fetch** — Pulls smart money netflow data from Nansen API
2. **Analyze** — Cross-references with trending tokens on Base
3. **Score** — Calculates composite smart money scores
4. **Rank** — Sorts signals by conviction level
5. **Report** — Generates beautiful markdown dashboard

---

## 📊 Sample Output

```markdown
# 🧠 Smart Money Pulse Monitor

**Generated:** 2026-03-20 18:00 UTC  
**Chain:** Base  
**Timeframe:** 24h

## 🏆 Top 10 Smart Money Moves

### 1. AERO — Aerodrome Finance
| Metric | Value |
|--------|-------|
| Signal | 🟢 **ACCUMULATING** |
| Net Flow | +$2,450,000 |
| Smart Score | ⭐ 285.3 |

### 2. DEGEN — Degen
| Metric | Value |
|--------|-------|
| Signal | 🔴 **DISTRIBUTING** |
| Net Flow | -$1,200,000 |
| Smart Score | ⭐ 142.7 |
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NANSEN_API_KEY` | ✅ Yes | Your Nansen API key |

### Score Thresholds

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MIN_FLOW_THRESHOLD` | $50,000 | Minimum flow to include |
| `TOP_N` | 10 | Number of signals to report |

---

## 🛣️ Roadmap

- [x] Core smart money tracking
- [x] Token cross-referencing
- [x] Composite scoring algorithm
- [x] Markdown dashboard generation
- [ ] WebSocket real-time feeds
- [ ] Multi-chain support (Ethereum, Arbitrum)
- [ ] Historical trend analysis
- [ ] Telegram/Discord alerts
- [ ] MCP server for AI agents
- [ ] Web dashboard

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built for the **Nansen CLI Build Challenge 2026**
- Powered by [Nansen](https://nansen.ai) smart money data
- Made with ❤️ by [@clawvader](https://x.com/clawvader)

---

<div align="center">

**[⭐ Star this repo](https://github.com/clawvader-tech/smart-money-pulse)** if you find it useful!

<p align="center">
  <sub>Built with the Nansen CLI</sub>
</p>

</div>
