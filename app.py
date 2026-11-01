import numpy as np
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Nifty 50 Scanner", layout="wide")
st.title("📈 Nifty 50 స్కానర్")

# API Configuration - Replace with your actual API key
API_KEY = "HE9VYFMH4LAI7ELG"

# NIFTY 50 జాబితా
NIFTY_50 = [
    "ADANIENT",
    "ADANIPORTS",
    "APOLLOHOSP",
    "ASIANPAINT",
    "BAJAJ-AUTO",
    "BAJFINANCE",
    "BAJAJFINSV",
    "BEL",
    "BHARTIARTL",
    "BPCL",
    "BRITANNIA",
    "CIPLA",
    "COALINDIA",
    "DRREDDY",
    "EICHERMOT",
    "GRASIM",
    "HCLTECH",
    "HDFCBANK",
    "HDFCLIFE",
    "HEROMOTOCO",
    "HINDALCO",
    "HINDUNILVR",
    "ICICIBANK",
    "INDIGO",
    "INFY",
    "ITC",
    "JSWSTEEL",
    "KOTAKBANK",
    "LT",
    "M&M",
    "MARUTI",
    "NESTLEIND",
    "NTPC",
    "ONGC",
    "POWERGRID",
    "RELIANCE",
    "SBILIFE",
    "SBIN",
    "SUNPHARMA",
    "TATACONSUMER",
    "TATAMOTORS",
    "TATASTEEL",
    "TCS",
    "TECHM",
    "TITAN",
    "TRENT",
    "ULTRACEMCO",
    "WIPRO",
]


@st.cache_data(ttl=60, show_spinner="డేటా డౌన్లోడ్ అవుతోంది...")
def fetch_intraday_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}.NS&interval=1min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "Time Series (1min)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (1min)"], orient="index")
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.index)
        df["Close"] = df["Close"].astype(float)
        return df.sort_index()
    return pd.DataFrame()


def rsi(series, n=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(n).mean()
    loss = (-delta.clip(upper=0)).rolling(n).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


results = []

for symbol in NIFTY_50:
    df = fetch_intraday_data(symbol)
    if not df.empty:
        current_close = df["Close"].iloc[-1]
        current_rsi = rsi(df["Close"]).iloc[-1]
        results.append(
            {
                "స్టాక్": symbol,
                "ప్రస్తుత ధర": round(current_close, 2),
                "RSI": round(current_rsi, 2),
            }
        )

results_df = pd.DataFrame(results)
st.subheader("📊 ప్రస్తుత RSI విలువలు")
st.dataframe(results_df, use_container_width=True)

