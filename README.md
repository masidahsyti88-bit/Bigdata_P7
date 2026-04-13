🚀 Smart City Traffic Prediction AIProyek ini adalah implementasi Machine Learning Pipeline untuk memprediksi volume lalu lintas kendaraan di Smart City menggunakan model Random Forest Regressor. Sistem ini mencakup pembersihan data, pelatihan model, hingga visualisasi interaktif melalui dashboard.
📊 Hasil Praktikum
    Average Traffic:113 kendaraan.
    Max Traffic:189 kendaraan.
    Fitur Prediksi: Mampu memprediksi jumlah kendaraan berdasarkan input jam, hari, dan data traffic sebelumnya (lag).

📁 Struktur Proyek
    Big Data:data/raw/: Dataset mentah (traffic_smartcity_v1.csv).
    data/clean/: Data hasil pembersihan.
    scripts/: Skrip Python untuk data cleaning.
    analytics/: Skrip pelatihan model Machine Learning.
    models/: Penyimpanan model terlatih dalam format .
    pkl.dashboard/: Antarmuka visual menggunakan Streamlit.

🛠️ Cara MenjalankanData Cleaning:
    Bashpython3 scripts/traffic_data_cleaning_v1.py
    Model Training:Bashpython3 analytics/traffic_ml_model_v1.py
    Run Dashboard:Bashstreamlit run dashboard/traffic_dashboard_v1.py

📝 Insight
    Penggunaan fitur time-series seperti jam dan hari sangat efektif untuk memprediksi pola kemacetan.
    Pipeline data yang terstruktur memudahkan integrasi antara proses backend (ML) dan frontend (Dashboard).
