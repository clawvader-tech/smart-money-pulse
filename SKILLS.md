# Nansen Hackathon — Smart Money Pulse

## What to Build

An AI agent-powered **Smart Money Pulse Monitor** that:
1. Tracks Smart Money flows across Base, Solana, Ethereum
2. Identifies accumulation/distribution patterns
3. Generates alerts when smart money moves >$50K
4. Creates a visual markdown dashboard
5. Posts findings to X

## Contest Requirements
- Install Nansen CLI ✅
- Make ≥10 API calls ✅ (30 credits available)
- Build something real ✅
- Share on X with #NansenCLI @nansen_ai ✅

## Deadline
**Mar 22, 2026 — 11:59 PM SGT** (~35 hours)

## Strategy
Build a `smart_money_pulse.py` agent that:
1. Runs periodic scans via `nansen research smart-money netflow`
2. Identifies tokens with biggest smart money flows
3. Cross-references with Nansen labels (wallets, funds)
4. Generates a ranked "Top Smart Money Moves" report
5. Sends alerts via AgentMail
6. Posts to X

## Contest Judging
- Creativity (originality of the build)
- Usefulness (solves a real problem)
- Technical depth (demonstrates API capability)
- Presentation clarity (clear demo value)

## Credits (30 remaining)
- 5 credits per netflow query
- Use sparingly — save for demo day

## Key Files
- `smart_money_pulse.py` — Main agent
- `pulse_dashboard.md` — Live dashboard output
- `hackathon_demo.sh` — One-command demo
- `README.md` — Submission README
