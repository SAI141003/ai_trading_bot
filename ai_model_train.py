# 📁 ai_model_train.py
# Train a simple ML model to predict option signals: BUY CALL / BUY PUT / HOLD

import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 🔍 Download NIFTY historical data
df = yf.download("^NSEI", interval="15m", period="60d")
df = df.dropna()

# 🧠 Feature engineering
df["return"] = df["Close"].pct_change()
df["EMA5"] = df["Close"].ewm(span=5).mean()
df["EMA20"] = df["Close"].ewm(span=20).mean()
df["RSI"] = 100 - (100 / (1 + df["Close"].diff().clip(lower=0).rolling(14).mean() / df["Close"].diff().clip(upper=0).abs().rolling(14).mean()))

# 🎯 Target label
# BUY CALL = 1, BUY PUT = -1, HOLD = 0 based on next bar movement
df["target"] = df["Close"].shift(-1) - df["Close"]
df["target"] = df["target"].apply(lambda x: 1 if x > 0.25 else (-1 if x < -0.25 else 0))
df = df.dropna()

# 🎓 Train/Test split
features = ["return", "EMA5", "EMA20", "RSI"]
X = df[features]
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🤖 Train model
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 📈 Evaluate
y_pred = model.predict(X_test)
print("\n🧪 Classification Report:\n")
print(classification_report(y_test, y_pred))

# 💾 Save model for later use
joblib.dump(model, "option_signal_model.pkl")
print("✅ Model saved as option_signal_model.pkl")

