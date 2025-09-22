# 📁 main.py — AI Trading Bot (BANKNIFTY/NIFTY + Clean LTP + ATM Fix)

import os
import json
import pandas as pd
import yfinance as yf
import joblib
import datetime
from dhan_api import get_ltp, place_market_order

# 🔧 Load config
with open("config.json") as f:
    config = json.load(f)

DRY_RUN = config.get("dry_run", True)
UNDERLYING = config.get("underlying", "NIFTY")
CSV_FILE = "api-scrip-master-detailed.csv"

# 🛎️ macOS Notification
def notify(title, message):
    os.system(f'''osascript -e 'display notification "{message}" with title "{title}"' ''')

# 🧠 Load AI Model
model_path = "option_signal_model.pkl"
if not os.path.exists(model_path):
    print("❌ AI model file not found: option_signal_model.pkl")
    exit()
model = joblib.load(model_path)

# 📈 Fetch Live Index Data
print(f"📥 Fetching {UNDERLYING} live data...")
symbol_map = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK"}
yf_symbol = symbol_map.get(UNDERLYING)
df = yf.download(yf_symbol, interval="15m", period="1d")
if df.empty:
    print("❌ Failed to fetch live data.")
    exit()

# 🧠 Feature Engineering
df["return"] = df["Close"].pct_change()
df["EMA5"] = df["Close"].ewm(span=5).mean()
df["EMA20"] = df["Close"].ewm(span=20).mean()
df["RSI"] = 100 - (100 / (1 + df["Close"].diff().clip(lower=0).rolling(14).mean() / df["Close"].diff().clip(upper=0).abs().rolling(14).mean()))
df.dropna(inplace=True)

# 🎯 Predict Signal
latest = df.iloc[-1]
X_live = pd.DataFrame([[latest["return"], latest["EMA5"], latest["EMA20"], latest["RSI"]]],
                      columns=["return", "EMA5", "EMA20", "RSI"])
signal = model.predict(X_live)[0]
print(f"🤖 AI Signal: {'BUY CALL' if signal == 1 else 'BUY PUT' if signal == -1 else 'HOLD'}")
if signal == 0:
    notify("📉 AI Strategy: HOLD", "No trade placed today.")
    exit()

# 🔍 Load instrument data
df_opt = pd.read_csv(CSV_FILE, low_memory=False)
df_opt = df_opt[(df_opt['UNDERLYING_SYMBOL'] == UNDERLYING) & (df_opt['INSTRUMENT'] == 'OPTIDX') & (df_opt['OPTION_TYPE'].isin(['CE', 'PE']))]
df_opt['SM_EXPIRY_DATE'] = pd.to_datetime(df_opt['SM_EXPIRY_DATE'], errors='coerce')
df_opt = df_opt[df_opt['SM_EXPIRY_DATE'] >= pd.Timestamp.now()]
latest_expiry = df_opt['SM_EXPIRY_DATE'].min()
df_opt = df_opt[df_opt['SM_EXPIRY_DATE'] == latest_expiry]

# 📊 Approx LTP
ltp = float(df["Close"].iloc[-1])
print(f"✅ {UNDERLYING} LTP (approx): ₹{ltp}")

# 🎯 Find CE and PE rows with NaN-safe argsort
ce_strikes = df_opt[df_opt['OPTION_TYPE'] == 'CE']['STRIKE_PRICE'].dropna()
pe_strikes = df_opt[df_opt['OPTION_TYPE'] == 'PE']['STRIKE_PRICE'].dropna()
ce_row = df_opt[df_opt['OPTION_TYPE'] == 'CE'].iloc[(ce_strikes - ltp).abs().argsort().iloc[0]]
pe_row = df_opt[df_opt['OPTION_TYPE'] == 'PE'].iloc[(pe_strikes - ltp).abs().argsort().iloc[0]]

# 🛒 Execute Trade
order_row = ce_row if signal == 1 else pe_row
symbol = order_row['SYMBOL_NAME']
security_id = str(order_row['SECURITY_ID'])
strike = float(order_row['STRIKE_PRICE'])
option_type = order_row['OPTION_TYPE']
instrument_type = order_row['INSTRUMENT_TYPE']
exchange_segment = order_row['EXCH_ID']
lot_size = int(order_row['LOT_SIZE']) if not pd.isna(order_row['LOT_SIZE']) else 50

if DRY_RUN:
    print(f"[Dry Run] Would place order for {symbol} ({option_type})")
    notify("🧪 Dry Run", f"Simulated {option_type}: {symbol}")
else:
    place_market_order(security_id, exchange_segment, instrument_type, "BUY", lot_size)
    notify("✅ Trade Placed", f"AI - BUY {option_type}: {symbol}")

# 🗃️ Log the trade
log = pd.DataFrame([{
    "timestamp": datetime.datetime.now(),
    "symbol": symbol,
    "strike": strike,
    "type": option_type,
    "security_id": security_id
}])

log_file = "trade_logs.csv"
try:
    log.to_csv(log_file, mode='a', index=False, header=not os.path.exists(log_file))
    print("📊 Trade logged to trade_logs.csv")
except Exception as e:
    print(f"⚠️ Failed to log trade: {e}")
