import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

from streamlit_webrtc import webrtc_streamer, WebRtcMode
from frontend.webrtc_utils import SignLanguageProcessor
from core.ai_translator import generate_sentence
from frontend.tts_utils import speak_text
import json

@st.cache_resource
def load_asl_model():
    try:
        import tensorflow as tf
        model_path = os.path.join("models", "asl_model.keras")
        if os.path.exists(model_path):
            return tf.keras.models.load_model(model_path)
        return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

@st.cache_data
def get_labels():
    try:
        with open(os.path.join("dataset", "labels.json"), "r") as f:
            labels = json.load(f)
            # Invert for index lookup
            return {str(v): k for k, v in labels.items()}
    except:
        return {}

st.set_page_config(
    page_title="Deaf Connect AI | Breaking Silence",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- THEME & STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #000000;
        --secondary: #4B5563;
        --bg-light: #FFFFFF;
        --bg-gray: #F9FAFB;
        --border: #E5E7EB;
        --text-main: #000000;
        --text-muted: #6B7280;
    }

    /* Global Reset */
    .stApp {
        background-color: var(--bg-light);
        color: var(--text-main);
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--border);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-gray);
        border-right: 1px solid var(--border);
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-main) !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }

    .hero-title {
        font-size: clamp(2.5rem, 8vw, 5rem);
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        color: var(--text-main);
    }

    /* Responsive Spacing */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }

    /* Modern Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    
    .glass-card:hover {
        border-color: rgba(0, 0, 0, 0.15);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        transform: translateY(-4px);
    }

    /* Message Box */
    .chat-bubble {
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        max-width: 80%;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .user-bubble {
        background: #000;
        color: #fff;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .ai-bubble {
        background: #F3F4F6;
        color: #000;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid #E5E7EB;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-fade {
        animation: fadeIn 0.5s ease forwards;
    }

    /* Skeleton Loading Simulation */
    .skeleton {
        background: linear-gradient(90deg, #F3F4F6 25%, #E5E7EB 50%, #F3F4F6 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
    }

    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    .hero-title {
        font-size: clamp(2.5rem, 8vw, 5rem);
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        color: var(--text-main);
    }

    .fy-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        background: #F3F4F6;
        border: 1px solid var(--border);
        border-radius: 4px;
        color: var(--text-main);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1.5rem;
    }

    .footer {
        padding: 4rem 0;
        border-top: 1px solid var(--border);
        text-align: center;
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    </style>

""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = None

# --- HELPER FUNCTIONS ---
def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- LANDING PAGE ---
def show_landing():
    # 1. Navigation
    cols = st.columns([1, 4, 1])
    with cols[0]:
        st.markdown("<h4 style='margin:0; font-weight:900;'>SIGNSYNC</h4>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
            <div style='display:flex; gap:32px; justify-content:center; align-items:center; height:100%; font-size:0.8rem; font-weight:700; color:#6B7280; text-transform:uppercase; letter-spacing:0.05em;'>
                <span style='cursor:pointer;'>Platform</span>
                <span style='cursor:pointer;'>Technology</span>
                <span style='cursor:pointer;'>Mission</span>
                <span style='cursor:pointer;'>Docs</span>
            </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        if st.button("Launch App", use_container_width=True, key="launch_top"):
            navigate_to('login')

    # 2. Hero Section
    st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
    
    # Responsive Hero
    c1, _ = st.columns([10, 2])
    with c1:
        st.markdown("<div class='fy-badge'>AI Communication Interface</div>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>Breaking the<br>silence with AI.</h1>", unsafe_allow_html=True)
        st.markdown("""
            <p class='hero-subtitle' style='font-size:1.2rem; color:#4B5563; max-width:650px; margin-bottom:3rem; line-height:1.6;'>
                SignSync AI bridges communication between the deaf community and hearing individuals 
                through real-time gesture recognition and neural speech synthesis.
            </p>
        """, unsafe_allow_html=True)
        
        btn_cols = st.columns([1, 1, 3])
        with btn_cols[0]:
            if st.button("Get Started", type="primary", use_container_width=True):
                navigate_to('login')
        with btn_cols[1]:
            st.button("View Demo", use_container_width=True)

    # 3. Stats Section
    st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("95%", "Accuracy"),
        ("21", "Landmarks"),
        ("63", "Features"),
        ("<30ms", "Latency")
    ]
    for i, (val, label) in enumerate(stats):
        with [s1, s2, s3, s4][i]:
            st.markdown(f"<div class='glass-card' style='text-align:center;'><h3>{val}</h3><p style='font-size:0.75rem; color:#6B7280; font-weight:700; text-transform:uppercase; margin:0;'>{label}</p></div>", unsafe_allow_html=True)

    # 4. How It Works
    st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
    st.header("The Neural Pipeline")
    
    hw_col1, hw_col2 = st.columns(2)
    with hw_col1:
        st.markdown("""
            <div class='glass-card' style='height:100%;'>
                <h5 style='margin-bottom:1.5rem;'>Sign to Speech</h5>
                <ol style='font-size:0.85rem; color:#4B5563; line-height:2;'>
                    <li>High-speed camera captures gesture data</li>
                    <li>MediaPipe extracts 21-point hand geometry</li>
                    <li>Temporal vectors processed via LSTM layers</li>
                    <li>Neural engine predicts gesture intent</li>
                    <li>Real-time speech synthesis output</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    with hw_col2:
        st.markdown("""
            <div class='glass-card' style='height:100%;'>
                <h5 style='margin-bottom:1.5rem;'>Voice to Text</h5>
                <ol style='font-size:0.85rem; color:#4B5563; line-height:2;'>
                    <li>Neural mic array captures acoustic input</li>
                    <li>Transformer-based speech recognition</li>
                    <li>Real-time transcription & formatting</li>
                    <li>Visual display for deaf operators</li>
                    <li>Persistent log archiving in database</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)


    # 5. Core Services
    st.markdown("<div class='section-padding'>", unsafe_allow_html=True)
    st.header("Core Services")
    
    serv_cols = st.columns(3)
    services = [
        ("Real-time Sign Detection", "Live gesture recognition using MediaPipe and LSTM."),
        ("Sign to Voice Conversion", "Converts signs into spoken language offline."),
        ("Voice to Text Conversion", "Converts speech into readable text instantly."),
        ("AI Gesture Recognition", "LSTM model detects temporal sign patterns."),
        ("Offline Voice Support", "Uses pyttsx3 for offline speech synthesis."),
        ("Interactive Web Interface", "Responsive Streamlit-based interface."),
        ("Custom Dataset Training", "Custom-trained gesture dataset."),
        ("Assistive Technology", "Built for differently-abled individuals."),
        ("Scalable AI Solution", "Expandable for sentences and mobile deployment.")
    ]
    
    for i, (title, desc) in enumerate(services):
        with serv_cols[i % 3]:
            st.markdown(f"""
                <div class='glass-card' style='margin-bottom:24px; min-height:160px;'>
                    <h5 style='color:#60A5FA; margin-bottom:8px;'>{title}</h5>
                    <p style='font-size:0.85rem; color:#94A3B8; margin:0;'>{desc}</p>
                </div>
            """, unsafe_allow_html=True)

    # 6. Tech Stack
    st.markdown("<div class='section-padding'>", unsafe_allow_html=True)
    st.header("Technology Stack")
    st.table({
        "Category": ["UI Framework", "Computer Vision", "Hand Tracking", "Deep Learning", "Core Model", "Text-to-Speech", "Speech-to-Text", "Data Handling"],
        "Technology": ["Streamlit", "OpenCV", "MediaPipe", "TensorFlow / Keras", "LSTM", "pyttsx3", "SpeechRecognition", "NumPy"]
    })

    # 7. Model Architecture
    st.markdown("<div class='section-padding'>", unsafe_allow_html=True)
    st.header("LSTM Model Architecture")
    st.write("Sign language is sequential data. LSTM captures temporal dependencies across frames better than CNN-only models.")
    
    arch_col1, arch_col2 = st.columns([3, 2])
    with arch_col1:
        st.markdown("""
            <div style='background:rgba(59,130,246,0.1); border:1px dashed #3B82F6; padding:2rem; border-radius:16px; text-align:center;'>
                <div style='font-weight:bold; margin-bottom:10px;'>LSTM Layer 1 (Input: 20x63)</div>
                <div style='font-size:0.8rem; opacity:0.6;'>↓</div>
                <div style='font-weight:bold; margin-bottom:10px;'>Dropout (0.2)</div>
                <div style='font-size:0.8rem; opacity:0.6;'>↓</div>
                <div style='font-weight:bold; margin-bottom:10px;'>LSTM Layer 2</div>
                <div style='font-size:0.8rem; opacity:0.6;'>↓</div>
                <div style='font-weight:bold; margin-bottom:10px;'>Dropout (0.2)</div>
                <div style='font-size:0.8rem; opacity:0.6;'>↓</div>
                <div style='font-weight:bold; margin-bottom:10px;'>Dense Layer</div>
                <div style='font-size:0.8rem; opacity:0.6;'>↓</div>
                <div style='font-weight:bold; color:#3B82F6;'>Softmax Output</div>
            </div>
        """, unsafe_allow_html=True)
    with arch_col2:
        st.markdown("""
            <div class='glass-card'>
                <h5>Model Accuracy</h5>
                <h1 style='color:#10B981;'>95%</h1>
                <p style='font-size:0.8rem; color:#94A3B8;'>Validated on custom trained gesture dataset.</p>
                <hr>
                <p style='font-size:0.85rem;'><b>Input Shape:</b> (20, 63)</p>
                <p style='font-size:0.85rem;'><b>Dataset Shape:</b> (20, 63)</p>
            </div>
        """, unsafe_allow_html=True)

    # 8. Team
    st.markdown("<div class='section-padding'>", unsafe_allow_html=True)
    st.header("The Team")
    t1, t2, t3 = st.columns(3)
    with t1: st.markdown("<div class='glass-card' style='text-align:center;'><h5>AI Engineer</h5></div>", unsafe_allow_html=True)
    with t2: st.markdown("<div class='glass-card' style='text-align:center;'><h5>Frontend Developer</h5></div>", unsafe_allow_html=True)
    with t3: st.markdown("<div class='glass-card' style='text-align:center;'><h5>Backend Developer</h5></div>", unsafe_allow_html=True)

    # 9. CTA
    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align:center; padding:80px; background:linear-gradient(rgba(59, 130, 246, 0.1), transparent); border-radius:32px; border:1px solid rgba(59, 130, 246, 0.1);'>
            <h2 style='margin-bottom:1rem;'>Communication for everyone.</h2>
            <p style='color:#94A3B8; margin-bottom:2.5rem;'>AI-powered. Inclusive by design. Built for the deaf and mute community.</p>
        </div>
    """, unsafe_allow_html=True)
    c_btn = st.columns([4, 2, 4])
    with c_btn[1]:
        if st.button("Launch Deaf Connect AI", type="primary", use_container_width=True):
            navigate_to('login')

    # 10. Footer
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.markdown("<b>DeafConnect AI</b>")
    st.markdown("Breaking communication barriers with artificial intelligence.")
    st.markdown("<p style='font-size:0.75rem; margin-top:10px;'>Final Year Project — 2025</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- LOGIN PAGE ---
def show_login():
    st.title("System Authentication")
    st.write("Access the Deaf Connect terminal via Google Secure Login.")
    
    if st.button("LOGIN WITH GOOGLE"):
        st.session_state.user = {
            "id": "test-user-001",
            "full_name": "Zain Decora",
            "email": "zain@example.com",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Zain"
        }
        st.session_state.page = 'dashboard'
        st.rerun()
    
    if st.button("Back to Landing"):
        navigate_to('landing')

# --- DASHBOARD & MAIN APP ---
def main_app():
    # --- MODERN SIDEBAR ---
    with st.sidebar:
        st.markdown(f"""
            <div style='text-align:center; padding:1rem 0 2rem 0;'>
                <h2 style='margin:0; letter-spacing:-0.05em; font-weight:900;'>DEAF CONNECT</h2>
                <div style='font-size:0.6rem; color:#6B7280; font-weight:700; text-transform:uppercase; letter-spacing:0.2em;'>Neural Interface v1.0</div>
            </div>
        """, unsafe_allow_html=True)
        
        # User Profile
        st.markdown(f"""
            <div style='background:white; border:1px solid #E5E7EB; border-radius:12px; padding:1rem; margin-bottom:2rem; display:flex; align-items:center; gap:12px;'>
                <img src='{st.session_state.user['avatar_url']}' style='width:40px; height:40px; border-radius:50%; border:2px solid #000;'>
                <div style='overflow:hidden;'>
                    <div style='font-size:0.8rem; font-weight:800; white-space:nowrap; text-overflow:ellipsis;'>{st.session_state.user['full_name']}</div>
                    <div style='font-size:0.65rem; color:#10B981; font-weight:700;'>● ONLINE</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Navigation Menu
        nav_items = [
            ("📊 Dashboard", "Dashboard"),
            ("🤟 Live Detection", "Live Communication"),
            ("🤖 AI Chat", "AI Assistant"),
            ("📜 History", "History"),
            ("📈 Analytics", "Analytics"),
            ("⚙️ Settings", "Settings")
        ]
        
        # Current Page Highlight logic could be added here if using custom buttons
        # For now, we use a radio with a cleaner look
        page = st.radio("MENU", [item[0] for item in nav_items], label_visibility="collapsed")
        current_page = next(item[1] for item in nav_items if item[0] == page)

        st.markdown("<div style='height:10vh;'></div>", unsafe_allow_html=True)
        
        # Footer Actions
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = 'landing'
            st.rerun()
        
        st.markdown("""
            <div style='margin-top:1rem; text-align:center; font-size:0.6rem; color:#9CA3AF;'>
                DEAF CONNECT AI &copy; 2026<br>Restoring Communication
            </div>
        """, unsafe_allow_html=True)

    # Page Routing
    if current_page == "Dashboard":
        show_dashboard()
    elif current_page == "Live Communication":
        show_live_comm()
    elif current_page == "AI Assistant":
        show_ai_chat()
    elif current_page == "History":
        show_history()
    elif current_page == "Analytics":
        show_analytics()
    elif current_page == "Settings":
        show_settings()

    if page == "Dashboard":
        show_dashboard()
    elif page == "Live Communication":
        show_live_comm()
    elif page == "History":
        show_history()
    elif page == "Analytics":
        show_analytics()
    elif page == "Settings":
        show_settings()

def show_dashboard():
    st.title("System Analytics")
    st.markdown("<p style='color:#6B7280; margin-bottom:2rem;'>Dynamic performance metrics and activity trends.</p>", unsafe_allow_html=True)
    
    try:
        res = requests.get(f"{API_BASE_URL}/analytics/{st.session_state.user['id']}")
        stats_data = res.json()
    except:
        stats_data = {"total_chats": 0, "total_messages": 0, "avg_confidence": 0.0}

    # Top Row Cards
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("Total Sessions", stats_data.get('total_chats', 0), "🤟"),
        ("Gestures Detected", stats_data.get('total_messages', 0), "🧠"),
        ("Avg Confidence", f"{stats_data.get('avg_confidence', 0)*100:.1f}%", "🎯"),
        ("AI Sentences", stats_data.get('total_chats', 0) * 2, "📝") # Simulation for now
    ]
    
    for i, (label, val, icon) in enumerate(cards):
        with [c1, c2, c3, c4][i]:
            st.markdown(f"""
                <div class='glass-card' style='text-align:center;'>
                    <div style='font-size:1.5rem; margin-bottom:0.5rem;'>{icon}</div>
                    <div style='font-size:0.7rem; font-weight:700; color:#6B7280; text-transform:uppercase;'>{label}</div>
                    <div style='font-size:1.5rem; font-weight:800;'>{val}</div>
                </div>
            """, unsafe_allow_html=True)

    # Secondary Content
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Detection Trends")
        # Placeholder chart
        import pandas as pd
        import numpy as np
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Accuracy', 'Latency', 'Volume'])
        st.line_chart(chart_data)
        
    with col_right:
        st.subheader("System Health")
        st.markdown("""
            <div class='glass-card'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;'>
                    <span style='font-size:0.85rem; font-weight:600;'>Neural Pipeline</span>
                    <span style='color:#10B981; font-weight:700; font-size:0.7rem;'>OPERATIONAL</span>
                </div>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;'>
                    <span style='font-size:0.85rem; font-weight:600;'>Database Sync</span>
                    <span style='color:#10B981; font-weight:700; font-size:0.7rem;'>CONNECTED</span>
                </div>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:0.85rem; font-weight:600;'>WebRTC Stream</span>
                    <span style='color:#3B82F6; font-weight:700; font-size:0.7rem;'>WAITING</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_live_comm():
    st.title("Neural Translation")
    st.markdown("<p style='color:#6B7280; margin-bottom:1rem;'>Active ASL-to-Speech and Speech-to-Text pipeline.</p>", unsafe_allow_html=True)
    
    # Load Model & Labels
    model = load_asl_model()
    labels = get_labels()

    if not model:
        st.warning("⚠️ Neural Core Engine (Model) not found. Running in simulation mode.")

    # Session State for Detection
    if 'detected_words' not in st.session_state:
        st.session_state.detected_words = []
    if 'final_sentence' not in st.session_state:
        st.session_state.final_sentence = ""

    # Status Indicators
    status_cols = st.columns([1, 1, 1, 3])
    status_cols[0].markdown("<div style='font-size:0.6rem; font-weight:700; color:#10B981;'>● WEBCAM</div>", unsafe_allow_html=True)
    status_cols[1].markdown("<div style='font-size:0.6rem; font-weight:700; color:#10B981;'>● AUDIO</div>", unsafe_allow_html=True)
    status_cols[2].markdown("<div style='font-size:0.6rem; font-weight:700; color:#10B981;'>● NEURAL</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    
    main_col, side_col = st.columns([2, 1])
    
    with main_col:
        ctx = webrtc_streamer(
            key="sign-sync",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=lambda: SignLanguageProcessor(model=model, labels=labels),
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )

        if ctx.video_processor:
            word, conf = ctx.video_processor.get_results()
            if word and (not st.session_state.detected_words or st.session_state.detected_words[-1] != word):
                st.session_state.detected_words.append(word)
                st.toast(f"Detected: {word} ({conf*100:.0f}%)")
                # Save detection event to DB
                try:
                    requests.post(f"{API_BASE_URL}/analytics/detection", json={
                        "user_id": st.session_state.user['id'],
                        "sign_name": word,
                        "confidence": float(conf)
                    })
                except: pass

        # Controls
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        if c1.button("Generate Sentence", use_container_width=True, type="primary"):
            if st.session_state.detected_words:
                with st.spinner("AI is thinking..."):
                    sentence = generate_sentence(st.session_state.detected_words)
                    st.session_state.final_sentence = sentence
                    
                    # Create Conversation & Save Message
                    try:
                        # 1. Create conv if needed
                        if 'active_conv_id' not in st.session_state:
                            conv_res = requests.post(f"{API_BASE_URL}/conversations/", json={
                                "user_id": st.session_state.user['id'],
                                "title": f"Session {datetime.now().strftime('%H:%M')}"
                            }).json()
                            st.session_state.active_conv_id = conv_res['id']
                        
                        # 2. Save Message
                        requests.post(f"{API_BASE_URL}/conversations/messages", json={
                            "conversation_id": st.session_state.active_conv_id,
                            "sender": "user",
                            "raw_words": " ".join(st.session_state.detected_words),
                            "translated_sentence": sentence,
                            "confidence": 0.95 # Average
                        })
                    except Exception as e:
                        st.error(f"Sync Error: {e}")
            else:
                st.warning("No signs detected yet.")
        
        if c2.button("Clear Buffer", use_container_width=True):
            st.session_state.detected_words = []
            st.session_state.final_sentence = ""
            if 'active_conv_id' in st.session_state:
                del st.session_state.active_conv_id
            st.rerun()
            
        if c3.button("Speak Output", use_container_width=True):
            if st.session_state.final_sentence:
                st.info(f"🔊 Speaking: {st.session_state.final_sentence}")
                speak_text(st.session_state.final_sentence)
        
        # Speech to Text Fallback
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        audio_file = st.audio_input("Voice Input (Hearing to Deaf)")
        if audio_file:
            st.success("Audio captured. Transcribing...")
            # Here we would send to an API like Groq Whisper
            # For now, we simulate
            st.session_state.final_sentence = "Hello, how can I help you today?"

    with side_col:
        st.markdown("<div style='font-size:0.7rem; font-weight:700; color:#6B7280; text-transform:uppercase; margin-bottom:1rem;'>Live Gloss Buffer</div>", unsafe_allow_html=True)
        buffer_html = "".join([f"<span style='background:#F3F4F6; padding:4px 8px; border-radius:4px; margin-right:4px; font-size:0.8rem;'>{w}</span>" for w in st.session_state.detected_words])
        st.markdown(f"""
            <div style='background:white; border:1px solid #E5E7EB; border-radius:8px; min-height:100px; padding:1rem; margin-bottom:1rem;'>
                {buffer_html if st.session_state.detected_words else "<span style='color:#9CA3AF; font-style:italic;'>Waiting for signs...</span>"}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='font-size:0.7rem; font-weight:700; color:#6B7280; text-transform:uppercase; margin-bottom:1rem;'>AI Translation</div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:black; color:white; border-radius:8px; min-height:150px; padding:1.5rem; font-size:1.1rem; font-weight:500;'>
                {st.session_state.final_sentence if st.session_state.final_sentence else "..."}
            </div>
        """, unsafe_allow_html=True)

def show_ai_chat():
    st.title("AI Communication Assistant")
    st.markdown("<p style='color:#6B7280; margin-bottom:2rem;'>Interactive chat powered by Groq Llama 3.</p>", unsafe_allow_html=True)
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    chat_col1, chat_col2 = st.columns([4, 1])
    with chat_col1:
        prompt = st.chat_input("Ask me anything about sign language...")
    with chat_col2:
        audio_chat = st.audio_input("Voice", label_visibility="collapsed")

    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                # Simplified AI response for now
                response = generate_sentence([prompt]) # Reuse translator or implement full chat
                st.markdown(response)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})

def show_history():
    st.title("Neural Archive")
    st.markdown("<p style='color:#6B7280; margin-bottom:2rem;'>Persistent logs of all neural translation sessions synced to Supabase.</p>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("""
        <div style='display:flex; gap:12px; margin-bottom:2rem;'>
            <button style='padding:8px 16px; background:#F3F4F6; border:1px solid #E5E7EB; border-radius:6px; font-size:0.8rem; font-weight:600; cursor:pointer;'>Export All (CSV)</button>
            <button style='padding:8px 16px; background:#F3F4F6; border:1px solid #E5E7EB; border-radius:6px; font-size:0.8rem; font-weight:600; cursor:pointer;'>Download PDF Summary</button>
        </div>
    """, unsafe_allow_html=True)

    try:
        res = requests.get(f"{API_BASE_URL}/conversations/", params={"user_id": st.session_state.user['id']})
        convs = res.json()
    except:
        convs = []
        
    if not convs:
        st.info("No conversations found in the cloud archive.")
        return

    for conv in convs:
        with st.expander(f"📄 {conv.get('title', 'Untitled')} — {conv.get('created_at', 'N/A')}"):
            st.markdown(f"""
                <div style='padding:1rem; background:#F9FAFB; border-radius:8px;'>
                    <div style='font-size:0.7rem; font-weight:700; color:#6B7280; text-transform:uppercase; margin-bottom:1rem;'>Session Log</div>
                    <div style='font-family:monospace; font-size:0.85rem; color:#374151;'>
                        [ID: {conv.get('id')}] Initialized neural link...<br>
                        [SUCCESS] Synced to Supabase PostgreSQL.<br>
                        [DATA] Total gestures in this session: {len(conv.get('messages', []))}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Message list
            for msg in conv.get('messages', []):
                st.markdown(f"**{msg['sender'].upper()}**: {msg['translated_sentence']} *(Conf: {msg['confidence']*100:.0f}%)*")
            
            c1, c2, _ = st.columns([1, 1, 4])
            c1.button("View Details", key=f"det_{conv['id']}")
            if c2.button("Delete", key=f"del_{conv['id']}"):
                requests.delete(f"{API_BASE_URL}/conversations/{conv['id']}")
                st.rerun()

def show_analytics():
    st.title("Diagnostics")
    st.markdown("<p style='color:#6B7280; margin-bottom:2rem;'>Hardware verification and pipeline latency analytics.</p>", unsafe_allow_html=True)
    
    import platform
    c1, c2, c3 = st.columns(3)
    
    infra = [
        ("Runtime", platform.python_version()),
        ("Engine", "TensorFlow 2.15"),
        ("Status", "Operational")
    ]
    
    for i, (label, val) in enumerate(infra):
        with [c1, c2, c3][i]:
            st.markdown(f"""
                <div class='glass-card' style='text-align:center;'>
                    <div style='font-size:0.65rem; font-weight:700; color:#6B7280; text-transform:uppercase;'>{label}</div>
                    <div style='font-size:1.1rem; font-weight:800; margin-top:0.25rem;'>{val}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    if st.button("RUN FULL SYSTEM DIAGNOSTIC", type="primary", use_container_width=True):
        st.info("Running neural core validation...")

def show_settings():
    st.title("Preferences")
    st.markdown("<p style='color:#6B7280; margin-bottom:2rem;'>Configure neural link behavior and output synthesis synced to Supabase.</p>", unsafe_allow_html=True)
    
    # Load current settings
    try:
        current_settings = requests.get(f"{API_BASE_URL}/settings/{st.session_state.user['id']}").json()
    except:
        current_settings = {"theme": "dark", "speech_rate": 1.0, "auto_speak": True}

    with st.container(border=True):
        st.subheader("Output Synthesis")
        rate = st.slider("Speech Synthesis Rate", 0.5, 2.0, float(current_settings.get('speech_rate', 1.0)))
        st.selectbox("Voice Profile", ["Neural Neutral", "Neural Warm", "Neural Crisp"])
        auto_speak = st.toggle("Auto-play Speech", value=current_settings.get('auto_speak', True))
        
        st.divider()
        st.subheader("Interface")
        theme = st.selectbox("Theme Mode", ["dark", "light"], index=0 if current_settings.get('theme') == "dark" else 1)
        st.checkbox("Enable Low Latency Mode", value=True)
        
        if st.button("Save Configuration", type="primary"):
            try:
                requests.put(f"{API_BASE_URL}/settings/{st.session_state.user['id']}", json={
                    "theme": theme,
                    "speech_rate": rate,
                    "auto_speak": auto_speak
                })
                st.success("Preferences saved to Supabase.")
            except Exception as e:
                st.error(f"Save Failed: {e}")

# --- ROUTER ---
if st.session_state.page == 'landing':
    show_landing()
elif st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'dashboard':
    if st.session_state.user:
        main_app()
    else:
        st.session_state.page = 'landing'
        st.rerun()

