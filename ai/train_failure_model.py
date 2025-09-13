# ai/train_failure_model.py

import os
import json
import pandas as pd
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def load_test_history():
    """Fungsi yang sama seperti sebelumnya"""
    history = []
    
    if not os.path.exists("history"):
        print("❌ Folder 'history/' tidak ditemukan.")
        return pd.DataFrame()
    
    for filename in os.listdir("history"):
        if filename.startswith("report_") and filename.endswith(".json"):
            filepath = os.path.join("history", filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                
                execution_time = datetime.fromtimestamp(data["created"])
                
                for test in data["tests"]:
                    history.append({
                        "timestamp": data["created"],
                        "execution_time": execution_time,
                        "test_name": test["nodeid"],
                        "outcome": test["outcome"],
                        "duration_sec": round(test["call"]["duration"], 3)
                    })
            except Exception as e:
                print(f"⚠️ Error baca {filename}: {e}")
    
    return pd.DataFrame(history)

# --- 1. Muat data ---
df = load_test_history()
if df.empty:
    print("❌ Tidak ada data. Jalankan CI dulu!")
    exit()

print(f"✅ Data dimuat: {len(df)} record")

# --- 2. Ekstrak Fitur ---
df['hour'] = df['execution_time'].dt.hour
df['day_of_week'] = df['execution_time'].dt.dayofweek
df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)

# Normalized duration (relatif terhadap rata-rata)
mean_duration = df['duration_sec'].mean()
df['duration_ratio'] = df['duration_sec'] / (mean_duration + 1e-8)  # hindari divide by zero

# --- 3. Encode nama test ---
le = LabelEncoder()
df['test_encoded'] = le.fit_transform(df['test_name'])

# --- 4. Target: Prediksi kegagalan di masa depan ---
# Karena semua test PASSED, kita simulasi sedikit
# Asumsi: jika durasi > 8 detik, lebih berisiko gagal nanti
df = df.sort_values("timestamp").reset_index(drop=True)
df['will_fail_next'] = 0
# Simulasi: test UI panjang → beri label 1 (risiko tinggi)
df.loc[(df['test_name'].str.contains("ui")) & (df['duration_sec'] > 8), 'will_fail_next'] = 1

# Cek distribusi target
print("\n--- Distribusi Target ---")
print(df['will_fail_next'].value_counts())

# --- 5. Siapkan Fitur untuk ML ---
features = ['test_encoded', 'hour', 'day_of_week', 'is_weekend', 'duration_ratio']
X = df[features]
y = df['will_fail_next']

# Jika hanya ada satu kelas, tambahkan dummy row agar model bisa latih
if len(y.unique()) == 1:
    print("⚠️ Hanya satu kelas, tambahkan data dummy untuk simulasi...")
    import numpy as np
    X = pd.concat([X, pd.DataFrame([X.iloc[0].values], columns=X.columns)], ignore_index=True)
    y = pd.concat([y, pd.Series([1])], ignore_index=True)

# --- 6. Latih Model ---
model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
model.fit(X, y)

# --- 7. Simpan Model & Encoder ---
os.makedirs("ai/models", exist_ok=True)
joblib.dump(model, "ai/models/failure_prediction_model.pkl")
joblib.dump(le, "ai/models/test_name_encoder.pkl")

print("\n✅ Model berhasil dilatih dan disimpan!")
print("📁 File: ai/models/failure_prediction_model.pkl")
print("📊 Fitur: test, jam, hari, durasi relatif")
print("🎯 Target: prediksi risiko kegagalan di masa depan")

# --- 8. Contoh Prediksi ---
sample = X.iloc[[0]]  # ambil satu baris
pred = model.predict(sample)[0]
prob = model.predict_proba(sample)[0]

print(f"\n🔍 Contoh Prediksi:")
print(f"Test: {df['test_name'].iloc[0]}")
print(f"Durasi: {df['duration_sec'].iloc[0]:.3f}s")
print(f"Prediksi: {'Berisiko Gagal' if pred == 1 else 'Aman'}")
print(f"Probabilitas Gagal: {prob[1]:.2%}")