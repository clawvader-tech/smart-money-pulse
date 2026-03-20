#!/usr/bin/env python3
"""
Smart Money Pulse — Agent Tool
Fetches top trading signals from the Smart Money Pulse CLI.
"""
import json
import subprocess
import sys
import os

def get_signals(chain: str = "base", top_n: int = 5, format: str = "json"):
    """
    Get top smart money signals for a chain.
    
    Args:
        chain: One of base, ethereum, solana, arbitrum, optimism
        top_n: Number of signals to return
        format: json or text
    """
    cmd = [
        sys.executable, "smart_money_pulse.py",
        "--chain", chain,
        "--top-n", str(top_n),
        "--format", format
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if result.returncode != 0:
        return {"error": result.stderr}
    if format == "json":
        try:
            return json.loads(result.stdout)
        except:
            return {"raw": result.stdout}
    return {"output": result.stdout}

def get_positions():
    """Get current open positions."""
    # MCP server would be used here in production
    return {"status": "connect_to_mcp_server"}

def main():
    if len(sys.argv) < 2:
        print("Usage: smart_money_signals.py <chain> [top_n]")
        sys.exit(1)
    
    chain = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    result = get_signals(chain, top_n)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
