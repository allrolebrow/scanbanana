import streamlit as st
import numpy as np
from PIL import Image
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
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Cormorant+Garamond:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #111312 !important;
    color: #ECE9E1 !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
    max-width: 1250px !important;
}

h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #F4F1EA !important;
    letter-spacing: -0.02em;
}

p, label, div, span {
    font-family: 'Inter', sans-serif !important;
}

.hero-wrap {
    background: linear-gradient(135deg, #171917 0%, #141614 100%);
    border: 1px solid #232623;
    border-radius: 24px;
    padding: 2.6rem 2.4rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.18);
}

.kicker {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #B7C96B;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    line-height: 1.05;
    font-weight: 500;
    color: #F3F0E8;
    margin-bottom: 0.9rem;
}

.hero-title em {
    color: #C6D96A;
    font-style: italic;
}

.hero-desc {
    color: #A7A89E;
    font-size: 0.98rem;
    line-height: 1.8;
    max-width: 700px;
}

.metric-card {
    background: #171917;
    border: 1px solid #232623;
    border-radius: 18px;
    padding: 1.1rem 1rem;
    text-align: center;
    box-shadow: 0 4px 18px rgba(0,0,0,0.14);
}
.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.9rem;
    color: #F4F1EA;
    line-height: 1;
}
.metric-label {
    margin-top: 0.35rem;
    font-size: 0.75rem;
    color: #8C8F84;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
}

.card {
    background: #171917;
    border: 1px solid #232623;
    border-radius: 22px;
    padding: 1.2rem 1.2rem 1rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.14);
    height: 100%;
}

.card-title {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #8C8F84;
    font-weight: 700;
    margin-bottom: 0.25rem;
}

.card-sub {
    font-size: 1rem;
    color: #ECE9E1;
    font-weight: 500;
    margin-bottom: 1rem;
}

.status-box {
    border-radius: 18px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    border: 1px solid;
}

.status-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    line-height: 1;
    margin-bottom: 0.25rem;
}

.status-sub {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
    opacity: 0.85;
}

.tip-box {
    background: #141614;
    border: 1px solid #232623;
    border-left: 4px solid #C6D96A;
    border-radius: 14px;
    padding: 1rem 1rem;
    color: #B9B8AF;
    line-height: 1.7;
    font-size: 0.92rem;
}

.empty-box {
    border: 1px dashed #2B2E2A;
    border-radius: 18px;
    padding: 2.4rem 1.2rem;
    text-align: center;
    color: #7F8277;
    background: #141614;
}

.stButton > button {
    width: 100%;
    border-radius: 14px !important;
    border: 1px solid #B9CD63 !important;
    background: #C6D96A !important;
    color: #161813 !important;
    font-weight: 700 !important;
    height: 44px !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    opacity: 0.95;
}

[data-testid="stDownloadButton"] > button {
    width: 100%;
    border-radius: 14px !important;
    background: transparent !important;
    color: #D8D5CD !important;
    border: 1px solid #31342F !important;
    height: 42px !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: #B9CD63 !important;
    color: #F4F1EA !important;
}

[data-testid="stFileUploader"] {
    border-radius: 16px !important;
    border: 1px dashed #343832 !important;
    background: #141614 !important;
}

[data-testid="stTabs"] [role="tablist"] {
    gap: 0.5rem;
    margin-bottom: 1rem;
}
[data-testid="stTabs"] [role="tab"] {
    border-radius: 999px !important;
    padding: 0.55rem 1.1rem !important;
    background: #171917 !important;
    border: 1px solid #252824 !important;
    color: #9A9D92 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #161813 !important;
    background: #C6D96A !important;
    border-color: #C6D96A !important;
}

[data-testid="stImage"] img {
    border-radius: 18px !important;
    border: 1px solid #232623 !important;
}

hr {
    border: none;
    border-top: 1px solid #232623;
    margin: 1.5rem 0;
}
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
        # Cari model di beberapa lokasi
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

def infer(model, arr, conf, imgsz=640):
    t0 = time.time()
    res = model.predict(arr, conf=conf, imgsz=imgsz, verbose=False)
    return res, time.time() - t0

def annotate(res):
    # plot() mengembalikan gambar dalam format RGB
    return res[0].plot(line_width=2, font_size=11, labels=True, conf=True)

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
                arr = np.array(pil)
                res, t = infer(model, arr, conf_thresh, img_size)
                ann = annotate(res)
                dets = parse(res)

            st.image(ann, use_container_width=True)
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            render_result(dets, t)

            if dets:
                buf = io.BytesIO()
                Image.fromarray(ann).save(buf, format="PNG")
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
                arr2 = np.array(pil2)
                res2, t2 = infer(model, arr2, conf_thresh, img_size)
                ann2 = annotate(res2)
                dets2 = parse(res2)

            st.image(ann2, use_container_width=True)
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
    BananaLens · Aal Ismu Halat - Johannes Paulus Manik  - Corry Amelia Br Pasaribu
</div>
""", unsafe_allow_html=True)