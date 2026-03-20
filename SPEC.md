# Smart Money Pulse Monitor — Technical Specification

> **Version:** 1.0.0  
> **Status:** Production Ready  
> **License:** MIT  
> **Hackathon:** Nansen CLI Build Challenge 2026

---

## One-Liner

An AI-powered smart money tracker that monitors whale and institutional wallet flows on Base, cross-references with trending tokens, and generates ranked trading signals.

---

## Features

- 🔍 **Smart Money Flow Tracking** — Monitor netflow data from Nansen-labeled wallets
- 📊 **Trending Token Analysis** — Cross-reference flows with high-volume tokens
- 🧮 **Composite Scoring Algorithm** — Rank signals by magnitude, direction, and volume ratio
- 📝 **Auto-Generated Reports** — Beautiful markdown dashboards with insights
- ⚡ **Real-time Data** — 24h timeframe updates for timely signals
- 🎯 **Accumulation/Distribution Signals** — Clear buy/sell indicators
- 🔗 **Base Network Focus** — Optimized for Base L2 ecosystem
- 🖥️ **CLI Interface** — Simple command-line execution
- 📱 **Extensible Architecture** — MCP server ready for AI agent integration

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Smart Money Pulse Monitor                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   INPUT LAYER                    PROCESSING LAYER      OUTPUT LAYER    │
│   ───────────                    ────────────────      ───────────     │
│                                                                         │
│  ┌─────────────┐                ┌──────────────┐      ┌─────────────┐  │
│  │ Nansen API  │───────────────▶│ Smart Money  │      │  Markdown   │  │
│  │ Smart Money │                │   Engine     │─────▶│  Dashboard  │  │
│  │   Netflow   │                │              │      │             │  │
│  └─────────────┘                └──────────────┘      └─────────────┘  │
│         │                               │                    │         │
│         │                               │                    │         │
│  ┌─────────────┐                ┌──────────────┐      ┌─────────────┐  │
│  │   Nansen    │───────────────▶│   Cross-     │      │  Console    │  │
│  │   Token     │                │  Reference   │─────▶│   Output    │  │
│  │  Screener   │                │    Engine    │      │             │  │
│  └─────────────┘                └──────────────┘      └─────────────┘  │
│                                        │                               │
│                                        ▼                               │
│                              ┌──────────────┐                          │
│                              │   Scoring    │                          │
│                              │   Algorithm  │                          │
│                              └──────────────┘                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

Data Flow:
1. Fetch smart money netflow (Base, 24h)
2. Fetch trending tokens (Base, 24h)
3. Cross-reference by symbol/address
4. Calculate composite scores
5. Generate ranked report
6. Save to markdown dashboard
```

---

## Supported Chains

| Chain | Chain ID | Status | Notes |
|-------|----------|--------|-------|
| Base | 8453 | ✅ Production | Primary chain, full feature support |
| Base Sepolia | 84532 | ✅ Testnet | Testing and development |

### Planned Support

| Chain | Chain ID | Status | Notes |
|-------|----------|--------|-------|
| Ethereum | 1 | 🚧 Planned | Smart money tracking |
| Arbitrum | 42161 | 🚧 Planned | L2 expansion |
| Optimism | 10 | 🚧 Planned | L2 expansion |

---

## Quick Start

### Prerequisites

- Python 3.12+
- Nansen API key ([Get one here](https://nansen.ai))
- Nansen CLI installed

### Installation

```bash
# Clone the repository
git clone https://github.com/clawvader/smart-money-pulse.git
cd smart-money-pulse

# Set environment variable
export NANSEN_API_KEY="your_api_key_here"

# Run the monitor
python3 smart_money_pulse.py
```

### Output

The tool generates:
- `pulse_dashboard.md` — Full markdown report
- Console output — Preview of top signals

---

## Smart Money Score Algorithm

```python
score = (|netflow| / 10,000) * direction_bonus + volume_ratio_factor

where:
- direction_bonus = 1.2 for accumulation, 1.0 for distribution
- volume_ratio_factor = (|netflow| / volume_24h) * 100
```

### Thresholds

| Parameter | Value | Description |
|-----------|-------|-------------|
| MIN_FLOW_THRESHOLD | $50,000 | Minimum flow to report |
| Top N Results | 10 | Number of signals in report |

---

## API Integration

### Nansen CLI Commands

```bash
# Smart money netflow
nansen research smart-money netflow --chain base --timeframe 24h

# Token screener
nansen research token screener --chain base --timeframe 24h
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NANSEN_API_KEY` | ✅ Yes | Your Nansen API key |

---

## File Structure

```
smart-money-pulse/
├── smart_money_pulse.py    # Main application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── SPEC.md                # This specification
├── CONTRIBUTING.md        # Contribution guidelines
├── SUPPORT.md            # Support information
├── .gitignore            # Git ignore rules
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI
├── docs/
│   └── index.html        # GitHub Pages site
└── assets/               # Images and media
```

---

## Roadmap

### Phase 1: Core (✅ Complete)
- [x] Smart money flow tracking
- [x] Token cross-referencing
- [x] Composite scoring algorithm
- [x] Markdown dashboard generation

### Phase 2: Enhancement (In Progress)
- [ ] Real-time WebSocket feeds
- [ ] Multi-chain support (Ethereum, Arbitrum, Optimism)
- [ ] Historical trend analysis
- [ ] Alert notifications (Telegram, Discord)

### Phase 3: Ecosystem (Planned)
- [ ] MCP server for AI agents
- [ ] REST API
- [ ] Web dashboard
- [ ] Mobile app

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built for the **Nansen CLI Build Challenge 2026**  
Powered by [Nansen](https://nansen.ai)  
Made with ❤️ by @clawvader
