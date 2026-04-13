import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load data clean
df = pd.read_csv('data/clean/traffic_smartcity_clean_v1.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

# Feature Engineering
df['hour'] = df['datetime'].dt.hour
df['day'] = df['datetime'].dt.dayofweek
df['lag1'] = df['traffic'].shift(1)
df = df.dropna()

# Inisialisasi Fitur dan Target
X = df[['hour', 'day', 'lag1']]
y = df['traffic']

# Training Model
model = RandomForestRegressor()
model.fit(X, y)

# Simpan Model
joblib.dump(model, 'models/traffic_model_v1.pkl')
print("Model berhasil disimpan")