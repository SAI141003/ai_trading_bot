# 📁 auto_scheduler.py
# Schedule your trading bot to run at specific times

import schedule
import time
import subprocess
from datetime import datetime

# Define your time triggers (24-hour format)
TRADE_TIME = "09:20"
EXIT_TIME = "15:15"


def run_main_trade():
    print(f"\n🚀 Running main.py at {datetime.now().strftime('%H:%M:%S')}...")
    subprocess.call(["python3", "main.py"])

def run_exit_logger():
    print(f"\n💼 Running exit_trades.py at {datetime.now().strftime('%H:%M:%S')}...")
    subprocess.call(["python3", "exit_trades.py"])


# Schedule jobs
schedule.every().day.at(TRADE_TIME).do(run_main_trade)
schedule.every().day.at(EXIT_TIME).do(run_exit_logger)

print("🕒 Auto Scheduler Started")
print(f"📆 Will run main.py at {TRADE_TIME} and exit_trades.py at {EXIT_TIME} each day.")

# Keep script running
while True:
    schedule.run_pending()
    time.sleep(30)

