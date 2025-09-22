# 📁 train_model.py — Retrain AI model on labeled signals (Fixed NaN issue)

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# 📄 Load labeled data
df = pd.read_csv("training_data.csv")

# ✅ Drop rows with NaN (missing values)
df.dropna(inplace=True)

# 🧠 Features & Labels
X = df[["return", "EMA5", "EMA20", "RSI"]]
y = df["label"]

# 🔀 Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🎓 Train Model
model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
model.fit(X_train, y_train)

# 📊 Evaluation
y_pred = model.predict(X_test)
print("\n✅ Model Evaluation:")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 💾 Save Model
joblib.dump(model, "option_signal_model.pkl")
print("\n📦 Model saved as option_signal_model.pkl")


