# 📁 backtest_engine.py
# Run AI strategy on historical data and calculate PnL

import yfinance as yf
import pandas as pd
import joblib

# 📥 Load model
model = joblib.load("option_signal_model.pkl")

# 📈 Download historical NIFTY data
print("📊 Downloading historical data for backtest...")
df = yf.download("^NSEI", interval="15m", period="30d")
df.dropna(inplace=True)

# 🧠 Feature engineering
df["return"] = df["Close"].pct_change()
df["EMA5"] = df["Close"].ewm(span=5).mean()
df["EMA20"] = df["Close"].ewm(span=20).mean()
df["RSI"] = 100 - (100 / (1 + df["Close"].diff().clip(lower=0).rolling(14).mean() / df["Close"].diff().clip(upper=0).abs().rolling(14).mean()))
df.dropna(inplace=True)

# 🎯 Prediction
df["signal"] = model.predict(df[["return", "EMA5", "EMA20", "RSI"]])

# 💵 Simulate trades
capital = 100000  # starting capital
quantity = 50     # lot size
entry_price = 0
position = None
pnl = []

for i in range(1, len(df)):
    row = df.iloc[i]
    prev_row = df.iloc[i - 1]
    signal = prev_row["signal"]
    price = row["Close"]

    if position is None:
        if signal == 1:
            position = ("CALL", price)
        elif signal == -1:
            position = ("PUT", price)

    elif position:
        # Close previous position
        if signal != 0:
            direction, entry_price = position
            if direction == "CALL":
                profit = (price - entry_price) * quantity
            else:
                profit = (entry_price - price) * quantity
            capital += profit
            pnl.append(profit)
            position = None

# 🧾 Results
print(f"\n📈 Final Capital: ₹{capital:.2f}")
print(f"💰 Net Profit: ₹{capital - 100000:.2f}")
print(f"📊 Total Trades: {len(pnl)} | Wins: {sum(1 for p in pnl if p > 0)} | Losses: {sum(1 for p in pnl if p <= 0)}")


