import json
import requests

with open("config.json") as f:
    config = json.load(f)

headers = {
    "access-token": config["access_token"],
    "Content-Type": "application/json"
}

def place_market_order(security_id, exchange_segment, instrument_type, transaction_type, quantity):
    url = "https://api.dhan.co/orders"
    payload = {
        "transactionType": transaction_type.upper(),  # BUY or SELL
        "securityId": security_id,
        "exchangeSegment": exchange_segment,
        "instrumentType": instrument_type,
        "productType": "INTRADAY",  # or DELIVERY
        "orderType": "MARKET",
        "quantity": quantity,
        "price": 0
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Order placed successfully:", response.json())
    else:
        print("❌ Order placement failed:", response.text)

if __name__ == "__main__":
    # Replace with actual values from your lookup
    place_market_order(
        security_id="95123",  # ← Replace with real SECURITY_ID
        exchange_segment="NFO",
        instrument_type="OPTIDX",
        transaction_type="BUY",
        quantity=50  # lot size
    )
