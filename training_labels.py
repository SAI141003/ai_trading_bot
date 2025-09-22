# 📁 training_labels.py — Generate true labels for signal training (with indicators)

import pandas as pd
import yfinance as yf
from ta.trend import MACD, ADXIndicator
from ta.volatility import BollingerBands

# 🔧 Config
INDEX = "^NSEBANK"   # or use "^NSEI" for NIFTY
PERIOD = "60d"
INTERVAL = "15m"
FWD_PERIOD = 2        # How many bars ahead to look for direction
THRESHOLD = 0.001     # 0.1% move up or down for classification

print(f"📥 Downloading {INDEX} data...")
df = yf.download(INDEX, period=PERIOD, interval=INTERVAL)
if df.empty:
    print("❌ No data found")
    exit()

# 🎯 Feature engineering
df["return"] = df["Close"].pct_change()
df["EMA5"] = df["Close"].ewm(span=5).mean()
df["EMA20"] = df["Close"].ewm(span=20).mean()
df["RSI"] = 100 - (100 / (1 + df["Close"].diff().clip(lower=0).rolling(14).mean() /
                          df["Close"].diff().clip(upper=0).abs().rolling(14).mean()))

# ➕ Technical Indicators
macd_obj = MACD(close=df["Close"])
df["MACD"] = macd_obj.macd().squeeze()
df["MACD_SIGNAL"] = macd_obj.macd_signal().squeeze()

adx = ADXIndicator(high=df["High"], low=df["Low"], close=df["Close"])
df["ADX"] = adx.adx()

bb = BollingerBands(close=df["Close"])
df["BB_WIDTH"] = bb.bollinger_wband()

df["VOLATILITY"] = df["High"] - df["Low"]

# 🎯 True label creation
future_close = df["Close"].shift(-FWD_PERIOD)
df["future_return"] = (future_close - df["Close"]) / df["Close"]

def label_signal(r):
    if r > THRESHOLD:
        return 1
    elif r < -THRESHOLD:
        return -1
    else:
        return 0

df["label"] = df["future_return"].apply(label_signal)

# 🧼 Drop rows with missing values
df.dropna(inplace=True)

# 💾 Save enriched dataset
features = [
    "return", "EMA5", "EMA20", "RSI",
    "MACD", "MACD_SIGNAL", "ADX", "BB_WIDTH", "VOLATILITY", "label"
]
df[features].to_csv("training_data.csv", index=False)
print("✅ Saved enriched training set with indicators as training_data.csv")
