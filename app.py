import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Nifty 50 Scanner", layout="wide")
st.title("📈 Nifty 50 స్కానర్")

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

# Sidebar లో కాలావధి ఎంపిక
period = st.sidebar.selectbox("కాలావధి", ["3mo", "6mo", "1y"])


@st.cache_data(ttl=900, show_spinner="డేటా డౌన్లోడ్ అవుతోంది...")
def load_data(symbols, period):
    tickers = [f"{s}.NS" for s in symbols]
    return yf.download(
        tickers,
        period=period,
        group_by="ticker",
        auto_adjust=True,
        progress=False,
        threads=True,
    )


def rsi(series, n=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(n).mean()
    loss = (-delta.clip(upper=0)).rolling(n).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


# డేటాని తీసుకురావడం
data = load_data(NIFTY_50, period)

# ఫలితాలను నిల్వ చేయడానికి జాబితా
results = []

# ప్రతి స్టాక్ కి RSI ని కాలిక్యులేట్ చేయడం
for symbol in NIFTY_50:
    ticker_data = data[f"{symbol}.NS"]
    if not ticker_data.empty:
        current_close = ticker_data["Close"].iloc[-1]
        current_rsi = rsi(ticker_data["Close"]).iloc[-1]
        results.append(
            {
                "స్టాక్": symbol,
                "ప్రస్తుత ధర": round(current_close, 2),
                "RSI": round(current_rsi, 2),
            }
        )

# ఫలితాలను DataFrame లోకి మార్చడం
results_df = pd.DataFrame(results)

# యాప్ లో డిస్ప్లే చేయడం
st.subheader("📊 ప్రస్తుత RSI విలువలు")
st.dataframe(results_df, use_container_width=True)
