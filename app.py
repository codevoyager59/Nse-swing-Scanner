import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Nifty 50 Scanner", layout="wide")
st.title("📈 Nifty 50 స్కానర్")

# జాబితా మారుతూ ఉంటుంది; అవసరమైతే ఇక్కడ సవరించండి
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
TICKERS = [f"{s}.NS" for s in NIFTY_50]


@st.cache_data(ttl=300, show_spinner="డైలీ డేటా డౌన్‌లోడ్ అవుతోంది...")
def fetch_daily():
    return yf.download(
        TICKERS, period="6mo", interval="1d", group_by="ticker",
        auto_adjust=True, progress=False, threads=True,
    )


@st.cache_data(ttl=60, show_spinner="లైవ్ ధరలు తెస్తున్నాం...")
def fetch_live():
    return yf.download(
        TICKERS, period="1d", interval="1m", group_by="ticker",
        auto_adjust=True, progress=False, threads=True,
    )


def rsi(series, n=14):
    """Wilder RSI"""
