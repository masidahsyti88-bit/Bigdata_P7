import streamlit as st
import time
import sys
import os
import pandas as pd

# FIX MODULE PATH (WAJIB)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# IMPORT MODULE
from analytics import transportation_analytics as ta
from alerts import transportation_alert as alert

# CONFIG
DATA_PATH = "data/serving/transportation"
st.set_page_config(page_title="Smart Transportation Dashboard", layout="wide")
st.title("Smart Transportation Real-Time Analytics (Big Data Optimized)")

# AUTO REFRESH
REFRESH_INTERVAL = 5
placeholder = st.empty()

# MAIN LOOP
while True:
    with placeholder.container():
        # 1. LOAD DATA
        df = ta.load_data(DATA_PATH)
        if df.empty:
            st.warning("Waiting for streaming transportation data...")
            time.sleep(REFRESH_INTERVAL)
            continue
        
        # 2. PREPROCESS
        df = ta.preprocess(df)

        # --- LANGKAH 3: OPTIMASI PENGAMBILAN DATA (DOWNSAMPLING) ---
        # Ambil subset data terbaru (1000 baris terakhir) agar rendering visualisasi cepat
        df_sample = df.tail(1000)
        
        # 3. METRICS (Tetap menggunakan df asli untuk akurasi total)
        try:
            metrics = ta.compute_metrics(df)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trips", metrics["total_trips"])
            col2.metric("Total Fare", f"Rp {int(metrics['total_fare']):,}")
            col3.metric("Top Location", metrics["top_location"])
        except Exception as e:
            st.error(f"Error computing metrics: {e}")
            
        st.divider()
        
        # 4. PEAK HOUR
        try:
            peak_hour = ta.detect_peak_hour(df)
            st.info(f"Peak traffic hour: {peak_hour}:00")
        except Exception:
            st.warning("Tidak dapat menghitung peak hour")
            
        # 5. ALERTS
        try:
            alerts = alert.generate_alert(df)
            if alerts:
                st.subheader("Traffic Alerts")
                for a in alerts:
                    st.error(a)
        except Exception as e:
            st.warning(f"Alert error: {e}")
            
        st.divider()
        
        # --- LANGKAH 3: VISUALISASI REAL-TIME & SKALA BESAR ---
        try:
            # A. Real-Time Traffic (Window Aggregation)
            st.subheader("Real-Time Traffic (Window Aggregation)")
            traffic_window = ta.traffic_per_window(df)
            if traffic_window is not None:
                st.line_chart(traffic_window)

            col1, col2 = st.columns(2)
            with col1:
                # B. Traffic Density (Menggunakan df_sample)
                st.subheader("Traffic Density (Fare per Location)")
                st.bar_chart(ta.fare_per_location(df_sample))
            
            with col2:
                # C. Vehicle Distribution (Menggunakan df_sample)
                st.subheader("Vehicle Distribution")
                st.bar_chart(ta.vehicle_distribution(df_sample))
            
            # D. Mobility Trend (Menggunakan df_sample['fare'])
            st.subheader("Mobility Trend (Fare Analysis)")
            st.line_chart(df_sample['fare'])

        except Exception as e:
            st.warning(f"Visualization error: {e}")
            
        st.divider()
        
        # 6. ANOMALY DETECTION
        try:
            st.subheader("Abnormal Trips Detection")
            anomaly_df = ta.detect_anomaly(df)
            if not anomaly_df.empty:
                st.dataframe(anomaly_df.tail(20), use_container_width=True)
            else:
                st.success("No anomalies detected")
        except Exception as e:
            st.warning(f"Anomaly error: {e}")
            
        st.divider()
        
        # --- LANGKAH 3: LIMITED TABLE ---
        # Menampilkan hanya 50 data terakhir agar dashboard tidak crash
        st.subheader("Live Trip Data (Latest 50 Records)")
        st.dataframe(df.tail(50), use_container_width=True)
        
        # Jeda refresh
        time.sleep(REFRESH_INTERVAL)