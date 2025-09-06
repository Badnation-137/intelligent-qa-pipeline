# tests/api/test_api_users.py

import pytest
import requests
import json

# 🔗 API endpoint publik
API_URL = "https://jsonplaceholder.typicode.com/users"
@pytest.mark.api
def test_get_all_users():
    # 🔹 Kirim request GET
    response = requests.get(API_URL)

    # 🔹 Cek status code (harus 200)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # 🔹 Ambil data JSON
    data = response.json()

    # 🔹 Cek jumlah data (minimal 10 user)
    assert len(data) >= 10, f"Hanya dapat {len(data)} user, seharusnya >= 10"

    # 🔹 Simpan hasil ke file
    with open("data/results/api_users_response.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Berhasil ambil {len(data)} user dari API")