# 🛠️ CI/CD Configuration

Dokumentasi resmi untuk **Intelligent QA Pipeline** — sistem otomasi kualitas berbasis AI & cloud.

---

## 🔄 Alur Pipeline

```mermaid
graph TD
    A[Push ke GitHub] --> B[Checkout Kode]
    B --> C[Setup Python & Dependencies]
    C --> D[Prediksi Risiko dengan AI]
    D --> E[Prioritaskan Test Berisiko Tinggi]
    E --> F[Jalankan Otomasi UI/API]
    F --> G[Simpan Laporan JSON]
    G --> H[Upload Histori Hasil Tes]
```

---

## 📋 Detail Jobs

| Job | Deskripsi |
|-----|-----------|
| `Setup Python` | Install Python 3.10 |
| `Install dependencies` | Install pytest, Playwright, scikit-learn, pandas, joblib |
| `🔮 Predict Risk` | Jalankan model AI untuk prediksi risiko kegagalan |
| `⚡ Prioritize Tests` | Urutkan test: high-risk first |
| `🧪 Run UI & API Tests` | Jalankan otomasi web & API |
| `📤 Upload test report` | Simpan hasil ke artifact (`test-results`) |
| `📁 Save historical report` | Backup ke `history/` dengan timestamp |

---

## ⚙️ Workflow File

- Lokasi: `.github/workflows/ci.yml`  
- Trigger: `push` atau `pull_request` ke `main`  
- Runner: `ubuntu-latest`  
- Bahasa: Python 3.10  

---

## 📦 Artifact yang Dihasilkan

| Nama Artifact | Isi | Digunakan Untuk |
|---------------|-----|-----------------|
| `test-results` | `pytest-report.json` | Debug hasil terbaru |
| `test-history` | Semua file `history/report_*.json` | Analisis tren & pelatihan AI |

---

## 🔐 Best Practices

1. ✅ Gunakan `headless=True` di server  
2. ✅ Hindari `slow_mo` di production  
3. ✅ Simpan model AI di `models/` jika < 50MB  
4. ✅ Jangan tulis script panjang di `run:` → gunakan file `.py` eksternal  
5. ✅ Gunakan emoji di nama step → lebih mudah dibaca:  
   - `🔮 Predict Test Failure Risk`  
   - `⚡ Prioritize Tests by Risk`  

---

## 🔗 Referensi Resmi

- [GitHub Actions Docs](https://docs.github.com/en/actions)  
- [Playwright CI Guide](https://playwright.dev/python/docs/ci)  
- [Pytest JSON Report](https://pypi.org/project/pytest-json-report/)  
