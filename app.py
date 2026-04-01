import streamlit as st
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Banana Detection", layout="wide")

st.title("🍌 Banana Ripeness Detection")

@st.cache_resource
def load_model():
    try:
        from ultralytics import YOLO
        import sys
        # Force reload ultralytics
        if 'ultralytics' in sys.modules:
            import importlib
            importlib.reload(sys.modules['ultralytics'])
        
        model_path = "model/best.pt"
        if os.path.exists(model_path):
            return YOLO(model_path)
        else:
            st.error(f"Model not found at {model_path}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

model = load_model()

if model:
    uploaded = st.file_uploader("Upload banana image", type=["jpg", "jpeg", "png"])
    
    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        st.image(img, width=400)
        
        if st.button("Detect"):
            with st.spinner("Analyzing..."):
                results = model(img)
                
                for r in results:
                    boxes = r.boxes
                    if boxes is not None and len(boxes) > 0:
                        for box in boxes:
                            conf = float(box.conf[0])
                            cls = int(box.cls[0])
                            label = r.names[cls]
                            st.success(f"{label}: {conf:.0%}")
                    else:
                        st.warning("No banana detected")