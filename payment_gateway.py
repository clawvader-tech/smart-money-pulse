#!/usr/bin/env python3
"""
Project Atlas x402 Payment Gateway
Implements x402/TPP protocol for agent payments for Atlas data
"""

import hashlib
import hmac
import json
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Configuration
BASE_CHAIN_ID = 8453  # Base Mainnet
USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC on Base
GATEWAY_PORT = 8080

# Price configuration (in USDC)
TPP_PRICES = {
    "signals": 0.01,        # $0.01 per signals request
    "signals_premium": 0.03,  # $0.03 for premium signals
    "augment": 0.05,       # $0.05 for Nansen-augmented data
}

# Rate limiting (free tier)
FREE_TIER_CALLS = 10
FREE_TIER_WINDOW = 3600  # 1 hour in seconds

# In-memory rate limit storage (use Redis in production)
rate_limits = {}


def get_client_id() -> str:
    """Get unique client identifier from request."""
    # Try to get from headers, fallback to IP
    client_id = request.headers.get("X-Client-ID") or request.headers.get("X-Forwarded-For", "unknown")
    if "," in client_id:
        client_id = client_id.split(",")[0].strip()
    return client_id


def check_rate_limit(client_id: str) -> tuple[bool, int]:
    """
    Check if client has exceeded free tier rate limit.
    Returns (allowed, remaining_calls)
    """
    now = time.time()
    
    if client_id not in rate_limits:
        rate_limits[client_id] = {
            "calls": [],
            "paid": False
        }
    
    client_data = rate_limits[client_id]
    
    # Clean old calls outside the window
    client_data["calls"] = [
        t for t in client_data["calls"] 
        if now - t < FREE_TIER_WINDOW
    ]
    
    if client_data["paid"]:
        return True, 999  # Unlimited for paid users
    
    call_count = len(client_data["calls"])
    remaining = max(0, FREE_TIER_CALLS - call_count)
    
    if call_count >= FREE_TIER_CALLS:
        return False, 0
    
    # Record this call
    client_data["calls"].append(now)
    return True, remaining


def check_x402_payment(headers: dict) -> tuple[bool, dict]:
    """
    Validate x402 payment header.
    Expected format: WWW-Authorization: Pay-Token <token_data>
    
    Returns (is_valid, payment_data)
    """
    auth_header = headers.get("WWW-Authorization") or headers.get("Authorization")
    
    if not auth_header:
        return False, {"error": "No payment header"}
    
    if not auth_header.startswith("Pay-Token "):
        return False, {"error": "Invalid payment format. Use: Pay-Token <token>"}
    
    token_data = auth_header[10:]  # Remove "Pay-Token " prefix
    
    try:
        # Parse token (in production, verify cryptographic signature)
        # Format: base64 encoded JSON with payment details
        import base64
        payment_info = json.loads(base64.b64decode(token_data))
        
        # Verify payment details
        required_fields = ["amount", "currency", "chain", "timestamp"]
        for field in required_fields:
            if field not in payment_info:
                return False, {"error": f"Missing field: {field}"}
        
        # Check if payment is recent (within 5 minutes)
        payment_time = payment_info.get("timestamp", 0)
        if abs(time.time() - payment_time) > 300:
            return False, {"error": "Payment token expired"}
        
        # Verify amount
        amount = float(payment_info.get("amount", 0))
        if amount < TPP_PRICES["signals"]:
            return False, {"error": f"Insufficient payment. Required: {TPP_PRICES['signals']} USDC"}
        
        return True, payment_info
        
    except Exception as e:
        return False, {"error": f"Invalid payment token: {str(e)}"}


def get_tpp_price(endpoint: str = "signals") -> dict:
    """
    Get the Third-Party Paymaster (TPP) price in USDC on Base.
    """
    price = TPP_PRICES.get(endpoint, TPP_PRICES["signals"])
    
    return {
        "endpoint": endpoint,
        "price_usdc": price,
        "currency": "USDC",
        "chain": "Base",
        "chain_id": BASE_CHAIN_ID,
        "token_address": USDC_ADDRESS,
        "instructions": "Include payment in WWW-Authorization header"
    }


def require_payment(endpoint: str):
    """Decorator to require x402 payment for an endpoint."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_id = get_client_id()
            
            # Check rate limit first
            allowed, remaining = check_rate_limit(client_id)
            
            # Check for x402 payment
            is_paid, payment_data = check_x402_payment(dict(request.headers))
            
            if is_paid:
                # Mark client as paid
                rate_limits[client_id]["paid"] = True
                request.payment_data = payment_data
                return f(*args, **kwargs)
            
            if not allowed:
                # Return 402 Payment Required
                price_info = get_tpp_price(endpoint)
                response = jsonify({
                    "error": "Rate limit exceeded",
                    "message": f"Free tier limit reached ({FREE_TIER_CALLS} calls/hour)",
                    "required_payment": price_info,
                    "www_authenticate": f'Pay-Token price="{price_info["price_usdc"]}", chain="{price_info["chain"]}"'
                })
                response.status_code = 402
                response.headers["WWW-Authenticate"] = f'Pay-Token price="{price_info["price_usdc"]}", chain="{price_info["chain"]}"'
                return response
            
            # Free tier - add rate limit headers
            request.remaining_calls = remaining
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


# ============================================================================
# API Endpoints
# ============================================================================

@app.route("/api/v1/signals", methods=["GET"])
@require_payment("signals")
def get_signals():
    """
    Get trading signals from Project Atlas.
    
    Free tier: 10 calls/hour
    Paid: Requires x402 payment header
    """
    # Get optional parameters
    chain = request.args.get("chain", "base")
    limit = int(request.args.get("limit", 10))
    
    # Generate signals data
    signals = [
        {
            "rank": i + 1,
            "token": token["symbol"],
            "name": token["name"],
            "chain": chain,
            "action": token["action"],
            "confidence": token["confidence"],
            "flow_usd": token["flow"],
            "smart_money_status": token["smart_money"],
            "timestamp": token["timestamp"]
        }
        for i, token in enumerate(get_sample_signals()[:limit])
    ]
    
    response = {
        "success": True,
        "data": signals,
        "meta": {
            "source": "Project Atlas",
            "chain": chain,
            "count": len(signals),
            "payment_type": "paid" if hasattr(request, 'payment_data') else "free_tier",
            "remaining_calls": getattr(request, 'remaining_calls', None),
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    return jsonify(response)


@app.route("/api/v1/augment", methods=["POST"])
@require_payment("augment")
def augment_signals():
    """
    Get Nansen-augmented signals.
    Costs 5 Nansen credits per request.
    Requires x402 payment.
    """
    data = request.get_json() or {}
    tokens = data.get("tokens", [])
    
    if not tokens:
        return jsonify({"error": "No tokens provided"}), 400
    
    # In production, this would call Nansen API
    # For demo, return augmented data
    augmented = []
    for token in tokens[:10]:
        augmented.append({
            "token": token.upper() if isinstance(token, str) else token.get("symbol", "UNKNOWN"),
            "nansen_data": {
                "smart_money_holdings": 2450000 + (hash(token) % 1000000),
                "whale_transactions_24h": 12 + (hash(token) % 20),
                "portfolio_ concentration": 0.15 + (hash(token) % 10) / 100,
                "avg_entry_price": 12.50 + (hash(token) % 50),
                "labels": ["whale", "smart_money", "early_investor"],
                "last_active": "2 hours ago"
            },
            "signal_score": 85 + (hash(token) % 15),
            "recommendation": "BUY" if hash(token) % 2 == 0 else "HOLD",
            "nansen_credits_used": 5
        })
    
    response = {
        "success": True,
        "data": augmented,
        "meta": {
            "source": "Nansen API (via Project Atlas)",
            "credits_used": len(augmented) * 5,
            "payment_type": "paid",
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    return jsonify(response)


@app.route("/api/v1/price", methods=["GET"])
def get_price():
    """Get TPP pricing information."""
    endpoint = request.args.get("endpoint", "signals")
    return jsonify(get_tpp_price(endpoint))


@app.route("/api/v1/rate-limit", methods=["GET"])
def get_rate_limit():
    """Get current rate limit status for client."""
    client_id = get_client_id()
    allowed, remaining = check_rate_limit(client_id)
    
    return jsonify({
        "client_id": client_id[:8] + "..." if len(client_id) > 8 else client_id,
        "remaining_calls": remaining,
        "limit": FREE_TIER_CALLS,
        "window_seconds": FREE_TIER_WINDOW,
        "is_paid": rate_limits.get(client_id, {}).get("paid", False)
    })


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Project Atlas Payment Gateway",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })


# ============================================================================
# Helper Functions
# ============================================================================

def get_sample_signals():
    """Generate sample trading signals."""
    return [
        {
            "symbol": "HYPE",
            "name": "Hyperliquid",
            "action": "BUY",
            "confidence": 94,
            "flow": 2400000,
            "smart_money": "accumulating",
            "timestamp": (datetime.utcnow() - timedelta(minutes=2)).isoformat()
        },
        {
            "symbol": "TAO",
            "name": "Bittensor",
            "action": "BUY",
            "confidence": 89,
            "flow": 1800000,
            "smart_money": "accumulating",
            "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat()
        },
        {
            "symbol": "PENGU",
            "name": "Pudgy Penguins",
            "action": "BUY",
            "confidence": 85,
            "flow": 1200000,
            "smart_money": "accumulating",
            "timestamp": (datetime.utcnow() - timedelta(minutes=8)).isoformat()
        },
        {
            "symbol": "BTC",
            "name": "Bitcoin",
            "action": "SELL",
            "confidence": 78,
            "flow": -890000,
            "smart_money": "distributing",
            "timestamp": (datetime.utcnow() - timedelta(minutes=12)).isoformat()
        },
        {
            "symbol": "ETH",
            "name": "Ethereum",
            "action": "BUY",
            "confidence": 72,
            "flow": 650000,
            "smart_money": "accumulating",
            "timestamp": (datetime.utcnow() - timedelta(minutes=15)).isoformat()
        },
        {
            "symbol": "AAVE",
            "name": "Aave",
            "action": "SELL",
            "confidence": 68,
            "flow": -420000,
            "smart_money": "distributing",
            "timestamp": (datetime.utcnow() - timedelta(minutes=18)).isoformat()
        }
    ]


def generate_payment_token(amount: float, currency: str = "USDC") -> str:
    """
    Generate a payment token (for demo purposes).
    In production, this would be signed by a payment contract.
    """
    import base64
    
    token_data = {
        "amount": amount,
        "currency": currency,
        "chain": "Base",
        "chain_id": BASE_CHAIN_ID,
        "recipient": "0xProjectAtlasAddress",
        "timestamp": time.time(),
        "nonce": hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
    }
    
    return base64.b64encode(json.dumps(token_data).encode()).decode()


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🧠 Project Atlas - x402 Payment Gateway                         ║
║   ─────────────────────────────────                               ║
║                                                                   ║
║   Server running on: http://localhost:{GATEWAY_PORT}                   ║
║                                                                   ║
║   Endpoints:                                                      ║
║   • GET  /api/v1/signals    - Trading signals (10 free/hr)      ║
║   • POST /api/v1/augment    - Nansen-augmented data (paid)      ║
║   • GET  /api/v1/price      - Get TPP pricing                    ║
║   • GET  /api/v1/rate-limit - Check rate limit status            ║
║   • GET  /health            - Health check                        ║
║                                                                   ║
║   x402 Payment:                                                  ║
║   Include header: WWW-Authorization: Pay-Token <base64_token>    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host="0.0.0.0", port=GATEWAY_PORT, debug=False)
