# dashboard/quality_dashboard.py

import os
import json
import pandas as pd
from datetime import datetime

def build_quality_dashboard():
    """Buat ringkasan kualitas dari histori tes"""
    
    if not os.path.exists("history"):
        print("❌ Folder 'history/' tidak ditemukan.")
        return
    
    summary = []
    for filename in os.listdir("history"):
        if filename.startswith("report_") and filename.endswith(".json"):
            filepath = os.path.join("history", filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                
                timestamp = datetime.fromtimestamp(data["created"])
                total = data["summary"]["total"]
                passed = data["summary"]["passed"]
                failed = total - passed
                
                for test in data["tests"]:
                    summary.append({
                        "Date": timestamp.strftime("%Y-%m-%d"),
                        "Time": timestamp.strftime("%H:%M"),
                        "Test": test["nodeid"],
                        "Outcome": test["outcome"].upper(),
                        "Duration (s)": round(test["call"]["duration"], 3)
                    })
            except Exception as e:
                print(f"⚠️ Error: {e}")
    
    df = pd.DataFrame(summary)
    if df.empty:
        print("❌ Tidak ada data.")
        return
    
    print("\n📊 DASHBOARD KUALITAS\n")
    print("1. Ringkasan Per Test:")
    print(df.groupby("Test")["Outcome"].value_counts().unstack(fill_value=0))
    
    print("\n2. Trend Harian:")
    daily = df.groupby("Date")["Outcome"].value_counts().unstack(fill_value=0)
    print(daily)
    
    print("\n3. Rata-rata Durasi:")
    print(df.groupby("Test")["Duration (s)"].mean().round(3))
    
    # Simpan ke CSV
    df.to_csv("dashboard/quality_report.csv", index=False)
    print("\n✅ Laporan disimpan: dashboard/quality_report.csv")

if __name__ == "__main__":
    build_quality_dashboard()