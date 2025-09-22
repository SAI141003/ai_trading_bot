import pandas as pd

CSV_FILE = "api-scrip-master-detailed.csv"

def load_data():
    print("📥 Loading instrument data...")
    try:
        df = pd.read_csv(CSV_FILE, low_memory=False)
        print("✅ Instrument data loaded successfully.\n")
        return df
    except FileNotFoundError:
        print("❌ ERROR: CSV file not found.")
        exit()

def filter_optidx_options(df, underlying, strike, option_type):
    # Clean and filter
    df['SYMBOL_NAME'] = df['SYMBOL_NAME'].astype(str).str.upper().str.strip()
    df['INSTRUMENT_TYPE'] = df['INSTRUMENT_TYPE'].astype(str).str.upper().str.strip()
    df['UNDERLYING_SYMBOL'] = df['UNDERLYING_SYMBOL'].astype(str).str.upper().str.strip()
    df['OPTION_TYPE'] = df['OPTION_TYPE'].astype(str).str.upper().str.strip()

    # Filter for OPTIDX
    df = df[df['INSTRUMENT_TYPE'] == 'OPTIDX']
    
    # Match NIFTY/BANKNIFTY, strike, CE/PE
    result = df[
        (df['UNDERLYING_SYMBOL'] == underlying) &
        (df['STRIKE_PRICE'] == float(strike)) &
        (df['OPTION_TYPE'] == option_type)
    ]

    return result[['SYMBOL_NAME', 'SECURITY_ID', 'STRIKE_PRICE', 'OPTION_TYPE', 'SM_EXPIRY_DATE']]

if __name__ == "__main__":
    df = load_data()

    underlying = input("📈 Underlying (NIFTY or BANKNIFTY): ").strip().upper()
    strike = input("🎯 Strike Price (e.g., 47000): ").strip()
    option_type = input("📌 Option Type (CE or PE): ").strip().upper()

    result = filter_optidx_options(df, underlying, strike, option_type)

    if result.empty:
        print("❌ No matching option found.")
    else:
        print("✅ Matching option(s):")
        print(result.to_string(index=False))

