# ai/predict_risk.py

import os
import joblib
import pandas as pd
import sys
from datetime import datetime

# 🔧 Tambahkan path ke jira_integration secara manual
jira_path = os.path.join(os.path.dirname(__file__), '..', 'jira_integration')
if jira_path not in sys.path:
    sys.path.append(jira_path)

# Sekarang coba import
try:
    from create_issue import create_jira_task
    print("✅ Berhasil import create_jira_task")
except ImportError as e:
    print(f"❌ Gagal import: {e}")
    create_jira_task = None

# Daftar nama fitur — harus SAMA dengan saat training
FEATURE_NAMES = [
    'test_encoded',
    'hour',
    'day_of_week',
    'is_weekend',
    'duration_ratio'
]

def predict_risk():
    model_path = 'ai/models/failure_prediction_model.pkl'
    encoder_path = 'ai/models/test_name_encoder.pkl'

    if not os.path.exists(model_path):
        print('❌ Model tidak ditemukan.')
        return

    try:
        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)
    except Exception as e:
        print(f'❌ Gagal muat model: {e}')
        return

    test_names = [
        'tests/api/test_api_users.py::test_get_all_users',
        'tests/ui/test_login_demoqa.py::test_login_demoqa'
    ]

    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()  # 0=Senin, ..., 6=Minggu
    is_weekend = int(day_of_week >= 5)
    duration_ratio = 1.0

    print('\n🔍 PREDIKSI RISIKO KEGAGALAN (AI-Powered)\n')

    for name in test_names:
        try:
            encoded = encoder.transform([name])[0]
        except (ValueError, AttributeError):
            encoded = 0

        # Kirim sebagai DataFrame dengan nama kolom
        features_df = pd.DataFrame([[
            encoded,
            hour,
            day_of_week,
            is_weekend,
            duration_ratio
        ]], columns=FEATURE_NAMES)

        try:
            prob = model.predict_proba(features_df)[0][1]  # Probabilitas gagal
        except Exception as e:
            print(f"❌ Gagal prediksi untuk {name}: {e}")
            prob = 0.0

        risk = '🔴 TINGGI' if prob > 0.5 else '🟡 SEDANG' if prob > 0.2 else '🟢 RENDAH'
        print(f'{risk} {name}')
        print(f'   Probabilitas Gagal: {prob:.2%}\n')

        # 🔥 Auto-create ticket di Jira jika risiko tinggi & test UI
        if create_jira_task is not None and prob > 0.15 and "ui" in name.lower():
            create_jira_task(
                summary=f"🚨 High Risk Detected: {name}",
                description_text=f"Model AI memprediksi bahwa test UI `{name}` memiliki probabilitas gagal sebesar {prob:.2%}. Disarankan segera diperiksa oleh tim dev/QA."
            )

        elif prob > 0.5 and "api" in name.lower():
            print(f"ℹ️  Risiko tinggi pada API test diabaikan untuk ticket otomatis.")

if __name__ == "__main__":
    predict_risk()