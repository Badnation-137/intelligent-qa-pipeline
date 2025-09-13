# scripts/validate_api_response.py

import json
import requests

def validate_users_api():
    """Validasi respons API /users"""
    
    url = "https://jsonplaceholder.typicode.com/users"
    
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Status code bukan 200: {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Respons bukan array"
        assert len(data) >= 10, f"Hanya dapat {len(data)} user"
        
        # Validasi struktur satu user
        user = data[0]
        required_fields = ["id", "name", "email", "address", "phone"]
        for field in required_fields:
            assert field in user, f"Field '{field}' tidak ditemukan"
        
        print("✅ API /users valid!")
        
    except Exception as e:
        print(f"❌ Validasi gagal: {e}")

if __name__ == "__main__":
    validate_users_api()