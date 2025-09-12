# ai/predict_risk.py

import os
import joblib
import sys
from datetime import datetime

def predict_risk():
    # Path ke model
    model_path = 'ai/models/failure_prediction_model.pkl'
    
    if not os.path.exists(model_path):
        print('❌ Model tidak ditemukan. Jalankan train_failure_model.py dulu!')
        return

    try:
        model = joblib.load(model_path)
        encoder = joblib.load('ai/models/test_name_encoder.pkl')
    except Exception as e:
        print(f'❌ Gagal muat model: {e}')
        return

    # Daftar test
    test_names = [
        'tests/api/test_api_users.py::test_get_all_users',
        'tests/ui/test_login_demoqa.py::test_login_demoqa'
    ]

    # Fitur waktu
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    is_weekend = int(day_of_week >= 5)
    duration_ratio = 1.0

    print('\n🔍 PREDIKSI RISIKO KEGAGALAN (AI-Powered)\n')

    for name in test_names:
        try:
            encoded = encoder.transform([name])[0]
        except ValueError:
            encoded = 0

        features = [[encoded, hour, day_of_week, is_weekend, duration_ratio]]
        prob = model.predict_proba(features)[0][1]  # prob gagal

        risk = '🔴 TINGGI' if prob > 0.5 else '🟡 SEDANG' if prob > 0.2 else '🟢 RENDAH'
        print(f'{risk} {name}')
        print(f'   Probabilitas Gagal: {prob:.2%}\n')

if __name__ == "__main__":
    predict_risk()
