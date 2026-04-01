import streamlit as st
import numpy as np
from PIL import Image
import time
import io
import os

# ─────────────────────────────────────────────────────────────
# MODEL
# ─────────────────────────────────────────────────────────────
RIPE = {
    # ... (sama seperti sebelumnya)
}

def norm(raw):
    # ... (sama seperti sebelumnya)

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

def infer(model, arr, conf, imgsz=640):
    t0 = time.time()
    # arr sudah dalam format RGB, langsung gunakan
    res = model.predict(arr, conf=conf, imgsz=imgsz, verbose=False)
    return res, time.time() - t0

def annotate(res):
    # plot() mengembalikan gambar dalam format RGB
    return res[0].plot(line_width=2, font_size=11, labels=True, conf=True)

def parse(res):
    # ... (sama seperti sebelumnya)

def render_result(dets, t):
    # ... (sama seperti sebelumnya)

# ─────────────────────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────────────────────
with st.spinner("Memuat model..."):
    model = load_model()

if model is None:
    st.stop()

# ... (sisanya sama, tapi ubah bagian yang menggunakan cv2)

# Di bagian TAB 1:
if uploaded and run:
    with st.spinner("Menganalisis gambar..."):
        arr = np.array(pil)  # sudah dalam format RGB
        res, t = infer(model, arr, conf_thresh, img_size)
        ann = annotate(res)  # langsung dapat gambar RGB
        dets = parse(res)
    
    st.image(ann, use_container_width=True)
    # ... sisanya sama

# Di bagian TAB 2:
if cam and cam_run:
    with st.spinner("Menganalisis foto..."):
        pil2 = Image.open(cam).convert("RGB")
        arr2 = np.array(pil2)  # sudah dalam format RGB
        res2, t2 = infer(model, arr2, conf_thresh, img_size)
        ann2 = annotate(res2)
        dets2 = parse(res2)
    
    st.image(ann2, use_container_width=True)
    # ... sisanya sama