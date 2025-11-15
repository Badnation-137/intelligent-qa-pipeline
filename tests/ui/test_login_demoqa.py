# tests/ui/test_login_demoqa.py

import pytest
from playwright.sync_api import sync_playwright, TimeoutError

USERNAME = "grimchannel"
PASSWORD = "Grimchannel141!"

@pytest.mark.ui
def test_login_demoqa():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]  # Lebih stabil di CI
        )
        page = browser.new_page()

        max_retries = 3
        for i in range(max_retries):
            try:
                # 🚀 Gunakan timeout lebih besar + wait_until
                page.goto(
                    "https://demoqa.com/login",
                    timeout=60000,
                    wait_until="domcontentloaded"  # Jangan tunggu resource berat
                )
                break  # Berhasil → keluar dari loop
            except TimeoutError:
                if i == max_retries - 1:
                    browser.close()
                    pytest.fail(f"❌ Gagal membuka halaman setelah {max_retries} kali percobaan")
                print(f"🔁 Ulangi ke-{i+1} karena timeout...")

        # Isi form login
        page.fill("#userName", USERNAME)
        page.fill("#password", PASSWORD)
        page.click("#login")

        # Tunggu navigasi ke profile
        try:
            page.wait_for_url("**/profile", timeout=20000)
        except TimeoutError:
            # Alternatif: cek elemen Profile langsung
            page.wait_for_selector("text=Profile", timeout=15000)

        # ✅ Verifikasi login berhasil
        assert page.is_visible("text=Profile"), "Login gagal: Tidak menemukan teks 'Profile'"

        # 📸 Ambil screenshot
        page.screenshot(path="data/results/login_success.png")

        browser.close()

    print("✅ Login test passed!")