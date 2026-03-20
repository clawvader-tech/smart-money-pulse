# Smart Money Pulse Monitor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Nansen](https://img.shields.io/badge/Nansen-CLI%20Challenge-purple)
![Base](https://img.shields.io/badge/Base-L2-blue)

**Track whale wallets. Spot accumulation. Trade with conviction.**

[Quick Start](#-quick-start) · [Features](#-features) · [Chains](#-supported-chains) · [MCP Server](#-mcp-server) · [Contributing](#-contributing)

</div>

---

## The Problem

Smart money moves in silence. Retail arrives late. By the time traders notice whale accumulation, the opportunity is gone.

## The Solution

AI-powered CLI that tracks whale/institutional wallet flows across multiple chains, ranks opportunities by confidence, and outputs actionable signals.

```bash
$ python smart_money_pulse.py --chain base --top-n 5

  Rank  Token      Flow (24h)    Smart Money
  ----  ---------  -----------   -----------
    1   PENGU     +$2,431,000   ACTIVE
    2   AERO      +$1,872,000   ACTIVE
    3   BRETT     -$943,000     EXIT
    4   DEGEN     +$521,000     ACTIVE
    5   VIRTUAL   +$298,000     CAUTION

  Confidence: 87%  |  Cycles: 56  |  Status: LIVE
```

## Features

| | |
|-|-|
| 📊 **Real-Time Signals** | Ranked opportunities with confidence scores |
| 🤖 **MCP Server** | AI agent integration via Model Context Protocol |
| 💳 **x402 Payments** | Native crypto micropayments for API access |
| 🖥️ **CEO Dashboard** | HTML dashboard with live data |
| ⛓️ **Multi-Chain** | Base, Ethereum, Solana, Arbitrum, Optimism |
| 🔒 **Secure** | No API keys in code. Environment config only |

## Supported Chains

| Chain | Status | Native Token | Key Tokens |
|-------|--------|-------------|------------|
| **Base** | Primary | ETH | DEGEN, AERO, BRETT, PENGU, VIRTUAL, cbBTC |
| **Ethereum** | Full | ETH | WBTC, stETH, LDO, UNI, LINK, AAVE, ARB, OP |
| **Solana** | Full | SOL | WIF, BONK, POPCAT, MEW, BOME, WEN, JTO, JUP |
| **Arbitrum** | Full | ETH | USDC, ARB |
| **Optimism** | Full | ETH | USDC, OP |

## Quick Start

```bash
git clone https://github.com/clawvader-tech/smart-money-pulse.git
cd smart-money-pulse
pip install -r requirements.txt
cp env.example .env   # add your NANSEN_API_KEY
python smart_money_pulse.py --chain base --top-n 10
```

## MCP Server

AI agents connect via Model Context Protocol:

```python
- get_signals(chain="base")     # Current trading signals
- get_positions()               # Open positions
- execute_trade(token, action)  # Execute via OKX
- get_system_status()          # Health & metrics
```

## Files

```
├── smart_money_pulse.py    # Main CLI
├── mcp_server.py           # AI agent integration
├── payment_gateway.py      # x402 payments
├── dashboard.html           # CEO dashboard (open in browser)
├── chain_data.py            # Multi-chain token registry
├── docs/                   # GitHub Pages site
├── assets/                 # Brand assets
└── requirements.txt
```

## License

MIT

Built for **Nansen CLI Build Challenge 2026**
