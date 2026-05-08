"""
Module: tts_utils.py
Purpose: Client-side Text-to-Speech via Web Speech API injected as JavaScript.
Author: SignSync AI Team
Date: 2026-05-08
"""

import streamlit as st


def speak_text(text: str) -> None:
    """
    Client-side Text-to-Speech using Web Speech API.
    Works in Streamlit Cloud by injecting JavaScript.
    """
    if not text:
        return

    # Escape single quotes to avoid breaking the JS string literal.
    # We use str.replace() here BEFORE building the HTML string —
    # backslashes inside f-string expressions are only valid in Python 3.12+.
    safe_text: str = text.replace("'", "&#39;")

    # Build HTML using str.format() instead of an f-string so that
    # static analysers (Pyrefly, pyright) do not try to parse the
    # embedded JavaScript block as Python source code.
    js_template = (
        "<script>"
        "var msg = new SpeechSynthesisUtterance('{text}');"
        "window.speechSynthesis.speak(msg);"
        "</script>"
    )
    js_code: str = js_template.format(text=safe_text)

    st.components.v1.html(js_code, height=0)
