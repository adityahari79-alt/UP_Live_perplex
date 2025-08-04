import time
import pandas as pd
from heikin_ashi import heikin_ashi
from doji_detector import is_heikin_ashi_doji
from upstox_client_wrapper import UpstoxClientWrapper
from upstox_client import LtpRequest  

# --- Initialization (Secure these in your real project)
ACCESS_TOKEN = eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI2S0JBNTgiLCJqdGkiOiI2ODkwNGU1NmIxYWQ2NTVhMTAyNWM0NzQiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6dHJ1ZSwiaWF0IjoxNzU0Mjg3NzAyLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3NTQzNDQ4MDB9.k4sUMzi1Ty5EpFyfwLd-ouyDoO6Uv24FCFZZxiYF_tQ
API_KEY = 299b3a51-7883-4bd2-9526-37152c12b0f2
EXCHANGE = "NSE_EQ"  # Exchange name
SYMBOL_NAME = "RELIANCE"  # Symbol name without exchange prefix
QUANTITY = 1

client = UpstoxClientWrapper(ACCESS_TOKEN, API_KEY)

# --- Data buffer for rolling OHLC candles (simulate with LTP for demo; replace for production)
ohlc_data = []

while True:
    # Prepare the LtpRequest body as required by the SDK
    body = LtpRequest(
        instruments=[{"exchange": EXCHANGE, "symbol": SYMBOL_NAME}]
    )

    # Fetch LTP (last traded price) with correct usage
    try:
        ltp_response = client.market_api.get_ltp(body)
        quote = ltp_response.data[0].last_traded_price
    except (AttributeError, IndexError, KeyError, TypeError) as e:
        print(f"Skipping, unable to fetch quote: {e}")
        time.sleep(5)
        continue

    # Fake OHLC for demonstration (replace with real interval OHLC fetch in production)
    now = pd.Timestamp.now()
    ohlc = {
        "Open": quote,
        "High": quote,
        "Low": quote,
        "Close": quote,
        "Volume": 0,  # Replace with real volume if available
        "Datetime": now,
    }
    ohlc_data.append(ohlc)

    if len(ohlc_data) < 20:
        # Wait until enough candles for analysis
        time.sleep(60)
        continue

    # --- Main Analysis (use the last 20 candles)
    df = pd.DataFrame(ohlc_data[-20:])
    ha_df = heikin_ashi(df)
    latest_ha = ha_df.iloc[-1]

    if is_heikin_ashi_doji(latest_ha):
        print(f"Doji Detected at {latest_ha['Datetime']}: Attempting to BUY")
        # Replace with actual instrument token integer from your data source
        instrument_token = 123456

        order = client.place_order(
            instrument_token=instrument_token,
            quantity=QUANTITY,
            transaction_type="BUY"
        )
        print(f"Order result: {order}")

    # Wait for next polling interval (use websocket or event-driven logic in production)
    time.sleep(60)


