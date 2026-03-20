---
name: smart-money-pulse
description: Track whale and institutional wallet flows across multiple chains, get ranked trading signals with confidence scores, and execute trades autonomously. Use when the user mentions tracking smart money, whale wallets, institutional flows, token accumulation, DeFi signals, on-chain trading, or wants to monitor cryptocurrency markets. Triggers on phrases like "track whale wallets", "smart money", "token flow analysis", "on-chain signals", "CEO dashboard", "trading signals", "PULSE", "Autonomous trading agent", or when building a crypto trading bot or on-chain analytics tool.
license: MIT
metadata:
  author: Clawvader
  version: "1.0.0"
compatibility: "Python 3.12+. Requires: requests, python-dotenv, mcp. Network access needed for API calls."
---

# Smart Money Pulse Monitor — Agent Skill

Enables autonomous AI agents to track whale/institutional wallet flows, analyze on-chain signals, and execute trades through a modular system.

## What This Skill Does

1. **Real-Time Signal Generation** — ranked token opportunities by smart money flow, confidence, and momentum
2. **Multi-Chain Coverage** — Base, Ethereum, Solana, Arbitrum, Optimism
3. **MCP Server Integration** — tools for AI agents to query signals, positions, trade history, and system health
4. **x402 Payment Gateway** — native crypto micropayments for API calls
5. **CEO Dashboard** — world-class HTML dashboard for human oversight

## Core Concepts

### Smart Money Status
| Status | Meaning |
|--------|---------|
| `ACTIVE` | Strong whale accumulation, high confidence |
| `CAUTION` | Mixed signals, wait for confirmation |
| `EXIT` | Smart money selling, avoid or short |

### Supported Chains
- **Base** (primary) — DEGEN, AERO, BRETT, PENGU, VIRTUAL, cbBTC, USDC
- **Ethereum** — WBTC, stETH, LDO, UNI, LINK, AAVE
- **Solana** — WIF, BONK, POPCAT, MEW, BOME, JTO, JUP
- **Arbitrum** — ETH, USDC, ARB
- **Optimism** — ETH, USDC, OP

### Signal Scoring
```
confidence = base_confidence × flow_multiplier × momentum_factor
```
- **Flow magnitude** — 24h USD volume of smart money
- **Direction** — accumulation vs distribution
- **Velocity** — accelerating vs decelerating

## Usage

### Quick Start

```bash
# Clone the repo
git clone https://github.com/clawvader-tech/smart-money-pulse.git
cd smart-money-pulse

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your NANSEN_API_KEY (optional — free sources work without it)

# Run CLI
python smart_money_pulse.py --chain base --top-n 10
```

### CLI Commands

```bash
# Get top signals on Base
python smart_money_pulse.py --chain base --top-n 5

# Get signals on Ethereum
python smart_money_pulse.py --chain ethereum --top-n 10

# Get wallet-specific flow
python smart_money_pulse.py --wallet 0x... --chain base

# Run as continuous monitor
python smart_money_pulse.py --monitor --interval 60

# Output JSON for agent consumption
python smart_money_pulse.py --chain base --format json
```

### MCP Server Tools

Start the MCP server:
```bash
python mcp_server.py
```

Available tools:
- `get_signals(chain: str, top_n: int)` — ranked trading signals
- `get_positions()` — current open positions
- `get_trade_history(limit: int)` — recent trade history
- `get_system_status()` — system health and data source status
- `execute_trade(token: str, action: str, amount_usd: float)` — submit a trade
- `get_wallet_balance()` — connected wallet balance

### CEO Dashboard

Open in any browser:
```bash
open dashboard.html
```

Features: signal feed, trade history, open positions, system health, OKX wallet widget.

### Payment Gateway (x402)

Start the payment server:
```bash
python payment_gateway.py
```

Endpoints:
- `GET /api/v1/signals` — premium signals (paid)
- `GET /api/v1/augment` — AI-augmented analysis (paid)
- `GET /health` — free health check

## Architecture

```
Data Sources: CoinGecko, Nansen API, OKX OnchainOS
     ↓
LLM Reasoning: minimax-m2.7 via OpenRouter
     ↓
Signal Engine: Scoring → Confidence → Ranking
     ↓
Outputs: CLI | MCP Server | Dashboard | x402 Payments
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NANSEN_API_KEY` | No | Nansen API key for enhanced signals (free sources work without it) |
| `OPENROUTER_API_KEY` | Yes | OpenRouter key for LLM reasoning |
| `OKX_WALLET_EMAIL` | No | Email for OKX wallet login |
| `ALLOWED_WALLET` | No | Restrict trades to this wallet address |

## Agent Integration Example

```python
import json
import subprocess

def get_top_signal(chain="base"):
    """Get the top smart money signal for a chain."""
    result = subprocess.run(
        ["python", "smart_money_pulse.py", "--chain", chain, "--top-n", "1", "--format", "json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def get_mcp_signals():
    """Query MCP server for current signals."""
    import mcp
    # Connect to MCP server and call get_signals tool
    ...
```

## Troubleshooting

**No signals returned:**
- Check data source connectivity (`python smart_money_pulse.py --doctor`)
- Free sources (CoinGecko) work without API keys

**MCP server not responding:**
- Ensure port 8080 is available
- Check `logs/mcp_server.log` for errors

**Dashboard not loading:**
- Open `dashboard.html` directly in browser (no server needed)
- Chrome/Edge recommended for best rendering

## Files

| File | Purpose |
|------|---------|
| `smart_money_pulse.py` | Main CLI entry point |
| `mcp_server.py` | Model Context Protocol server |
| `payment_gateway.py` | x402 crypto payment gateway |
| `dashboard.html` | CEO dashboard (open in browser) |
| `chain_data.py` | Multi-chain token registry |
| `requirements.txt` | Python dependencies |

## License

MIT License — use freely for personal and commercial AI agents.
