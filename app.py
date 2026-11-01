import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Nifty 50 Scanner", layout="wide")
st.title("📈 Nifty 50 స్కానర్")

# నిఫ్టీ 50 జాబితా మారుతూ ఉంటుంది; అవసరమైతే ఇక్కడ సవరించండి
NIFTY_50 = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BEL", "BHARTIARTL",
    "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "ETERNAL",
    "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE", "HINDALCO",
    "HINDUNILVR", "ICICIBANK", "INDIGO", "INFY", "ITC",
    "JIOFIN", "JSWSTEEL", "KOTAKBANK", "LT", "M&M",
    "MARUTI", "MAXHEALTH", "NESTLEIND", "NTPC", "ONGC",
    "POWERGRID", "RELIANCE", "SBILIFE", "SBIN", "SHRIRAMFIN",
    "SUNPHARMA", "TATACONSUMER", "TATAMOTORS", "TATASTEEL", "TCS",
    "TECHM", "TITAN", "TRENT", "ULTRACEMCO", "WIPRO",
]

period = st.sidebar.selectbox("కాలవ్యవధి", ["3mo", "6mo", "1y", "2y"], index=1)


@st.cache_data(ttl=900, show_spinner="డేటా డౌన్‌లోడ్ అవుతోంది...")
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
