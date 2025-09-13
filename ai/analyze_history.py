# ai/analyze_history.py

import os
import json
import pandas as pd
from datetime import datetime

def load_test_history():
    """
    Baca semua file JSON dari folder history/
    dan ubah jadi DataFrame.
    """
    history = []
    
    # Pastikan folder history ada
    if not os.path.exists("history"):
        print("❌ Folder 'history/' tidak ditemukan. Jalankan CI dulu!")
        return pd.DataFrame()
    
    # Loop semua file di history/
    for filename in os.listdir("history"):
        if filename.startswith("report_") and filename.endswith(".json"):
            filepath = os.path.join("history", filename)
            
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                
                # Ambil timestamp eksekusi
                execution_time = datetime.fromtimestamp(data["created"])
                
                # Loop setiap test dalam laporan
                for test in data["tests"]:
                    test_name = test["nodeid"]
                    outcome = test["outcome"]  # passed, failed, skipped
                    duration = test["call"]["duration"]  # durasi eksekusi
                    
                    # Simpan ke list
                    history.append({
                        "timestamp": data["created"],
                        "execution_time": execution_time,
                        "test_name": test_name,
                        "outcome": outcome,
                        "duration_sec": round(duration, 3)
                    })
                    
            except Exception as e:
                print(f"⚠️ Error baca {filename}: {e}")
    
    # Ubah ke DataFrame
    df = pd.DataFrame(history)
    
    # Urutkan berdasarkan waktu
    df = df.sort_values("timestamp").reset_index(drop=True)
    
    return df

# --- Jalankan fungsi ---
df = load_test_history()

# Tampilkan hasil
if not df.empty:
    print(f"\n✅ Berhasil muat {len(df)} record dari {df['execution_time'].dt.date.nunique()} hari")
    print("\n--- 5 Baris Pertama ---")
    print(df.head().to_string(index=False))
    
    print("\n--- Statistik Per Test ---")
    summary = df.groupby("test_name")["outcome"].value_counts().unstack(fill_value=0)
    print(summary)
    
    print("\n--- Rata-rata Durasi Eksekusi ---")
    avg_duration = df.groupby("test_name")["duration_sec"].mean()
    print(avg_duration.round(3))
else:
    print("❌ Tidak ada data yang dimuat. Cek folder history/")