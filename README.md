# 🍌 BananaLens — Banana Ripeness Detection

Aplikasi web berbasis **Streamlit** untuk mendeteksi tingkat kematangan pisang secara real-time menggunakan model **YOLOv8n**.

---

## 🗂 Struktur Proyek

```
banana-detection/
├── app.py               ← Aplikasi utama Streamlit
├── requirements.txt     ← Dependensi Python
├── README.md
└── model/
    └── best.pt          ← ⬅ Letakkan model kamu di sini
```

---

## 🚀 Cara Menjalankan

### 1. Clone / ekstrak proyek

```bash
cd banana-detection
```

### 2. Buat virtual environment (opsional, disarankan)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependensi

```bash
pip install -r requirements.txt
```

### 4. Letakkan model

Salin file `best.pt` ke dalam folder `model/`:

```
banana-detection/
└── model/
    └── best.pt   ← di sini
```

### 5. Jalankan aplikasi

```bash
streamlit run app.py
```

Buka browser → `http://localhost:8501`

---

## 🎯 Fitur

| Fitur | Deskripsi |
|---|---|
| Upload Gambar | JPG, PNG, WebP, BMP |
| Kamera Real-Time | Ambil foto langsung dari browser |
| Confidence Slider | Atur threshold deteksi |
| Bounding Box | Visualisasi lokasi pisang |
| Saran Konsumsi | Tips berdasarkan tingkat kematangan |
| Download Hasil | Export gambar hasil deteksi |

---

## 🏷 Kelas Deteksi

- 🟦 **Mentah** — Pisang masih keras, perlu waktu matang
- 🟩 **Matang** — Kondisi optimal untuk dikonsumsi  
- 🟧 **Terlalu Matang** — Cocok untuk smoothie / banana bread

---

## 📦 Tech Stack

- **Frontend**: Streamlit (custom CSS dark theme)
- **Model**: YOLOv8n (Ultralytics)
- **Image Processing**: OpenCV, Pillow
- **Deep Learning**: PyTorch
"# BananaLens" 
"# BananaLens" 
