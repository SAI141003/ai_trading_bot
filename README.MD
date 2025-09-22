# AI Trading Bot

A fully automated **options & stock trading system** for the Indian market, built with Python.  
It predicts market direction, selects strikes, executes orders via [Dhan HQ API](https://dhan.co/), and logs every trade — all in real time.

---

## 🚀 Features
- **Signal Generation**  
  - Machine-learning models trained on live & historical data  
  - Predicts direction for NIFTY / BANKNIFTY and equities  
- **Strike Selection**  
  - Automatically picks optimal CE/PE options based on LTP, delta, and strategy rules  
- **Order Execution**  
  - Places trades via Dhan API (market / limit)  
  - Supports straddle, strangle, and directional plays  
- **Automation & Scheduling**  
  - Cron-style scheduler to start/stop strategies at set times  
- **Risk & Logging**  
  - PnL calculation, trade history, Telegram alerts, daily summaries  
- **Backtesting Mode**  
  - Replay historical data to validate strategies before going live

---

## 🛠 Tech Stack
- **Python 3** (core language)  
- `pandas`, `numpy`, `scikit-learn`, `matplotlib`  
- Dhan HQ REST API  
- Cron / shell scripts for automation  
- Git & GitHub for version control

---

## 📂 Project Structure
