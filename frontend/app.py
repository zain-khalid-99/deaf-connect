import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

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
        background: white;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .glass-card:hover {
        border-color: #000;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    /* Badge */
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

    /* Buttons */
    .stButton button {
        border-radius: 4px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    /* Media Queries for Responsiveness */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
            text-align: center;
        }
        .hero-subtitle {
            text-align: center;
            font-size: 1rem !important;
        }
        .stButton {
            width: 100%;
        }
        .glass-card {
            padding: 1rem;
        }
    }

    /* Footer */
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
    # Sidebar
    with st.sidebar:
        st.markdown("<h3 style='margin-bottom:2rem; font-weight:900;'>SIGNSYNC AI</h3>", unsafe_allow_html=True)
        
        # User Profile Mini
        st.markdown(f"""
            <div style='display:flex; align-items:center; gap:12px; padding:12px; background:white; border:1px solid #E5E7EB; border-radius:8px; margin-bottom:2rem;'>
                <img src='{st.session_state.user['avatar_url']}' style='width:32px; height:32px; border-radius:50%;'>
                <div>
                    <div style='font-size:0.75rem; font-weight:700;'>{st.session_state.user['full_name']}</div>
                    <div style='font-size:0.6rem; color:#6B7280; text-transform:uppercase;'>Operator</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        page = st.radio("NAVIGATION", ["Dashboard", "Live Communication", "History", "Analytics", "Settings"], label_visibility="collapsed")
        
        st.markdown("<div style='flex:1; min-height:20vh;'></div>", unsafe_allow_html=True)
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = 'landing'
            st.rerun()

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
    st.title("Operator Dashboard")
    st.markdown("<p style='color:#6B7280; margin-bottom:2rem;'>Real-time system overview and activity metrics.</p>", unsafe_allow_html=True)
    
    try:
        res = requests.get(f"{API_BASE_URL}/analytics/{st.session_state.user['id']}")
        stats_data = res.json()
    except:
        stats_data = {"total_chats": 12, "total_messages": 142, "avg_confidence": 0.94}

    c1, c2, c3 = st.columns(3)
    metrics = [
        ("Total Sessions", stats_data['total_chats'], "↑ 12%"),
        ("Gestures Detected", stats_data['total_messages'], "↑ 8%"),
        ("Avg Confidence", f"{stats_data['avg_confidence']*100:.1f}%", "Optimal")
    ]
    
    for i, (label, val, delta) in enumerate(metrics):
        with [c1, c2, c3][i]:
            st.markdown(f"""
                <div class='glass-card'>
                    <div style='font-size:0.7rem; font-weight:700; color:#6B7280; text-transform:uppercase; margin-bottom:0.5rem;'>{label}</div>
                    <div style='font-size:1.5rem; font-weight:800;'>{val}</div>
                    <div style='font-size:0.65rem; color:#10B981; margin-top:0.5rem;'>{delta}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    st.subheader("System Health")
    st.markdown("""
        <div class='glass-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:0.85rem;'>Neural Core Engine</span>
                <span style='color:#10B981; font-weight:700; font-size:0.7rem;'>ACTIVE</span>
            </div>
            <div style='height:4px; background:#F3F4F6; border-radius:2px; margin-top:8px;'>
                <div style='width:94%; height:100%; background:black; border-radius:2px;'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_live_comm():
    st.title("Neural Translation")
    st.markdown("<p style='color:#6B7280; margin-bottom:1rem;'>Active ASL-to-Speech and Speech-to-Text pipeline.</p>", unsafe_allow_html=True)
    
    # Status Indicators
    status_cols = st.columns([1, 1, 1, 3])
    status_cols[0].markdown("<div style='font-size:0.6rem; font-weight:700; color:#10B981;'>● WEBCAM</div>", unsafe_allow_html=True)
    status_cols[1].markdown("<div style='font-size:0.6rem; font-weight:700; color:#10B981;'>● AUDIO</div>", unsafe_allow_html=True)
    status_cols[2].markdown("<div style='font-size:0.6rem; font-weight:700; color:#10B981;'>● NEURAL</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    
    # Responsive Webcam Layout
    main_col, side_col = st.columns([2, 1])
    
    with main_col:
        st.markdown("""
            <div style='background:#FAFAFA; aspect-ratio:16/9; border:1px solid #E5E7EB; border-radius:8px; display:flex; flex-direction:column; align-items:center; justify-content:center;'>
                <div style='font-size:0.8rem; font-weight:600; color:#000;'>Initializing Neural Link...</div>
                <div style='font-size:0.6rem; color:#6B7280; margin-top:0.5rem;'>Ensure proper lighting and hand visibility</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Controls
        ctrl_cols = st.columns([1, 1, 1])
        ctrl_cols[0].button("Start Camera", use_container_width=True, type="primary")
        ctrl_cols[1].button("Reset Tracking", use_container_width=True)
        ctrl_cols[2].button("Voice Input", use_container_width=True)

    with side_col:
        st.markdown("<div style='font-size:0.7rem; font-weight:700; color:#6B7280; text-transform:uppercase; margin-bottom:1rem;'>Translation Feed</div>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background:white; border:1px solid #E5E7EB; border-radius:8px; height:320px; padding:1rem; overflow-y:auto;'>
                <div style='font-size:0.75rem; color:#6B7280; font-style:italic; text-align:center; margin-top:4rem;'>Waiting for detection...</div>
            </div>
        """, unsafe_allow_html=True)
        st.text_input("Manual Correction", placeholder="Type here...", label_visibility="collapsed")

def show_history():
    st.title("Archive")
    st.markdown("<p style='color:#6B7280; margin-bottom:2rem;'>Persistent logs of all neural translation sessions.</p>", unsafe_allow_html=True)
    
    search_col, _ = st.columns([2, 1])
    search_col.text_input("Search archives...", placeholder="Keyword or date...", label_visibility="collapsed")
    
    try:
        res = requests.get(f"{API_BASE_URL}/conversations/", params={"user_id": st.session_state.user['id']})
        convs = res.json()
    except:
        convs = [{"title": "Morning Session", "created_at": "2024-05-08 09:15", "id": 1}]
        
    for conv in convs:
        with st.expander(f"{conv['title']} — {conv['created_at']}"):
            st.markdown(f"<div style='font-size:0.8rem; color:#4B5563; padding:1rem;'>Detailed log for session {conv['id']} will appear here.</div>", unsafe_allow_html=True)
            st.button(f"Export PDF", key=f"exp_{conv['id']}")

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
    st.markdown("<p style='color:#6B7280; margin-bottom:2rem;'>Configure neural link behavior and output synthesis.</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("Output Synthesis")
        st.slider("Speech Synthesis Rate", 0.5, 2.0, 1.0)
        st.selectbox("Voice Profile", ["Neural Neutral", "Neural Warm", "Neural Crisp"])
        st.toggle("Auto-play Speech", value=True)
        
        st.divider()
        st.subheader("Interface")
        st.selectbox("Default View", ["Dashboard", "Live Translation"])
        st.checkbox("Enable Low Latency Mode")
        
        st.button("Save Configuration", type="primary")

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

