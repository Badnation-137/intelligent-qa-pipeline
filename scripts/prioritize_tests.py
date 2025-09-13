# scripts/prioritize_tests.py

import os
import joblib
from datetime import datetime

def prioritize_tests():
    """Urutkan test dari risiko tertinggi ke terendah menggunakan model AI"""
    
    model_path = 'ai/models/failure_prediction_model.pkl'
    encoder_path = 'ai/models/test_name_encoder.pkl'

    if not os.path.exists(model_path):
        print('❌ Model tidak ditemukan. Jalankan: python ai/train_failure_model.py')
        return []
    
    try:
        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)
    except Exception as e:
        print(f'❌ Gagal muat model: {e}')
        return []

    # Daftar semua test
    all_tests = [
        'tests/api/test_api_users.py::test_get_all_users',
        'tests/ui/test_login_demoqa.py::test_login_demoqa'
    ]

    # Fitur kontekstual
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    is_weekend = int(day_of_week >= 5)
    duration_ratio = 1.0

    # Prediksi risiko
    test_risks = []
    for name in all_tests:
        try:
            encoded = encoder.transform([name])[0]
        except ValueError:
            encoded = 0

        features = [[encoded, hour, day_of_week, is_weekend, duration_ratio]]
        prob = model.predict_proba(features)[0][1]  # prob gagal

        test_risks.append((name, prob))

    # Urutkan: risiko tertinggi dulu
    prioritized = sorted(test_risks, key=lambda x: x[1], reverse=True)

    print('\n⚡ PRIORITY ORDER (High-Risk First)\n')
    for i, (name, prob) in enumerate(prioritized, 1):
        risk = '🔴 TINGGI' if prob > 0.5 else '🟡 SEDANG' if prob > 0.2 else '🟢 RENDAH'
        print(f'{i}. {risk} {name}')
        print(f'   Probabilitas Gagal: {prob:.2%}\n')

    # Simpan urutan
    with open('data/prioritized_tests.txt', 'w') as f:
        for name, _ in prioritized:
            f.write(f"{name}\n")

    print("✅ Urutan test disimpan: data/prioritized_tests.txt")
    return [name for name, _ in prioritized]

if __name__ == "__main__":
    prioritize_tests()