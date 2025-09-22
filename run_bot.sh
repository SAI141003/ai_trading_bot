#!/bin/bash

# 📦 run_bot.sh — One-click launcher for your AI trading bot
# ✅ Starts auto-scheduler to run main.py and exit_trades.py daily

# 🚀 Navigate to bot folder
cd "$(dirname "$0")"

# ✅ Activate virtualenv if used (optional)
# source venv/bin/activate

# ⏱️ Start the auto scheduler
nohup python3 auto_scheduler.py > scheduler.log 2>&1 &

echo "✅ Bot started in background. Logs: scheduler.log"


