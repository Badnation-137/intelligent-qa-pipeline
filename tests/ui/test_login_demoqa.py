# tests/ui/test_login_demoqa.py

import pytest
from playwright.sync_api import sync_playwright, TimeoutError

USERNAME = "grimchannel"
PASSWORD = "Grimchannel141!"

@pytest.mark.ui
def test_login_demoqa():
    with sync_playwright() as p:
        # 🛡️ Args tambahan untuk bypass deteksi headless
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
        )
        page = browser.new_page()

        # 🚀 Set user agent seperti browser normal
        page.set_extra_http_headers({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        })

        max_retries = 3
        for i in range(max_retries):
            try:
                # 🔧 Gunakan timeout lebih besar + wait_until cepat
                page.goto(
                    "https://demoqa.com/login",
                    timeout=60000,
                    wait_until="domcontentloaded"  # Jangan tunggu semua resource
                )
                break  # Berhasil → keluar dari loop
            except TimeoutError:
                if i == max_retries - 1:
                    browser.close()
                    pytest.fail("❌ Gagal membuka halaman setelah 3 kali percobaan")
                print(f"🔁 Ulangi ke-{i+1} karena timeout...")

        # Isi form login
        page.fill("#userName", USERNAME)
        page.fill("#password", PASSWORD)
        page.click("#login")

        # Tunggu navigasi ke profile
        try:
            page.wait_for_url("**/profile", timeout=20000)
        except TimeoutError:
            page.wait_for_selector("text=Profile", timeout=15000)

        # ✅ Verifikasi login berhasil
        assert page.is_visible("text=Profile"), "Login gagal: Tidak menemukan teks 'Profile'"

        # 📸 Ambil screenshot
        page.screenshot(path="data/results/login_success.png")

        browser.close()

    print("✅ Login test passed!")