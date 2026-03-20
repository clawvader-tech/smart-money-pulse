#!/bin/bash
# Smart Money Pulse Monitor — Hackathon Demo Script
# ==================================================
# 
# This script runs the full Smart Money Pulse Monitor
# and displays the results in a beautiful format.
#
# Usage:
#   chmod +x hackathon_demo.sh
#   ./hackathon_demo.sh

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║           🧠 SMART MONEY PULSE MONITOR 🦈                    ║"
echo "║                                                              ║"
echo "║     Nansen CLI Build Challenge — Week 1 Submission           ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check for NANSEN_API_KEY
if [ -z "$NANSEN_API_KEY" ]; then
    echo "⚠️  NANSEN_API_KEY not set in environment"
    echo "   Using demo mode with sample data..."
    echo ""
fi

# Run the pulse monitor
echo "🚀 Starting Smart Money Pulse Monitor..."
echo "─────────────────────────────────────────────────────────────"
echo ""

python3 smart_money_pulse.py

echo ""
echo "─────────────────────────────────────────────────────────────"
echo ""

# Display the dashboard
echo "📊 DISPLAYING DASHBOARD:"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

if [ -f "pulse_dashboard.md" ]; then
    cat pulse_dashboard.md
else
    echo "❌ Dashboard file not found!"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Stats
echo "✅ DEMO COMPLETE!"
echo ""
echo "📁 Files Generated:"
echo "   • pulse_dashboard.md — Full markdown report"
echo ""
echo "📊 Nansen API Usage:"
echo "   • Smart Money Netflow Query: 5 credits"
echo "   • Token Screener Query: 1 credit"
echo "   • Total: 6 credits per run"
echo ""
echo "🔗 Share your results:"
echo "   Post to X with #NansenCLI @nansen_ai"
echo ""
