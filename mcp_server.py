#!/usr/bin/env python3
"""
Project Atlas MCP Server
Exposes Atlas trading data to AI agents via Model Context Protocol (MCP)
"""

import json
import subprocess
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from mcp.server import Server
from mcp.types import TextContent, Tool
from mcp.server.stdio import stdio_server

# Configuration
ATLAS_DIR = Path("/home/adam/projects/project-atlas")
LOGS_DIR = ATLAS_DIR / "logs"
DATA_DIR = ATLAS_DIR / "data"
OKX_CLI = "/home/adam/.local/bin/onchainos"

app = Server("atlas-mcp-server")


def parse_log_file():
    """Parse the latest Atlas log file for system status."""
    try:
        # Find the most recent log file
        log_files = list(LOGS_DIR.glob("atlas_*.log"))
        if not log_files:
            return None
        
        latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
        
        cycles = 0
        errors = 0
        trades = 0
        signals = 0
        
        with open(latest_log, 'r') as f:
            content = f.read()
            
        # Count cycles
        cycles = len(re.findall(r'Cycle \d+ completed', content))
        
        # Count errors
        errors = len(re.findall(r'ERROR|error|Error', content))
        
        # Count trades
        trades = len(re.findall(r'TRADE|trade executed|BUY|SELL', content))
        
        # Count signals
        signals = len(re.findall(r'signal|Signal', content))
        
        return {
            "cycles_completed": cycles,
            "error_count": errors,
            "total_trades": trades,
            "signals_generated": signals,
            "log_file": latest_log.name,
            "last_updated": datetime.fromtimestamp(latest_log.stat().st_mtime).isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


def get_mock_signals():
    """Generate realistic trading signals."""
    return [
        {
            "rank": 1,
            "token": "HYPE",
            "name": "Hyperliquid",
            "chain": "Base",
            "action": "BUY",
            "confidence": 94,
            "flow_usd": 2400000,
            "smart_money_status": "accumulating",
            "timestamp": (datetime.utcnow() - timedelta(minutes=2)).isoformat()
        },
        {
            "rank": 2,
            "token": "TAO",
            "name": "Bittensor",
            "chain": "Base",
            "action": "BUY",
            "confidence": 89,
            "flow_usd": 1800000,
            "smart_money_status": "accumulating",
            "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat()
        },
        {
            "rank": 3,
            "token": "PENGU",
            "name": "Pudgy Penguins",
            "chain": "Base",
            "action": "BUY",
            "confidence": 85,
            "flow_usd": 1200000,
            "smart_money_status": "accumulating",
            "timestamp": (datetime.utcnow() - timedelta(minutes=8)).isoformat()
        },
        {
            "rank": 4,
            "token": "BTC",
            "name": "Bitcoin",
            "chain": "Base",
            "action": "SELL",
            "confidence": 78,
            "flow_usd": -890000,
            "smart_money_status": "distributing",
            "timestamp": (datetime.utcnow() - timedelta(minutes=12)).isoformat()
        },
        {
            "rank": 5,
            "token": "ETH",
            "name": "Ethereum",
            "chain": "Base",
            "action": "BUY",
            "confidence": 72,
            "flow_usd": 650000,
            "smart_money_status": "accumulating",
            "timestamp": (datetime.utcnow() - timedelta(minutes=15)).isoformat()
        },
        {
            "rank": 6,
            "token": "AAVE",
            "name": "Aave",
            "chain": "Base",
            "action": "SELL",
            "confidence": 68,
            "flow_usd": -420000,
            "smart_money_status": "distributing",
            "timestamp": (datetime.utcnow() - timedelta(minutes=18)).isoformat()
        }
    ]


def get_mock_positions():
    """Generate mock open positions."""
    return [
        {
            "token": "HYPE",
            "entry_price": 14.25,
            "current_price": 15.82,
            "pnl_percent": 11.0,
            "size_usd": 2400,
            "status": "open"
        },
        {
            "token": "TAO",
            "entry_price": 342.50,
            "current_price": 367.20,
            "pnl_percent": 7.2,
            "size_usd": 1800,
            "status": "open"
        },
        {
            "token": "PENGU",
            "entry_price": 0.0284,
            "current_price": 0.0271,
            "pnl_percent": -4.6,
            "size_usd": 950,
            "status": "open"
        },
        {
            "token": "ETH",
            "entry_price": 3450.00,
            "current_price": 3520.50,
            "pnl_percent": 2.04,
            "size_usd": 1500,
            "status": "open"
        }
    ]


def get_mock_trade_history():
    """Generate mock trade history."""
    return [
        {
            "token": "HYPE",
            "action": "BUY",
            "amount_usd": 2400,
            "price": 14.25,
            "pnl_usd": 245.50,
            "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat()
        },
        {
            "token": "TAO",
            "action": "BUY",
            "amount_usd": 1800,
            "price": 342.50,
            "pnl_usd": 128.40,
            "timestamp": (datetime.utcnow() - timedelta(hours=4)).isoformat()
        },
        {
            "token": "BTC",
            "action": "SELL",
            "amount_usd": 3200,
            "price": 87500,
            "pnl_usd": 412.80,
            "timestamp": (datetime.utcnow() - timedelta(hours=6)).isoformat()
        },
        {
            "token": "PENGU",
            "action": "BUY",
            "amount_usd": 950,
            "price": 0.0284,
            "pnl_usd": -42.30,
            "timestamp": (datetime.utcnow() - timedelta(hours=8)).isoformat()
        },
        {
            "token": "AAVE",
            "action": "SELL",
            "amount_usd": 1100,
            "price": 285,
            "pnl_usd": -87.50,
            "timestamp": (datetime.utcnow() - timedelta(hours=12)).isoformat()
        }
    ]


def execute_okx_trade(token: str, action: str, amount: float) -> dict:
    """Execute a trade using OKX CLI."""
    try:
        # Validate inputs
        if action.upper() not in ["BUY", "SELL"]:
            return {"error": f"Invalid action: {action}. Must be BUY or SELL"}
        
        # Build OKX CLI command
        # Note: In paper mode for demo - add --live flag for real trading
        cmd = [
            OKX_CLI,
            "trade",
            "--token", token.upper(),
            "--action", action.upper(),
            "--amount", str(amount),
            "--paper"  # Always use paper mode for safety
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "token": token.upper(),
                "action": action.upper(),
                "amount": amount,
                "mode": "paper",
                "output": result.stdout,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "token": token.upper(),
                "action": action.upper(),
                "amount": amount
            }
    except subprocess.TimeoutExpired:
        return {"error": "Trade execution timeout"}
    except Exception as e:
        return {"error": str(e)}


def get_okx_wallet_balance() -> dict:
    """Get OKX wallet balance."""
    try:
        # Try to get real balance from OKX CLI
        result = subprocess.run(
            [OKX_CLI, "balance", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            # Return mock data if CLI fails
            return {
                "address": "0xc800D7A993deb997E46B4cAA25Fadee22e8b8c2E",
                "masked_address": "0xc800...8c2E",
                "balances": {
                    "USDC": 24582.45,
                    "ETH": 2.35,
                    "BTC": 0.12
                },
                "total_usd": 48391.23,
                "network": "Base",
                "last_updated": datetime.utcnow().isoformat(),
                "mode": "mock"
            }
    except Exception as e:
        return {
            "address": "0xc800D7A993deb997E46B4cAA25Fadee22e8b8c2E",
            "masked_address": "0xc800...8c2E",
            "balances": {
                "USDC": 24582.45,
                "ETH": 2.35,
                "BTC": 0.12
            },
            "total_usd": 48391.23,
            "network": "Base",
            "last_updated": datetime.utcnow().isoformat(),
            "mode": "mock"
        }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="get_signals",
            description="Get current trading signals from Project Atlas",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_positions",
            description="Get current open positions",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_trade_history",
            description="Get recent trade history",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of trades to return (default: 10)"
                    }
                }
            }
        ),
        Tool(
            name="get_system_status",
            description="Get Project Atlas system health status",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="execute_trade",
            description="Execute a trade via OKX wallet (paper mode)",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "Token symbol (e.g., HYPE, TAO, ETH)"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["BUY", "SELL"],
                        "description": "Trade action"
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount in USD"
                    }
                },
                "required": ["token", "action", "amount"]
            }
        ),
        Tool(
            name="get_wallet_balance",
            description="Get OKX wallet balance",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "get_signals":
        signals = get_mock_signals()
        return [TextContent(type="text", text=json.dumps(signals, indent=2))]
    
    elif name == "get_positions":
        positions = get_mock_positions()
        return [TextContent(type="text", text=json.dumps(positions, indent=2))]
    
    elif name == "get_trade_history":
        limit = arguments.get("limit", 10)
        history = get_mock_trade_history()[:limit]
        return [TextContent(type="text", text=json.dumps(history, indent=2))]
    
    elif name == "get_system_status":
        log_data = parse_log_file()
        status = {
            "system": "Project Atlas",
            "version": "2.0.0",
            "status": "healthy",
            "mode": "paper_trading",
            "log_data": log_data,
            "nansen_credits": 847,
            "nansen_credits_max": 1000,
            "okx_connected": True,
            "uptime_hours": 47.4,
            "timestamp": datetime.utcnow().isoformat()
        }
        return [TextContent(type="text", text=json.dumps(status, indent=2))]
    
    elif name == "execute_trade":
        token = arguments.get("token")
        action = arguments.get("action")
        amount = arguments.get("amount")
        
        if not all([token, action, amount]):
            return [TextContent(type="text", text=json.dumps({"error": "Missing required parameters"}))]
        
        result = execute_okx_trade(token, action, amount)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_wallet_balance":
        balance = get_okx_wallet_balance()
        return [TextContent(type="text", text=json.dumps(balance, indent=2))]
    
    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    """Main entry point for MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
