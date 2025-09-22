# 📁 log_trades.py
# Append trade logs to CSV with profit/loss calculation

import pandas as pd
import datetime
import os


def log_trade(symbol, strike, type_, entry_price, exit_price, quantity, security_id):
    timestamp = datetime.datetime.now()
    pnl = (exit_price - entry_price) * quantity if type_ == "CE" else (entry_price - exit_price) * quantity

    log = pd.DataFrame([{
        "timestamp": timestamp,
        "symbol": symbol,
        "type": type_,
        "strike": strike,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "quantity": quantity,
        "pnl": round(pnl, 2),
        "security_id": security_id
    }])

    log_file = "trade_logs.csv"
    write_header = not os.path.exists(log_file)
    log.to_csv(log_file, mode="a", index=False, header=write_header)
    print(f"📊 Logged trade: {symbol} {type_} | P&L: ₹{round(pnl, 2)}")


if __name__ == "__main__":
    # Test log
    log_trade("NIFTY 20JUN24 23500CE", 23500, "CE", 120, 132.5, 50, "95123")
