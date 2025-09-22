#!/bin/bash

echo "🚀 Starting AI Trading Bot Auto Scheduler..."
cd "$(dirname "$0")"

nohup python3 auto_scheduler.py > scheduler_output.log 2>&1 &
echo "🕒 Bot is now running in background."

