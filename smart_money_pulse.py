#!/usr/bin/env python3
"""
Smart Money Pulse Monitor
=========================
An AI agent that tracks smart money flows on Base and generates ranked reports.

Usage:
    export NANSEN_API_KEY="your_key_here"
    python3 smart_money_pulse.py

Features:
- Fetches smart money netflow data from Nansen API
- Cross-references with trending tokens
- Generates ranked "Top 10 Smart Money Moves" report
- Saves results to pulse_dashboard.md
"""

import subprocess
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Configuration
DASHBOARD_FILE = "pulse_dashboard.md"
MIN_FLOW_THRESHOLD = 50000  # $50K minimum flow to report

class SmartMoneyPulse:
    """Smart Money Pulse Monitor Agent"""
    
    def __init__(self):
        self.api_key = os.environ.get("NANSEN_API_KEY")
        if not self.api_key:
            print("❌ Error: NANSEN_API_KEY environment variable not set")
            print("   Run: export NANSEN_API_KEY='your_key'")
            sys.exit(1)
        
        self.smart_money_data: List[Dict] = []
        self.token_data: List[Dict] = []
        self.cross_referenced: List[Dict] = []
        
    def run_command(self, cmd: List[str]) -> Optional[Dict]:
        """Execute a nansen CLI command and return parsed JSON."""
        try:
            # Set API key in environment for the subprocess
            env = os.environ.copy()
            env["NANSEN_API_KEY"] = self.api_key
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                timeout=120
            )
            
            if result.returncode != 0:
                print(f"⚠️  Command failed: {result.stderr}")
                return None
                
            # Parse JSON output
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                # Try to extract JSON from mixed output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and line.startswith('{'):
                        try:
                            return json.loads(line)
                        except:
                            continue
                print("⚠️  Could not parse JSON response")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  Command timed out: {' '.join(cmd)}")
            return None
        except Exception as e:
            print(f"⚠️  Error running command: {e}")
            return None
    
    def fetch_smart_money_netflow(self, chain: str = "base", timeframe: str = "24h") -> List[Dict]:
        """Fetch smart money netflow data from Nansen."""
        print(f"📊 Fetching smart money netflow for {chain} ({timeframe})...")
        
        cmd = [
            "nansen", "research", "smart-money", "netflow",
            "--chain", chain,
            "--timeframe", timeframe
        ]
        
        data = self.run_command(cmd)
        
        if data and isinstance(data, dict):
            # Extract flows from response
            flows = data.get("data", data.get("flows", data.get("results", [])))
            if isinstance(flows, list):
                self.smart_money_data = flows
                print(f"   ✅ Retrieved {len(flows)} smart money flows")
                return flows
        
        print("   ⚠️  Using fallback data (API credits may be exhausted)")
        return []
    
    def fetch_token_screener(self, chain: str = "base", timeframe: str = "24h") -> List[Dict]:
        """Fetch trending tokens from Nansen token screener."""
        print(f"🔍 Fetching trending tokens for {chain} ({timeframe})...")
        
        cmd = [
            "nansen", "research", "token", "screener",
            "--chain", chain,
            "--timeframe", timeframe
        ]
        
        data = self.run_command(cmd)
        
        if data and isinstance(data, dict):
            # Extract tokens from response
            tokens = data.get("data", data.get("tokens", data.get("results", [])))
            if isinstance(tokens, list):
                self.token_data = tokens
                print(f"   ✅ Retrieved {len(tokens)} trending tokens")
                return tokens
        
        print("   ⚠️  Using fallback data (API credits may be exhausted)")
        return []
    
    def cross_reference_data(self) -> List[Dict]:
        """Cross-reference smart money flows with trending tokens."""
        print("🔗 Cross-referencing smart money with token trends...")
        
        combined = []
        
        # Create token lookup by symbol/address
        token_lookup = {}
        for token in self.token_data:
            symbol = token.get("symbol", "").upper()
            address = token.get("address", "").lower()
            if symbol:
                token_lookup[symbol] = token
            if address:
                token_lookup[address] = token
        
        # Match smart money flows with token data
        for flow in self.smart_money_data:
            symbol = flow.get("symbol", flow.get("token_symbol", "")).upper()
            address = flow.get("token_address", "").lower()
            
            matched_token = None
            if symbol in token_lookup:
                matched_token = token_lookup[symbol]
            elif address in token_lookup:
                matched_token = token_lookup[address]
            
            # Calculate smart money score
            netflow = float(flow.get("netflow", flow.get("net_flow", 0)))
            inflow = float(flow.get("inflow", 0))
            outflow = float(flow.get("outflow", 0))
            
            # Skip if below threshold
            if abs(netflow) < MIN_FLOW_THRESHOLD:
                continue
            
            entry = {
                "symbol": symbol,
                "name": matched_token.get("name", flow.get("name", symbol)) if matched_token else flow.get("name", symbol),
                "address": address or flow.get("address", ""),
                "netflow": netflow,
                "inflow": inflow,
                "outflow": outflow,
                "price_change_24h": matched_token.get("price_change_24h", 0) if matched_token else 0,
                "volume_24h": matched_token.get("volume_24h", matched_token.get("volume", 0)) if matched_token else 0,
                "market_cap": matched_token.get("market_cap", 0) if matched_token else 0,
                "smart_money_score": self._calculate_score(netflow, inflow, outflow, matched_token),
                "signal": "ACCUMULATING" if netflow > 0 else "DISTRIBUTING"
            }
            combined.append(entry)
        
        # Sort by smart money score (descending)
        combined.sort(key=lambda x: x["smart_money_score"], reverse=True)
        
        self.cross_referenced = combined
        print(f"   ✅ Identified {len(combined)} significant smart money moves")
        return combined
    
    def _calculate_score(self, netflow: float, inflow: float, outflow: float, token: Optional[Dict]) -> float:
        """Calculate a composite smart money score."""
        # Base score from netflow magnitude
        score = abs(netflow) / 10000  # Scale down
        
        # Bonus for accumulation vs distribution
        if netflow > 0:
            score *= 1.2  # Accumulation gets bonus
        
        # Volume ratio factor
        if token and token.get("volume_24h"):
            volume = float(token.get("volume_24h", 1))
            if volume > 0:
                flow_ratio = abs(netflow) / volume
                score += flow_ratio * 100
        
        return round(score, 2)
    
    def generate_dashboard(self, top_n: int = 10) -> str:
        """Generate the markdown dashboard report."""
        print(f"📝 Generating dashboard report (top {top_n})...")
        
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        
        md = f"""# 🧠 Smart Money Pulse Monitor

**Generated:** {now}  
**Chain:** Base  
**Timeframe:** 24h  
**Data Source:** Nansen Research API

---

## 📊 Executive Summary

| Metric | Value |
|--------|-------|
| Smart Money Flows Tracked | {len(self.smart_money_data)} |
| Trending Tokens Analyzed | {len(self.token_data)} |
| Significant Moves Identified | {len(self.cross_referenced)} |
| Accumulating Signals | {sum(1 for x in self.cross_referenced if x['signal'] == 'ACCUMULATING')} |
| Distributing Signals | {sum(1 for x in self.cross_referenced if x['signal'] == 'DISTRIBUTING')} |

---

## 🏆 Top {top_n} Smart Money Moves

"""
        
        top_moves = self.cross_referenced[:top_n]
        
        for i, move in enumerate(top_moves, 1):
            signal_emoji = "🟢" if move["signal"] == "ACCUMULATING" else "🔴"
            netflow_formatted = f"${abs(move['netflow']):,.0f}"
            direction = "+" if move["netflow"] > 0 else "-"
            
            md += f"""### {i}. {move['symbol']} — {move['name']}

| Metric | Value |
|--------|-------|
| Signal | {signal_emoji} **{move['signal']}** |
| Net Flow | {direction}{netflow_formatted} |
| Inflow | ${move['inflow']:,.0f} |
| Outflow | ${move['outflow']:,.0f} |
| 24h Price Change | {move['price_change_24h']:+.2f}% |
| 24h Volume | ${move['volume_24h']:,.0f} |
| Market Cap | ${move['market_cap']:,.0f} |
| Smart Score | ⭐ {move['smart_money_score']:.1f} |

**Token Address:** `{move['address'] or 'N/A'}`

---

"""
        
        # Add insights section
        md += """## 💡 Key Insights

"""
        
        # Top accumulations
        accumulators = [x for x in top_moves if x["signal"] == "ACCUMULATING"][:5]
        if accumulators:
            md += "### 🟢 Most Accumulated (Smart Money Buying)\n\n"
            for token in accumulators:
                md += f"- **{token['symbol']}**: ${token['netflow']:,.0f} net inflow\n"
            md += "\n"
        
        # Top distributions
        distributors = [x for x in top_moves if x["signal"] == "DISTRIBUTING"][:5]
        if distributors:
            md += "### 🔴 Most Distributed (Smart Money Selling)\n\n"
            for token in distributors:
                md += f"- **{token['symbol']}**: ${abs(token['netflow']):,.0f} net outflow\n"
            md += "\n"
        
        # Methodology
        md += """## 🔬 Methodology

This report is generated by cross-referencing:
1. **Smart Money Netflow** — Tracks flows from Nansen-labeled smart money wallets
2. **Token Screener** — Identifies trending tokens with significant volume
3. **Composite Scoring** — Ranks tokens by flow magnitude, direction, and volume ratio

### Smart Money Score Calculation
- Base score from absolute netflow value
- 20% bonus for accumulation (buying) signals
- Volume ratio factor (flow relative to total volume)
- Higher scores indicate more significant smart money activity

---

*Generated by Smart Money Pulse Monitor — Powered by Nansen CLI* 🦈
"""
        
        return md
    
    def save_dashboard(self, content: str) -> None:
        """Save the dashboard to file."""
        with open(DASHBOARD_FILE, 'w') as f:
            f.write(content)
        print(f"   ✅ Dashboard saved to {DASHBOARD_FILE}")
    
    def run(self) -> str:
        """Execute the full pulse monitor workflow."""
        print("=" * 60)
        print("🚀 Smart Money Pulse Monitor Starting...")
        print("=" * 60)
        print()
        
        # Fetch data
        self.fetch_smart_money_netflow("base", "24h")
        self.fetch_token_screener("base", "24h")
        
        # Cross-reference
        self.cross_reference_data()
        
        # Generate and save dashboard
        dashboard = self.generate_dashboard(top_n=10)
        self.save_dashboard(dashboard)
        
        print()
        print("=" * 60)
        print("✅ Smart Money Pulse Complete!")
        print(f"📄 Report saved: {DASHBOARD_FILE}")
        print("=" * 60)
        
        return dashboard


def main():
    """Main entry point."""
    pulse = SmartMoneyPulse()
    dashboard = pulse.run()
    
    # Print a summary to console
    print("\n📊 DASHBOARD PREVIEW:\n")
    print("-" * 60)
    # Print first 2000 chars of dashboard
    preview = dashboard[:2000] + "..." if len(dashboard) > 2000 else dashboard
    print(preview)
    print("-" * 60)


if __name__ == "__main__":
    main()
