import streamlit as st
import pandas as pd
import time
import os

# konfigurasi halaman
st.set_page_config(page_title="Real-Time Dashboard", layout="wide")

st.title("📊 Real-Time Transaction Dashboard")

DATA_PATH = "data/serving/stream"

def load_data():
    try:
        files = [f for f in os.listdir(DATA_PATH) if f.endswith(".parquet")]
        if not files:
            return pd.DataFrame()

        df_list = []
        for file in files:
            df = pd.read_parquet(os.path.join(DATA_PATH, file))
            df_list.append(df)

        df = pd.concat(df_list, ignore_index=True)
        return df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# auto refresh loop
while True:
    df = load_data()

    if df.empty:
        st.warning("Menunggu data streaming masuk...")
    else:
        # KPI
        total_transactions = len(df)
        total_revenue = df["revenue"].sum()

        col1, col2 = st.columns(2)
        col1.metric("Total Transactions", total_transactions)
        col2.metric("Total Revenue", f"Rp {total_revenue:,.0f}")

        # revenue per city
        st.subheader("Revenue per City")
        city_rev = df.groupby("city")["revenue"].sum().reset_index()
        st.bar_chart(city_rev.set_index("city"))

        # top products
        st.subheader("Top Products")
        product_rev = df.groupby("product")["revenue"].sum().reset_index()
        st.bar_chart(product_rev.set_index("product"))

        # revenue trend
        st.subheader("Revenue Trend")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        trend = df.groupby("timestamp")["revenue"].sum().reset_index()
        st.line_chart(trend.set_index("timestamp"))

        # tabel transaksi
        st.subheader("Live Transactions")
        st.dataframe(df.tail(20), use_container_width=True)

    time.sleep(5)
    st.rerun()