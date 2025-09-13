# scripts/detect_flaky.py

import os
import json
import pandas as pd

def detect_flaky_tests():
    """Deteksi test yang sering berganti status (flaky)"""
    
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
                        "outcome": test["outcome"]
                    })
            except Exception as e:
                print(f"⚠️ Error baca {filename}: {e}")
    
    df = pd.DataFrame(history)
    if df.empty:
        print("❌ Tidak ada data historis.")
        return
    
    # Urutkan per test
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.sort_values(["test_name", "timestamp"])

    # Cari perubahan status
    df['prev_outcome'] = df.groupby("test_name")["outcome"].shift(1)
    df['flipped'] = df['outcome'] != df['prev_outcome']

    flip_count = df.groupby("test_name")["flipped"].sum().reset_index()
    flip_count = flip_count[flip_count["flipped"] > 0]

    if len(flip_count) == 0:
        print("✅ Tidak ada flaky test terdeteksi.")
        return

    print("\n🟡 FLAKY TEST DETECTED:\n")
    for _, row in flip_count.iterrows():
        print(f"🔁 {row['test_name']}")
        print(f"   Jumlah perubahan status: {int(row['flipped'])}\n")

    flip_count.to_csv("data/flaky_tests.csv", index=False)
    print("✅ Hasil disimpan: data/flaky_tests.csv")

if __name__ == "__main__":
    detect_flaky_tests()