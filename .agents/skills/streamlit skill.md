# Streamlit Skill — ASL Recognition Project

## Purpose
This skill covers all Streamlit patterns, components, and best practices for building the ASL recognition web app with multi-page layout, real-time webcam, session state management, and text-to-speech.

## When to Apply
- Writing any file in `pages/` or `app.py`
- Managing session state across pages
- Integrating webcam feed via streamlit-webrtc
- Implementing TTS via JavaScript injection

---

## Project Structure

```
app.py                          ← Home page (entry point)
pages/
├── 01_Live_Recognition.py      ← Main signing page
├── 02_Conversation_History.py  ← Full conversation log
└── 03_Reference_Guide.py       ← ASL sign reference
```

Run with: `streamlit run app.py`

---

## Session State — Shared Across All Pages

Initialize once in `app.py`. All pages read from the same state.

```python
# app.py — initialize all shared state here
import streamlit as st

def init_session_state():
    defaults = {
        'conversation': [],        # list of {text, timestamp, confidence}
        'current_words': [],       # words in current sentence
        'current_sentence': '',    # finalized sentence
        'model_loaded': False,     # model status
        'auto_speak': True,        # TTS toggle
        'tts_voice': 'default',
        'tts_speed': 1.0,
        'dark_mode': False,
        'font_size': 'medium'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()
```

---

## Page 1 — app.py (Home)

```python
import streamlit as st

st.set_page_config(
    page_title="ASL Recognition System",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤟 ASL Sign Language Recognition System")
st.markdown("*Bridging communication between deaf-mute and hearing people*")

# System status
col1, col2, col3 = st.columns(3)
with col1:
    status = "✅ Loaded" if st.session_state.model_loaded else "❌ Not Loaded"
    st.metric("AI Model", status)
with col2:
    st.metric("Supported Signs", "50 Words")
with col3:
    st.metric("Languages", "English")
```

---

## Page 2 — Live Recognition (Most Important)

### Two-Column Layout
```python
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from core.video_processor import ASLVideoProcessor

st.set_page_config(layout="wide")
st.title("Live Sign Recognition")

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("🧏 Signing Panel")
    # Webcam
    ctx = webrtc_streamer(
        key="asl-recognition",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=ASLVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_transform=True
    )

    # Current detection display
    if st.session_state.get('current_word'):
        word = st.session_state.current_word
        conf = st.session_state.current_confidence
        st.markdown(f"### Detected: **{word.upper()}**")
        st.progress(conf)

    # Words collected
    if st.session_state.current_words:
        st.markdown("**Current sentence:**")
        chips = " → ".join(st.session_state.current_words)
        st.info(chips)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("⌫ Backspace"):
            if st.session_state.current_words:
                st.session_state.current_words.pop()
    with col_b:
        if st.button("🗑️ Clear"):
            st.session_state.current_words = []
            st.session_state.current_sentence = ''

with right_col:
    st.subheader("👁️ Reading Panel")

    # Large sentence display
    sentence = st.session_state.current_sentence
    if sentence:
        st.markdown(
            f"<p style='font-size:32px; font-weight:bold; "
            f"color:#1a1a1a; padding:20px; background:#f0f8ff; "
            f"border-radius:12px;'>{sentence}</p>",
            unsafe_allow_html=True
        )

    # TTS controls
    st.session_state.auto_speak = st.toggle(
        "🔊 Auto-speak when sentence completes",
        value=st.session_state.auto_speak
    )
    if st.button("▶️ Speak Now"):
        tts_component(sentence)

    # Conversation history
    st.divider()
    st.subheader("💬 Conversation History")
    for entry in reversed(st.session_state.conversation[-20:]):
        with st.chat_message("user", avatar="🧏"):
            st.write(entry['text'])
            st.caption(entry['timestamp'])
```

---

## Text-to-Speech via JavaScript Injection

```python
import streamlit.components.v1 as components

def tts_component(text: str, speed: float = 1.0, pitch: float = 1.0):
    """Speak text using browser Web Speech API."""
    if not text:
        return
    # Escape single quotes in text
    safe_text = text.replace("'", "\\'")
    js_code = f"""
    <script>
    (function() {{
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance('{safe_text}');
        utterance.rate = {speed};
        utterance.pitch = {pitch};
        utterance.lang = 'en-US';
        window.speechSynthesis.speak(utterance);
    }})();
    </script>
    """
    components.html(js_code, height=0)
```

---

## Page 3 — Conversation History

```python
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("💬 Conversation History")

conversation = st.session_state.conversation

if not conversation:
    st.info("No conversation yet. Go to Live Recognition to start signing.")
else:
    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sentences", len(conversation))
    col2.metric("Total Words",
                sum(len(e['text'].split()) for e in conversation))
    avg_conf = sum(e.get('confidence', 0) for e in conversation) / len(conversation)
    col3.metric("Avg Confidence", f"{avg_conf*100:.1f}%")

    st.divider()

    # Search
    search = st.text_input("🔍 Search conversation")
    filtered = [e for e in conversation
                if search.lower() in e['text'].lower()] if search else conversation

    # Display
    for entry in reversed(filtered):
        with st.chat_message("user", avatar="🧏"):
            st.write(entry['text'])
            st.caption(f"🕐 {entry['timestamp']}")

    # Export
    df = pd.DataFrame(conversation)
    csv = df.to_csv(index=False)
    st.download_button("📥 Download as CSV", csv,
                       "conversation.csv", "text/csv")
```

---

## Page 4 — Reference Guide

```python
import streamlit as st
from PIL import Image
import os

st.title("📚 ASL Signs Reference Guide")

CATEGORIES = {
    "Greetings": ["hello", "goodbye", "please", "thank you", "sorry", "yes", "no", "fine"],
    "People": ["I", "you", "we", "mother", "father", "friend", "doctor", "name"],
    "Actions": ["want", "need", "help", "eat", "drink", "go", "come", "stop"],
    "Places": ["home", "school", "work", "hospital", "bathroom"],
    "Emotions": ["happy", "sad", "good", "bad", "pain", "sick", "love"]
}

search = st.text_input("🔍 Search a sign")
tab_names = list(CATEGORIES.keys())
tabs = st.tabs(tab_names)

for tab, (category, words) in zip(tabs, CATEGORIES.items()):
    with tab:
        filtered_words = [w for w in words
                          if search.lower() in w.lower()] if search else words
        cols = st.columns(4)
        for i, word in enumerate(filtered_words):
            with cols[i % 4]:
                img_path = f"assets/signs/{word}.jpg"
                if os.path.exists(img_path):
                    st.image(img_path, caption=word.upper(), use_column_width=True)
                else:
                    st.markdown(f"**{word.upper()}**")
                    st.caption("Image coming soon")
```

---

## Sidebar (shared across all pages)

Add to `app.py` and it appears on every page:

```python
with st.sidebar:
    st.image("assets/logo.png", width=120)
    st.title("ASL System")
    st.divider()
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode")
    font_options = {"Small": "14px", "Medium": "18px", "Large": "24px"}
    st.session_state.font_size = st.select_slider(
        "Font Size", options=list(font_options.keys()), value="Medium"
    )
    st.divider()
    st.caption("FYP Project — ASL Recognition")
    st.caption("Department of Computer Science")
```

---

## Common Streamlit Issues and Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Session state resets | Missing initialization | Init all keys in `app.py` before page load |
| Webcam not starting | Browser permissions | Use HTTPS or localhost only |
| TTS not speaking | JS runs before DOM ready | Wrap in `setTimeout(fn, 100)` |
| Page reruns on every widget | Normal Streamlit behavior | Use `st.session_state` to avoid reset |
| WebRTC black screen | Wrong video format | Use `format="bgr24"` in av frame |
| Slow rerun on large history | Rendering too many items | Slice to last 20: `conversation[-20:]` |

---

## Do Not
- Call `st.set_page_config()` in any file other than the top of each page file
- Store large numpy arrays in session state — store predictions only
- Use `time.sleep()` in Streamlit — it blocks the entire UI
- Render all conversation history — paginate or limit to last 20
