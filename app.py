import streamlit as st
import os
import base64
from PIL import Image

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aximum-Guard AI", page_icon="🛡️", layout="wide")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_img(name):
    path = os.path.join(BASE_DIR, name)
    if os.path.exists(path):
        return Image.open(path)
    return None

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
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

    /* --- NOUVEAU MENU TRANSPARENT (GLASSMORPHISM) --- */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.2) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }

    /* --- CORRECTION ULTIME DU LOGO AXIMUM --- */
    /* Force un fond blanc propre avec des bords arrondis pour écraser le damier */
    div[data-testid="stSidebar"] div[data-testid="stImage"] {
        background-color: #ffffff !important; 
        padding: 15px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }

    /* --- BALISES DE STATUT DYNAMIQUES --- */
    .status-tag {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
        border: 2px solid transparent;
    }
    .tag-orange { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border-color: #f59e0b; }
    .tag-red { 
        background: rgba(239, 68, 68, 0.2); color: #f87171; border-color: #ef4444; 
        animation: blinker 1s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.3; } }

    /* --- ANIMATIONS DU FOOTER --- */
    .construction-footer {
        position: fixed; bottom: 0; left: 0; width: 100%; height: 130px;
        background: transparent; overflow: hidden; z-index: 0; pointer-events: none; opacity: 0.8;
    }
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

    @keyframes drive-sprint {
        0% { transform: translateX(120vw); }
        13% { transform: translateX(-40vw); } 
        100% { transform: translateX(-40vw); }
    }
    @keyframes drive-left { from { transform: translateX(120vw); } to { transform: translateX(-40vw); } }

    .vibrate { animation: engine-vibrate 0.3s ease-in-out infinite alternate; width: 100%; }
    @keyframes engine-vibrate { from { transform: translateY(0); } to { transform: translateY(-3px); } }

    .worker-static { position: absolute; bottom: 30px; left: 5%; width: 60px; }

    /* --- OLED SCREEN SIMU (ALIGNEMENT PARFAIT) --- */
    .screen-simu {
        background-color: #000000; padding: 20px; border-radius: 20px;
        text-align: center; border: 2px solid #334155;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 25px;
        display: flex; flex-direction: column; align-items: center;
        min-height: 240px; 
    }
    .screen-simu h4 { 
        font-family: 'Courier New', monospace; letter-spacing: 2px; color: white !important; 
        margin: 0; margin-bottom: 20px; width: 100%; border-bottom: 1px solid #333; padding-bottom: 10px;
    }
    .screen-content {
        margin-top: auto; margin-bottom: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO & NAV ---
logo = load_img("AximumIA.png")
if logo: 
    st.sidebar.image(logo, use_container_width=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
else: 
    st.sidebar.error("⚠️ Image 'logo-aximum.png' introuvable")

page = st.sidebar.selectbox("Navigation :", ["👓 Dashboard Lunettes", "🚗 Scénario Vitesse", "🚧 Scénario Collision", "🆘 Scénario Homme Mort"])

# --- 4. PAGES (AVEC AVANT/APRÈS INTÉGRÉ) ---

if page == "👓 Dashboard Lunettes":
    st.title("🛡️ Dashboard Sécurité Connectée")
    col1, col2, col3, col4 = st.columns(4)
    
    # Chargement des pictos en Base64
    b64_casque = get_base64_image(os.path.join(BASE_DIR, "picto_casque.png"))
    b64_danger = get_base64_image(os.path.join(BASE_DIR, "picto_danger.png"))
    b64_vitesse = get_base64_image(os.path.join(BASE_DIR, "picto_vitesse.png"))
    b64_chute = get_base64_image(os.path.join(BASE_DIR, "picto_chute.png"))

    # MAGIE CSS : Ajout de "filter: invert(1);" pour le casque et l'homme au sol
    img_casque = f'<img src="data:image/png;base64,{b64_casque}" width="60" style="margin-bottom:15px; filter: invert(1);">' if b64_casque else ''
    img_danger = f'<img src="data:image/png;base64,{b64_danger}" width="60" style="margin-bottom:15px;">' if b64_danger else ''
    img_vitesse = f'<img src="data:image/png;base64,{b64_vitesse}" width="60" style="margin-bottom:15px;">' if b64_vitesse else ''
    img_chute = f'<img src="data:image/png;base64,{b64_chute}" width="60" style="margin-bottom:15px; filter: invert(1);">' if b64_chute else ''
    
    with col1:
        st.markdown(f"""
            <div class="screen-simu" style="border-color: #3b82f6;">
                <h4>🔵 VIGILANCE</h4>
                <div class="screen-content">
                    {img_casque}<br>
                    <b style="color:white; font-size:1.1em;">CASQUE REQUIS</b><br>
                    <span style="color:#aaa; font-size:0.8em;">Alerte EPI • 1 Vibration</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="screen-simu" style="border-color: #3b82f6;">
                <h4>🔵 INFO</h4>
                <div class="screen-content">
                    {img_danger}<br>
                    <b style="color:white; font-size:1.1em;">ZONE TRAVAUX</b><br>
                    <span style="color:#aaa; font-size:0.8em;">Statut Zone • 1 Vibration</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="screen-simu" style="border-color: #f59e0b;">
                <h4>🟠 RISQUE</h4>
                <div class="screen-content">
                    {img_vitesse}<br>
                    <b style="color:white; font-size:1.1em;">VÉHICULE: 78km/h</b><br>
                    <span style="color:#aaa; font-size:0.8em;">Alerte Vitesse • 2 Vibrations</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="screen-simu" style="border-color: #ef4444;">
                <h4>🔴 DANGER</h4>
                <div class="screen-content">
                    {img_chute}<br>
                    <b style="color:#ef4444; font-size:1.1em;">HOMME AU SOL</b><br>
                    <span style="color:#aaa; font-size:0.8em;">Urgence SOS • 3 Vib + Bip</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

elif page == "🚗 Scénario Vitesse":
    st.title("🚗 Analyse : Intrusion Haute Vitesse")
    col_visuel, col_data = st.columns([2, 1])
    
    with col_visuel:
        v1, v2 = st.columns(2)
        with v1:
            st.caption("📸 Flux Caméra Réel")
            img_brute = load_img("Voiture-Rapide.png")
            if img_brute: st.image(img_brute, use_container_width=True)
            else: st.warning("Image 'Voiture-Rapide.png' manquante.")
        with v2:
            st.caption("🤖 Vision IA Aximum")
            img_ia = load_img("analyse-vitesse.png")
            if img_ia: st.image(img_ia, use_container_width=True)
            else: st.warning("Image 'analyse-vitesse.png' manquante.")

    with col_data:
        st.markdown('<div class="status-tag tag-orange">⚠️ RISQUE DÉTECTÉ</div>', unsafe_allow_html=True)
        st.metric("Vitesse Relevée", "78 km/h", delta="+28 km/h")
        st.write("Analyse YOLOv8 : Menace identifiée en zone amont. Véhicule en net excès de vitesse.")

elif page == "🚧 Scénario Collision":
    st.title("🚧 Analyse : Collision Balisage")
    col_visuel, col_data = st.columns([2, 1])
    
    with col_visuel:
        v1, v2 = st.columns(2)
        with v1:
            st.caption("📸 Flux Caméra Réel")
            img_brute = load_img("Collision-plot.png")
            if img_brute: st.image(img_brute, use_container_width=True)
            else: st.warning("Image 'Collision-plot.png' manquante.")
        with v2:
            st.caption("🤖 Vision IA Aximum")
            img_ia = load_img("analyse-collisionFinal.png")
            if img_ia: st.image(img_ia, use_container_width=True)
            else: st.warning("Image 'analyse-collisionFinal.png' manquante.")

    with col_data:
        st.markdown('<div class="status-tag tag-red">🚨 DANGER IMMINENT</div>', unsafe_allow_html=True)
        st.error("Collision détectée sur matériel Aximum")
        st.write("Vérification périmètre de sécurité requise : Cône de signalisation percuté.")

elif page == "🆘 Scénario Homme Mort":
    st.title("🆘 Analyse : Posture Critique")
    col_visuel, col_data = st.columns([2, 1])
    
    with col_visuel:
        v1, v2 = st.columns(2)
        with v1:
            st.caption("📸 Vues Réelles")
            img_brute1 = load_img("Homme-mort.png")
            img_brute2 = load_img("Homme-mort2.png")
            if img_brute1: st.image(img_brute1, use_container_width=True)
            if img_brute2: st.image(img_brute2, use_container_width=True)
        with v2:
            st.caption("🤖 Analyses IA Correspondantes")
            img_ia1 = load_img("analyse-death1.png")
            img_ia2 = load_img("analyse-death2.png")
            if img_ia1: st.image(img_ia1, use_container_width=True)
            if img_ia2: st.image(img_ia2, use_container_width=True)

    with col_data:
        st.markdown('<div class="status-tag tag-red">🆘 URGENCE VITALE</div>', unsafe_allow_html=True)
        st.metric("Immobilité", "42 sec", delta="Critique")
        st.write("Détection posture anormale prolongée. Alerte envoyée aux secours (eCall).")

# --- 5. FOOTER DYNAMIQUE ---
worker_b64 = get_base64_image(os.path.join(BASE_DIR, "new-worker.png"))
loader_b64 = get_base64_image(os.path.join(BASE_DIR, "new-loader.png"))
truck_b64 = get_base64_image(os.path.join(BASE_DIR, "dumper-truck.png"))
wheel_b64 = get_base64_image(os.path.join(BASE_DIR, "wheel-loader.png"))
car_b64 = get_base64_image(os.path.join(BASE_DIR, "sports-car.png"))

footer_html = """<div class="construction-footer"><div class="road-line"></div>"""

if worker_b64: footer_html += f'<div class="worker-static"><img src="data:image/png;base64,{worker_b64}" style="width:100%;"></div>'
if loader_b64: footer_html += f'<div class="vehicle loader-anim"><img src="data:image/png;base64,{loader_b64}" class="vibrate"></div>'
if truck_b64: footer_html += f'<div class="vehicle truck-slow-anim"><img src="data:image/png;base64,{truck_b64}" class="vibrate"></div>'
if wheel_b64: footer_html += f'<div class="vehicle wheel-loader-anim"><img src="data:image/png;base64,{wheel_b64}" class="vibrate"></div>'
if car_b64: footer_html += f'<div class="vehicle car-fast-anim"><img src="data:image/png;base64,{car_b64}"></div>'

footer_html += "</div>"
st.markdown(footer_html, unsafe_allow_html=True)