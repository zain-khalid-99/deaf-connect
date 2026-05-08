import streamlit as st

def speak_text(text: str):
    """
    Client-side Text-to-Speech using Web Speech API.
    Works in Streamlit Cloud by injecting JavaScript.
    """
    if not text:
        return
        
    js_code = f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text.replace("'", "\\'")}');
        window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(js_code, height=0)
