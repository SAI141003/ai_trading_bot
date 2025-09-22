# 📁 exit_trades.py — Auto exit + PnL calculation from trade_logs.csv

import pandas as pd
import datetime
import os
from dhan_api import get_ltp, place_market_order
import json

# 🔧 Load config
with open("config.json") as f:
    config = json.load(f)

DRY_RUN = config.get("dry_run", True)

# 🛎️ macOS popup (optional)
def notify(title, message):
    os.system(f'''osascript -e 'display notification "{message}" with title "{title}"' ''')

log_file = "trade_logs.csv"
exit_log_file = "exit_trades.csv"

if not os.path.exists(log_file):
    print("❌ No trades to exit.")
    exit()

print("🔍 Reading trade logs...")
df = pd.read_csv(log_file)

# Remove trades already exited (if any)
if os.path.exists(exit_log_file):
    exited_df = pd.read_csv(exit_log_file)
    df = df[~df['security_id'].isin(exited_df['security_id'])]

if df.empty:
    print("✅ No open trades to exit.")
    exit()

exit_data = []
for _, row in df.iterrows():
    symbol = row['symbol']
    sec_id = str(row['security_id'])
    option_type = row['type']
    strike = row['strike']

    ltp = get_ltp(sec_id)
    if not ltp:
        print(f"❌ Failed to fetch LTP for {symbol}")
        continue

    entry_price = None  # Optional: store entry price in logs
    qty = 50  # default lot size
    
    print(f"📤 Exiting {symbol} @ ₹{ltp}...")
    
    if DRY_RUN:
        print(f"[Dry Run] Would place SELL order for {symbol}")
        notify("Dry Exit", f"{symbol} exited at ₹{ltp}")
    else:
        place_market_order(sec_id, "NFO", "OPTIDX", "SELL", qty)
        notify("✅ Exited Position", f"{symbol} @ ₹{ltp}")

    exit_data.append({
        "timestamp": datetime.datetime.now(),
        "symbol": symbol,
        "security_id": sec_id,
        "exit_price": ltp,
        "option_type": option_type,
        "strike": strike
    })

if exit_data:
    pd.DataFrame(exit_data).to_csv(exit_log_file, mode='a', index=False, header=not os.path.exists(exit_log_file))
    print("📦 All trades exited and logged to exit_trades.csv")
else:
    print("⚠️ No trades exited.")

