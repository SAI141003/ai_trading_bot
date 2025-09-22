# 📁 trade_engine.py
# Basic signal engine using moving averages (can plug into main.py or ML)

import pandas as pd
import yfinance as yf


def fetch_historical_data(symbol="^NSEI", interval="15m", period="5d"):
    """Fetch historical index data (default: NIFTY 50)"""
    print(f"📥 Downloading historical data for {symbol}...")
    df = yf.download(tickers=symbol, interval=interval, period=period)
    if df.empty:
        print("❌ No data fetched.")
        return None
    df = df[['Close']]
    df.dropna(inplace=True)
    return df


def generate_signal(df, short_window=5, long_window=20):
    """Generates basic crossover signal"""
    df['SMA5'] = df['Close'].rolling(window=short_window).mean()
    df['SMA20'] = df['Close'].rolling(window=long_window).mean()
    df.dropna(inplace=True)

    if df.iloc[-1]['SMA5'] > df.iloc[-1]['SMA20']:
        return "BUY CALL"
    elif df.iloc[-1]['SMA5'] < df.iloc[-1]['SMA20']:
        return "BUY PUT"
    else:
        return "HOLD"


if __name__ == "__main__":
    df = fetch_historical_data()
    if df is not None:
        signal = generate_signal(df)
        print(f"🧠 Signal Generated: {signal}")
