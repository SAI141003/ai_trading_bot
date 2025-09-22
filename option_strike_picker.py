import requests
import pandas as pd
import json

# Load token from config
with open("config.json") as f:
    config = json.load(f)

headers = {
    "access-token": config["access_token"],
    "Content-Type": "application/json"
}

# Step 1: Get LTP of NIFTY or BANKNIFTY
def get_ltp(security_id, instrument_type="INDEX"):
    url = "https://api.dhan.co/market/quotes/latest"
    params = {
        "securityId": security_id,
        "exchangeSegment": "NFO",
        "instrumentType": instrument_type
    }
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200:
        return r.json().get("lastTradedPrice", 0) / 100
    else:
        print("❌ LTP fetch failed:", r.text)
        return None

# Step 2: Download live instrument list
def download_instrument_master():
    url = "https://images.dhan.co/api-data/api-scrip-master-detailed.csv"
    r = requests.get(url)
    if r.status_code != 200:
        print("❌ Failed to download instrument list")
        return None
    with open("live_instruments.csv", "wb") as f:
        f.write(r.content)
    df = pd.read_csv("live_instruments.csv", low_memory=False)
    return df

# Step 3: Filter to get ATM strike option
def find_atm_option(df, underlying="NIFTY", option_type="CE", ltp=23500):
    base = 50 if underlying == "NIFTY" else 100
    atm_strike = round(ltp / base) * base

    df['INSTRUMENT_TYPE'] = df['INSTRUMENT_TYPE'].astype(str).str.upper()
    df['UNDERLYING_SYMBOL'] = df['UNDERLYING_SYMBOL'].astype(str).str.upper()
    df['OPTION_TYPE'] = df['OPTION_TYPE'].astype(str).str.upper()

    df = df[
        (df['INSTRUMENT_TYPE'] == "OPTIDX") &
        (df['UNDERLYING_SYMBOL'] == underlying) &
        (df['OPTION_TYPE'] == option_type) &
        (df['STRIKE_PRICE'] == atm_strike)
    ]

    if df.empty:
        print(f"❌ No matching {option_type} option found for {underlying} {atm_strike}")
        return None

    return df[['SYMBOL_NAME', 'SECURITY_ID', 'STRIKE_PRICE', 'SM_EXPIRY_DATE']]

if __name__ == "__main__":
    # NIFTY Index security ID
    underlying = "NIFTY"
    index_id = "9999200001"  # use 9999200005 for BANKNIFTY

    ltp = get_ltp(index_id)
    if ltp:
        print(f"✅ {underlying} LTP: ₹{ltp}")
        df = download_instrument_master()
        if df is not None:
            result = find_atm_option(df, underlying=underlying, option_type="CE", ltp=ltp)
            if result is not None:
                print("✅ ATM CE Option:")
                print(result.to_string(index=False))
