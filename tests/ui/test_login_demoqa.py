# tests/ui/test_login_demoqa.py

import pytest
from playwright.sync_api import sync_playwright

USERNAME = "grimchannel"
PASSWORD = "Grimchannel141!"

@pytest.mark.ui
def test_login_demoqa():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=0)
        page = browser.new_page()

        # ✅ URL benar-benar tanpa spasi!
        page.goto("https://demoqa.com/login")

        page.fill("#userName", USERNAME)
        page.fill("#password", PASSWORD)
        page.click("#login")

        # 🔧 Fix: pakai load state yang lebih stabil di CI
        try:
            page.wait_for_url("**/profile", timeout=15000)
        except:
            page.wait_for_load_state("load", timeout=15000)

        # Verifikasi login berhasil
        assert page.is_visible("text=Profile"), "Login gagal: Tidak menemukan teks 'Profile'"

        # Ambil screenshot
        page.screenshot(path="data/results/login_success.png")

        browser.close()

    print("✅ Login test passed!")
