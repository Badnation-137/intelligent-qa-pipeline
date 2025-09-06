# tests/ui/test_login_demoqa.py

import pytest
from playwright.sync_api import sync_playwright

# Data login (gunakan akun yang sudah dibuat di demoqa.com)
USERNAME = "grimchannel"
PASSWORD = "Grimchannel141!"

@pytest.mark.ui
def test_login_demoqa():
    with sync_playwright() as p:
        # Jalankan browser (headless=False agar bisa lihat prosesnya)
        browser = p.chromium.launch(headless=False, slow_mo=500)  # slow_mo: jeda 500ms tiap aksi
        page = browser.new_page()

        # Buka halaman login
        page.goto("https://demoqa.com/login")

        # Isi form login
        page.fill("#userName", USERNAME)
        page.fill("#password", PASSWORD)

        # Submit
        page.click("#login")

        # Tunggu halaman redirect
        page.wait_for_timeout(2000)

        # Verifikasi login berhasil (cek ada teks "Profile")
        assert page.is_visible("text=Profile"), "Login gagal: Tidak menemukan teks 'Profile'"

        # Ambil hasil screenshot (opsional, untuk dokumentasi)
        page.screenshot(path="data/results/login_success.png")

        # Tutup browser
        browser.close()

    print("✅ Login test passed!")