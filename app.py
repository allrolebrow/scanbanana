import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
import io
import os

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BananaLens · Ripeness Detection",
    page_icon="🍌",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────
# CSS (sama seperti sebelumnya - saya singkat)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ... CSS sama seperti sebelumnya ... */
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MODEL
# ─────────────────────────────────────────────────────────────
RIPE = {
    "mentah": {
        "bg": "#0F1A24", "border": "#223649", "text": "#8EC5FF",
        "label_en": "Unripe",
        "tip": "Pisang masih keras dan belum siap dikonsumsi. Simpan pada suhu ruang selama 2–4 hari agar proses pematangan berjalan alami.",
        "bar": "#5AA8FF",
    },
    "matang": {
        "bg": "#161C0D", "border": "#35411C", "text": "#C6D96A",
        "label_en": "Ripe",
        "tip": "Kondisi ideal untuk dikonsumsi. Jika ingin lebih awet, simpan di kulkas agar kematangan melambat.",
        "bar": "#C6D96A",
    },
    "terlalu matang": {
        "bg": "#21150D", "border": "#4A2A16", "text": "#F2A66A",
        "label_en": "Overripe",
        "tip": "Sangat cocok untuk olahan seperti smoothie, banana bread, pancake, atau campuran adonan kue.",
        "bar": "#F2A66A",
    },
}

def norm(raw):
    r = raw.lower().strip()
    for k in RIPE:
        if k in r:
            return k
    return r

@st.cache_resource(show_spinner=False)
def load_model():
    try:
        from ultralytics import YOLO
        model_paths = [
            "model/best.pt",
            os.path.join(os.path.dirname(__file__), "model", "best.pt"),
        ]
        for p in model_paths:
            if os.path.exists(p):
                return YOLO(p)
        st.error("File model tidak ditemukan. Pastikan file `model/best.pt` ada di repositori.")
        return None
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        return None

def infer(model, img_pil, conf, imgsz=640):
    """Menerima PIL Image, return hasil YOLO"""
    t0 = time.time()
    # Konversi PIL ke numpy array (RGB)
    img_array = np.array(img_pil)
    res = model.predict(img_array, conf=conf, imgsz=imgsz, verbose=False)
    return res, time.time() - t0

def draw_boxes(pil_img, results):
    """Gambar bounding box menggunakan PIL (tanpa OpenCV)"""
    img = pil_img.copy()
    draw = ImageDraw.Draw(img)
    
    boxes = results[0].boxes
    if boxes is None or len(boxes) == 0:
        return img
    
    # Ambil ukuran gambar untuk scaling (jika perlu)
    width, height = img.size
    
    for box in boxes:
        # Ambil koordinat box
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        label = results[0].names[cls]
        
        # Warna berdasarkan kelas
        if "mentah" in label.lower():
            color = (142, 197, 255)  # biru muda
        elif "matang" in label.lower():
            color = (198, 217, 106)  # hijau kekuningan
        else:
            color = (242, 166, 106)  # oranye
        
        # Gambar rectangle
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        
        # Gambar teks label
        text = f"{label} {conf:.0%}"
        # Estimasi ukuran teks (PIL tidak punya textsize di versi lama)
        draw.text((x1, y1 - 20), text, fill=color)
    
    return img

def parse(res):
    out = []
    b = res[0].boxes
    if b is None or len(b) == 0:
        return out
    for box in b:
        lbl = res[0].names[int(box.cls[0])]
        out.append({
            "label": norm(lbl),
            "raw": lbl,
            "conf": float(box.conf[0])
        })
    return sorted(out, key=lambda x: x["conf"], reverse=True)

def render_result(dets, t):
    if not dets:
        st.markdown("""
        <div class="empty-box">
            <h4 style="margin-bottom:.5rem;">Tidak ada pisang terdeteksi</h4>
            <p>Coba gunakan gambar yang lebih jelas, cahaya cukup, atau turunkan confidence threshold.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    top = dets[0]
    m = RIPE.get(top["label"], {
        "bg":"#171917", "border":"#2A2D28", "text":"#D0CEC6",
        "label_en": top["raw"], "tip":"—", "bar":"#A7A89E"
    })

    st.markdown(f"""
    <div class="status-box" style="background:{m['bg']}; border-color:{m['border']}">
        <div class="status-name" style="color:{m['text']}">{top['label'].title()}</div>
        <div class="status-sub" style="color:{m['text']}">{m['label_en']}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Confidence", f"{top['conf']:.0%}")
    c2.metric("Objek", f"{len(dets)}")
    c3.metric("Waktu", f"{t*1000:.0f} ms")

    if len(dets) > 1:
        st.markdown("#### Semua Objek Terdeteksi")
        for d in dets:
            st.progress(int(d["conf"] * 100), text=f"{d['label'].title()} — {d['conf']:.1%}")

    st.markdown(f"""
    <div class="tip-box" style="margin-top:1rem;">
        <strong>Saran:</strong> {m['tip']}
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────────────────────
with st.spinner("Memuat model..."):
    model = load_model()

if model is None:
    st.stop()

# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="kicker">Banana Ripeness Detection</div>
    <div class="hero-title">Deteksi kematangan <em>pisang</em> secara instan.</div>
    <div class="hero-desc">
        Upload foto atau ambil gambar langsung dari kamera. Model YOLOv8n akan mendeteksi tingkat kematangan pisang secara cepat dan visual.
    </div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">3</div>
        <div class="metric-label">Kelas</div>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">YOLOv8n</div>
        <div class="metric-label">Model</div>
    </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">Realtime</div>
        <div class="metric-label">Inferensi</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
with st.container():
    st.markdown("### Pengaturan Deteksi")
    c1, c2 = st.columns([2, 2])
    with c1:
        conf_thresh = st.slider("Confidence Threshold", 0.10, 0.95, 0.40, 0.05)
    with c2:
        img_size = st.selectbox("Ukuran Inferensi", [320, 416, 640, 800], index=2)

# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Upload Gambar", "Kamera"])

# ── TAB 1 ──
with tab1:
    L, R = st.columns(2, gap="large")

    with L:
        st.markdown("""
        <div class="card">
            <div class="card-title">Input</div>
            <div class="card-sub">Upload foto pisang</div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload gambar",
            type=["jpg", "jpeg", "png", "webp", "bmp"],
            label_visibility="collapsed"
        )

        run = False
        if uploaded:
            pil = Image.open(uploaded).convert("RGB")
            st.image(pil, use_container_width=True)
            st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)
            run = st.button("Analisis Gambar", use_container_width=True)
        else:
            st.markdown("""
            <div class="empty-box">
                <h4 style="margin-bottom:.4rem;">Belum ada gambar</h4>
                <p>Format yang didukung: JPG, JPEG, PNG, WebP, BMP.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with R:
        st.markdown("""
        <div class="card">
            <div class="card-title">Output</div>
            <div class="card-sub">Hasil deteksi</div>
        """, unsafe_allow_html=True)

        if uploaded and run:
            with st.spinner("Menganalisis gambar..."):
                # Inferensi dengan PIL Image
                res, t = infer(model, pil, conf_thresh, img_size)
                # Gambar bounding box dengan PIL
                annotated_img = draw_boxes(pil, res)
                dets = parse(res)

            st.image(annotated_img, use_container_width=True)
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            render_result(dets, t)

            if dets:
                buf = io.BytesIO()
                annotated_img.save(buf, format="PNG")
                st.download_button(
                    "⬇ Download Hasil",
                    data=buf.getvalue(),
                    file_name=f"bananalens_{dets[0]['label'].replace(' ','_')}.png",
                    mime="image/png",
                    use_container_width=True,
                )
        else:
            st.markdown("""
            <div class="empty-box">
                <h4 style="margin-bottom:.4rem;">Hasil akan muncul di sini</h4>
                <p>Upload gambar lalu klik tombol analisis.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ── TAB 2 ──
with tab2:
    L2, R2 = st.columns(2, gap="large")

    with L2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Kamera</div>
            <div class="card-sub">Ambil foto langsung</div>
        """, unsafe_allow_html=True)

        cam = st.camera_input("Ambil gambar", label_visibility="collapsed")

        if cam:
            st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)
            cam_run = st.button("Analisis Foto", use_container_width=True, key="cam_btn")
        else:
            cam_run = False
            st.markdown("""
            <div class="empty-box">
                <p>Pastikan pisang terlihat jelas, pencahayaan cukup, dan latar belakang tidak terlalu ramai.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with R2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Output</div>
            <div class="card-sub">Hasil deteksi kamera</div>
        """, unsafe_allow_html=True)

        if cam and cam_run:
            with st.spinner("Menganalisis foto..."):
                pil2 = Image.open(cam).convert("RGB")
                res2, t2 = infer(model, pil2, conf_thresh, img_size)
                annotated_img2 = draw_boxes(pil2, res2)
                dets2 = parse(res2)

            st.image(annotated_img2, use_container_width=True)
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            render_result(dets2, t2)
        else:
            st.markdown("""
            <div class="empty-box">
                <h4 style="margin-bottom:.4rem;">Belum ada hasil</h4>
                <p>Ambil foto lalu klik tombol analisis.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#6E7268; font-size:0.9rem; padding-top:0.4rem;">
    BananaLens · Aal Ismu Halat - Johannes Paulus Manik - Corry Amelia Br Pasaribu
</div>
""", unsafe_allow_html=True)