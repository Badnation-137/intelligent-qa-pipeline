# 🚀 Intelligent QA Pipeline

Sistem **Quality Assurance Otomatis Berbasis AI & CI/CD**  
Menggabungkan otomasi UI, API, dan analisis data untuk prediksi kualitas otomatis.

## 📊 Status CI/CD

![CI Pipeline](https://github.com/Badnation-137/intelligent-qa-pipeline/actions/workflows/ci.yml/badge.svg)

> Ganti `username` dengan username GitHub kamu

## ✅ Fitur Utama

- ✅ Otomasi UI dengan Playwright
- ✅ Otomasi API dengan `requests`
- ✅ Jalankan otomatis di GitHub Actions
- ✅ Laporan JSON otomatis
- ✅ Histori hasil tes tersimpan (`history/`)
- 🚀 Siap untuk AI & prediksi kegagalan

## 🧪 Struktur Proyek
intelligent-qa-pipeline/
├── tests/
│ ├── ui/ # Otomasi web
│ └── api/ # Otomasi API
├── data/results/ # Hasil tes terbaru
├── history/ # Histori hasil tes (untuk AI)
├── .github/workflows/ # CI/CD automation
└── README.md

---


## 🚀 Cara Menjalankan

### Lokal
```bash
# Aktifkan virtual environment
source qa-env/bin/activate  # Linux/macOS
# atau
qa-env\Scripts\activate     # Windows

# Jalankan semua test
pytest tests/ --json-report --json-report-file=data/results/pytest-report.json