# 📁 backtest_ai_signals.py — Evaluate model accuracy on past NIFTY/BANKNIFTY index data

import pandas as pd
import yfinance as yf
import joblib
from sklearn.metrics import classification_report

# 🔧 Config
MODEL_PATH = "option_signal_model.pkl"
INDEX = "^NSEBANK"  # or "^NSEI" for NIFTY
PERIOD = "30d"
INTERVAL = "15m"

print(f"📥 Downloading historical data for {INDEX}...")
df = yf.download(INDEX, period=PERIOD, interval=INTERVAL)
if df.empty:
    print("❌ Failed to fetch index data.")
    exit()

# 🧠 Feature engineering (same as main.py)
df["return"] = df["Close"].pct_change()
df["EMA5"] = df["Close"].ewm(span=5).mean()
df["EMA20"] = df["Close"].ewm(span=20).mean()
df["RSI"] = 100 - (100 / (1 + df["Close"].diff().clip(lower=0).rolling(14).mean() / df["Close"].diff().clip(upper=0).abs().rolling(14).mean()))
df.dropna(inplace=True)

# 🧠 Load model
print("🧠 Loading model...")
model = joblib.load(MODEL_PATH)

# 🔍 Run predictions
features = ["return", "EMA5", "EMA20", "RSI"]
X = df[features]
y_pred = model.predict(X)
df['signal'] = y_pred

# 🧪 Evaluate prediction distribution
buy_calls = sum(df['signal'] == 1)
buy_puts = sum(df['signal'] == -1)
holds = sum(df['signal'] == 0)

print(f"\n📊 Signal Distribution over {len(df)} bars:")
print(f"🟢 BUY CALLs: {buy_calls}")
print(f"🔴 BUY PUTs: {buy_puts}")
print(f"🟡 HOLDS: {holds}")

# 🔁 Optional: Save signals to CSV for further study
df[["Close", "return", "EMA5", "EMA20", "RSI", "signal"]].to_csv("backtest_signals.csv")
print("📄 Signals saved to backtest_signals.csv")


