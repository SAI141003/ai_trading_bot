# 📁 dhan_api.py (fully updated)

import json
import requests

# 🔧 Load access token from config.json
with open("config.json") as f:
    config = json.load(f)

ACCESS_TOKEN = config.get("access_token")
HEADERS = {
    "accept": "application/json",
    "access-token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# ✅ Fetch Latest Traded Price (LTP)
def get_ltp(security_id, exchange_segment="NSE", instrument_type="INDEX"):
    try:
        url = f"https://api.dhan.co/market/quotes/latest"
        payload = {
            "security_id": security_id,
            "exchange_segment": exchange_segment,
            "instrument_type": instrument_type
        }
        res = requests.post(url, json=payload, headers=HEADERS)
        if res.status_code == 200:
            data = res.json()
            return float(data.get("last_traded_price", 0)) / 100
        else:
            print("❌ Failed to fetch LTP:", res.text)
            return None
    except Exception as e:
        print("⚠️ LTP Exception:", e)
        return None


# ✅ Place Market Order
def place_market_order(security_id, exchange_segment, instrument_type, transaction_type, quantity):
    try:
        url = "https://api.dhan.co/orders"
        payload = {
            "security_id": security_id,
            "exchange_segment": exchange_segment,
            "instrument_type": instrument_type,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "order_type": "MARKET",
            "product_type": "INTRADAY",
            "validity": "DAY",
            "price": 0.0
        }
        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code == 200:
            print(f"✅ Order Placed: {security_id}")
        else:
            print(f"❌ Order Failed: {response.status_code} → {response.text}")
    except Exception as e:
        print("⚠️ Order Exception:", e)

