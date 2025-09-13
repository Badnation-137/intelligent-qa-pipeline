# ai/detect_flaky.py

import os
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_flaky_tests():
    """Deteksi flaky test menggunakan Isolation Forest"""
    
    if not os.path.exists("history"):
        print("❌ Folder 'history/' tidak ditemukan.")
        return
    
    history = []
    for filename in os.listdir("history"):
        if filename.startswith("report_") and filename.endswith(".json"):
            filepath = os.path.join("history", filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                timestamp = data["created"]
                for test in data["tests"]:
                    history.append({
                        "timestamp": timestamp,
                        "test_name": test["nodeid"],
                        "outcome": 1 if test["outcome"] == "passed" else 0  # 1=pass, 0=fail
                    })
            except Exception as e:
                print(f"⚠️ Error baca {filename}: {e}")
    
    df = pd.DataFrame(history)
    if df.empty:
        print("❌ Tidak ada data historis.")
        return
    
    # Hitung perubahan status (pass → fail → pass = flaky)
    df = df.sort_values(["test_name", "timestamp"])
    df["prev_outcome"] = df.groupby("test_name")["outcome"].shift(1)
    df["flipped"] = df["outcome"] != df["prev_outcome"]  # apakah status berubah?
    
    flip_count = df.groupby("test_name")["flipped"].sum().reset_index()
    flip_count = flip_count[flip_count["flipped"] > 0]
    
    if len(flip_count) == 0:
        print("✅ Tidak ada flaky test terdeteksi.")
        return
    
    print("\n🟡 FLAKY TEST DETECTED:\n")
    for _, row in flip_count.iterrows():
        print(f"🔁 {row['test_name']}")
        print(f"   Jumlah perubahan status: {int(row['flipped'])}\n")
    
    # Simpan hasil
    flip_count.to_csv("data/flaky_tests.csv", index=False)
    print("✅ Hasil disimpan: data/flaky_tests.csv")

if __name__ == "__main__":
    import json  # tambahkan karena dipakai di dalam loop
    detect_flaky_tests()