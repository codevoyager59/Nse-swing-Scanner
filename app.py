import streamlit as st
st.title("NSE Swing Scanner")
import os
import time
import requests

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

nifty_stocks = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "BHARTIARTL", "SBIN", "HINDUNILVR", "LT", "ITC",
]

all_stocks_data = []

for symbol in nifty_stocks:
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": f"{symbol}.BSE",
        "apikey": 'api_key',
    }
    try:
        response = requests.get(
            "https://www.alphavantage.co/query", params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"{symbol}: రిక్వెస్ట్ విఫలమైంది - {e}")
        continue

    quote = data.get("Global Quote")
    if quote:
        all_stocks_data.append(
            {
                "symbol": symbol,
                "price": quote.get("05. price"),
                "change_percent": quote.get("10. change percent"),
            }
        )
    else:
        # లిమిట్ లేదా తప్పు సింబల్ సందేశం
        print(f"{symbol}: డేటా రాలేదు - {data}")

    time.sleep(13)  # ఉచిత ప్లాన్ లిమిట్ కోసం

for item in all_stocks_data:
    print(item)
