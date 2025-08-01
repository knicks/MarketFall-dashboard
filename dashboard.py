import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Expanded symbol list
symbols = {
    "^NSEI": "NIFTY 50",
    "^NSMIDCP": "NIFTY NEXT 50",
    "^NSEMDCP150": "NIFTY MIDCAP 150",
    "^NSEBANK": "NIFTY BANK",
    "^CNXIT": "NIFTY IT",
    "^CNXFIN": "NIFTY FINANCIAL SERVICES",
    "^CRSLDX": "NIFTY 500",
    "^BSESN": "SENSEX",
    "NIFTYSMLCAP250.NS": "NIFTY SMLCAP 250",
    "^SPX": "S&P 500",
    "MAGS": "MAGS",
    "^VIX": "VIX",
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "SOXL": "SOXL",
    "AVGO": "Broadcom",
}

st.set_page_config(layout="wide")
st.title("📊 Fall Dashboard - % Drop from 52W High")
st.markdown("This dashboard shows the percentage fall of major indices, stocks, ETFs, and crypto assets from their 52-week highs.")

results = []

for symbol, name in symbols.items():
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1y")
        if hist.empty:
            continue

        current_price = hist["Close"][-1]
        high_52w = hist["Close"].max()
        fall_pct = ((current_price - high_52w) / high_52w) * 100

        results.append({
            "Symbol": symbol,
            "Name": name,
            "Price": round(current_price, 2),
            "52W High": round(high_52w, 2),
            "% Fall": round(fall_pct, 2),
            "10% Low": "✅" if fall_pct <= -10 else "",
            "15% Low": "✅" if fall_pct <= -15 else "",
            "20% Low": "✅" if fall_pct <= -20 else "",
            "25% Low": "✅" if fall_pct <= -25 else "",
        })
    except Exception as e:
        st.warning(f"Error fetching {symbol}: {e}")

df = pd.DataFrame(results)
df_display = df.set_index("Name")

st.dataframe(df_display)

# --- Fall Bar sorted from least to worst ---
df_sorted = df.sort_values("% Fall", ascending=True)

fig = go.Figure()
fig.add_trace(go.Bar(
    y=df_sorted["Name"],
    x=-df_sorted["% Fall"],
    orientation='h',
    text=df_sorted["% Fall"].apply(lambda x: f"{x:.2f}%"),
    textposition="outside",
    marker_color='crimson'
))

fig.update_layout(
    title="📉 Sorted Fall Bar - % Drop from 52W High",
    xaxis_title="Fall (%)",
    yaxis_title="Asset",
    template="plotly_white",
    height=600,
    margin=dict(l=100, r=20, t=60, b=40)
)

st.plotly_chart(fig, use_container_width=True)
