from dhan_api import get_ltp

# Example from symbol lookup: Replace this with real values you searched
security_id = "95123"           # Replace with a working ID
exchange_segment = "NFO"        # NFO = NSE Futures & Options
instrument_type = "OPTIDX"      # Options on index

ltp = get_ltp(security_id, exchange_segment, instrument_type)

if ltp:
    print(f"✅ LTP: ₹{ltp}")
else:
    print("❌ LTP fetch failed.")
