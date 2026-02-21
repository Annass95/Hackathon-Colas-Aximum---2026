import streamlit as st
import os
import base64
from PIL import Image
import cv2  # Nouveau
from ultralytics import YOLO  # Nouveau

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aximum-IA", page_icon="🛡️", layout="wide")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Charger le modèle YOLO (Mis en cache pour éviter de ramer)
@st.cache_resource
def load_yolo_model():
    # Assure-toi que yolov8n.pt est bien dans ton dossier assets/
    model_path = os.path.join(ASSETS_DIR, "yolov8n.pt")
    if os.path.exists(model_path):
        return YOLO(model_path)
    return None

model = load_yolo_model()

def load_img(name):
    path = os.path.join(ASSETS_DIR, name)
    if os.path.exists(path):
        return Image.open(path)
    return None

def get_base64_image(name):
    path = os.path.join(ASSETS_DIR, name)
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# --- 2. STYLE CSS COMPLET ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a) !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.2) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stImage"] {
        background-color: #ffffff !important; 
        padding: 15px !important;
        border-radius: 15px !important;
    }
    .status-tag {
        display: inline-block; padding: 8px 20px; border-radius: 10px;
        font-weight: 900; text-transform: uppercase;
    }
    .tag-orange { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border-color: #f59e0b; }
    .tag-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border-color: #ef4444; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    .construction-footer { position: fixed; bottom: 0; left: 0; width: 100%; height: 130px; pointer-events: none; opacity: 0.8; }
    .road-line {
        position: absolute; bottom: 20px; width: 200%; height: 4px;
        background: repeating-linear-gradient(90deg, #fbbf24 0, #fbbf24 40px, transparent 40px, transparent 80px);
        animation: road-move 3s linear infinite;
    }
    @keyframes road-move { from { transform: translateX(0); } to { transform: translateX(-80px); } }
    .vehicle { position: absolute; bottom: 25px; }
    .loader-anim { width: 100px; animation: drive-left 18s linear infinite; }
    .truck-slow-anim { width: 120px; animation: drive-left 30s linear infinite; }
    .wheel-loader-anim { width: 105px; animation: drive-left 30s linear infinite; animation-delay: 10s; }
    .car-fast-anim { width: 90px; animation: drive-sprint 15s linear infinite; }
    @keyframes drive-sprint { 0% { transform: translateX(120vw); } 13% { transform: translateX(-40vw); } 100% { transform: translateX(-40vw); } }
    @keyframes drive-left { from { transform: translateX(120vw); } to { transform: translateX(-40vw); } }
    .vibrate { animation: engine-vibrate 0.3s ease-in-out infinite alternate; }
    @keyframes engine-vibrate { from { transform: translateY(0); } to { transform: translateY(-3px); } }
    .worker-static { position: absolute; bottom: 30px; left: 5%; width: 60px; }
    .screen-simu {
        background-color: #000000; padding: 20px; border-radius: 20px; text-align: center;
        border: 2px solid #334155; min-height: 240px; display: flex; flex-direction: column; align-items: center;
    }
    .screen-simu h4 { font-family: 'Courier New', monospace; color: white !important; border-bottom: 1px solid #333; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO & NAV ---
logo = load_img("AximumIA.png")
if logo: 
    st.sidebar.image(logo, use_container_width=True)
else: 
    st.sidebar.error("⚠️ Image 'AximumIA.png' introuvable dans /assets")

page = st.sidebar.selectbox("Navigation :", [
    "👓 Dashboard Lunettes", 
    "🎥 Live Cam IA",  # Nouvelle page
    "🚗 Scénario Vitesse", 
    "🚧 Scénario Collision", 
    "🆘 Scénario Homme Mort"
])

# --- 4. PAGES ---

if page == "👓 Dashboard Lunettes":
    st.title("🛡️ Dashboard Sécurité Connectée")
    col1, col2, col3, col4 = st.columns(4)
    b64_casque = get_base64_image("picto_casque.png")
    b64_danger = get_base64_image("picto_danger.png")
    b64_vitesse = get_base64_image("picto_vitesse.png")
    b64_chute = get_base64_image("picto_chute.png")
    img_casque = f'<img src="data:image/png;base64,{b64_casque}" width="60" style="filter: invert(1);">' if b64_casque else ''
    img_danger = f'<img src="data:image/png;base64,{b64_danger}" width="60">' if b64_danger else ''
    img_vitesse = f'<img src="data:image/png;base64,{b64_vitesse}" width="60">' if b64_vitesse else ''
    img_chute = f'<img src="data:image/png;base64,{b64_chute}" width="60" style="filter: invert(1);">' if b64_chute else ''
    with col1:
        st.markdown(f'<div class="screen-simu" style="border-color: #3b82f6;"><h4>🔵 VIGILANCE</h4><div class="screen-content">{img_casque}<br><b style="color:white;">CASQUE REQUIS</b></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="screen-simu" style="border-color: #3b82f6;"><h4>🔵 INFO</h4><div class="screen-content">{img_danger}<br><b style="color:white;">ZONE TRAVAUX</b></div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="screen-simu" style="border-color: #f59e0b;"><h4>🟠 RISQUE</h4><div class="screen-content">{img_vitesse}<br><b style="color:white;">78 km/h</b></div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="screen-simu" style="border-color: #ef4444;"><h4>🔴 DANGER</h4><div class="screen-content">{img_chute}<br><b style="color:#ef4444;">HOMME AU SOL</b></div></div>', unsafe_allow_html=True)

elif page == "🎥 Live Cam IA":
    st.title("🎥 Flux Caméra : Analyse Prédictive")
    st.write("Démonstration de la détection YOLOv8 en temps réel sur un flux vidéo.")
    
    # Switch ON/OFF pour l'IA
    mode_ia = st.toggle("🤖 Activer l'Analyse IA YOLOv8", value=True)
    
    video_path = os.path.join(ASSETS_DIR, "video-chantier.mp4")
    
    if not os.path.exists(video_path):
        st.error(f"Fichier vidéo 'video-chantier.mp4' introuvable dans le dossier assets.")
    elif model is None:
        st.error("Le modèle 'yolov8n.pt' est introuvable dans le dossier assets.")
    else:
        cap = cv2.VideoCapture(video_path)
        frame_placeholder = st.empty()
        
        # Bouton pour arrêter le flux
        stop_cam = st.button("Arrêter la caméra")
        
        while cap.isOpened() and not stop_cam:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Boucle
                continue
            
            if mode_ia:
                results = model(frame, stream=True, conf=0.4, verbose=False)
                for r in results:
                    frame = r.plot()
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame, channels="RGB", use_container_width=True)
            
        cap.release()

elif page == "🚗 Scénario Vitesse":
    st.title("🚗 Analyse : Intrusion Haute Vitesse")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        img = load_img("Voiture-Rapide.png")
        if img: st.image(img, caption="📸 Flux Réel", use_container_width=True)
    with col_v2:
        img = load_img("analyse-vitesse.png")
        if img: st.image(img, caption="🤖 IA Vision", use_container_width=True)

elif page == "🚧 Scénario Collision":
    st.title("🚧 Analyse : Collision Balisage")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        img = load_img("Collision-plot.png")
        if img: st.image(img, caption="📸 Flux Réel", use_container_width=True)
    with col_v2:
        img = load_img("analyse-collisionFinal.png")
        if img: st.image(img, caption="🤖 IA Vision", use_container_width=True)

elif page == "🆘 Scénario Homme Mort":
    st.title("🆘 Analyse : Posture Critique")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        img = load_img("Homme-mort.png")
        if img: st.image(img, use_container_width=True)
    with col_v2:
        img = load_img("analyse-death1.png")
        if img: st.image(img, use_container_width=True)

# --- 5. FOOTER DYNAMIQUE ---
w_b64 = get_base64_image("new-worker.png")
l_b64 = get_base64_image("new-loader.png")
t_b64 = get_base64_image("dumper-truck.png")
wh_b64 = get_base64_image("wheel-loader.png")
c_b64 = get_base64_image("sports-car.png")

footer_html = f"""<div class="construction-footer"><div class="road-line"></div>
    <div class="worker-static">{"<img src='data:image/png;base64,"+w_b64+"' style='width:100%'>" if w_b64 else ""}</div>
    <div class="vehicle loader-anim">{"<img src='data:image/png;base64,"+l_b64+"' class='vibrate'>" if l_b64 else ""}</div>
    <div class="vehicle truck-slow-anim">{"<img src='data:image/png;base64,"+t_b64+"' class='vibrate'>" if t_b64 else ""}</div>
    <div class="vehicle wheel-loader-anim">{"<img src='data:image/png;base64,"+wh_b64+"' class='vibrate'>" if wh_b64 else ""}</div>
    <div class="vehicle car-fast-anim">{"<img src='data:image/png;base64,"+c_b64+"'>" if c_b64 else ""}</div>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)
