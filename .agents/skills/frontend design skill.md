# Frontend Design Skill — ASL Recognition Project

## Purpose
This skill covers UI/UX design decisions, layout patterns, color systems, typography, and visual design for the ASL Streamlit application.

## When to Apply
- Designing the two-panel Live Recognition layout
- Choosing colors, fonts, and spacing
- Writing custom CSS injected via `st.markdown`
- Making accessibility decisions for deaf/hard-of-hearing users

---

## Design Principles for This Project

### Primary Users
1. **Deaf/mute person** — signing into webcam, needs clear feedback on what's being detected
2. **Hearing person** — reading the translated sentence, needs large clear text

Every design decision should serve both users simultaneously.

### Core Design Values
- **Clarity over decoration** — information must be instantly readable
- **High contrast** — critical for accessibility
- **Large text** — hearing person panel minimum 28px
- **Real-time feedback** — detection status always visible
- **Calm colors** — avoid anxiety-inducing red/orange for primary UI

---

## Color System

```python
COLORS = {
    # Primary brand
    'primary':     '#2563EB',   # Blue — trust, technology
    'primary_light': '#DBEAFE',

    # Semantic
    'success':     '#16A34A',   # Green — hand detected, word confirmed
    'warning':     '#D97706',   # Amber — low confidence
    'danger':      '#DC2626',   # Red — no hand detected
    'neutral':     '#6B7280',   # Gray — inactive states

    # Backgrounds
    'bg_deaf':     '#F0F9FF',   # Light blue tint — left panel
    'bg_hearing':  '#F0FDF4',   # Light green tint — right panel
    'bg_dark':     '#0F172A',   # Dark mode background

    # Text
    'text_primary':  '#111827',
    'text_secondary': '#6B7280',
    'text_hearing':  '#1E3A5F',  # Dark blue — hearing panel sentence
}
```

---

## Custom CSS Injection

Inject once in `app.py` to apply globally:

```python
def inject_global_css():
    st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit default menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Large sentence display */
    .hearing-sentence {
        font-size: 32px;
        font-weight: 700;
        color: #1E3A5F;
        padding: 24px;
        background: #F0FDF4;
        border-radius: 16px;
        border-left: 6px solid #16A34A;
        line-height: 1.4;
        min-height: 100px;
    }

    /* Detected word display */
    .detected-word {
        font-size: 48px;
        font-weight: 800;
        color: #2563EB;
        text-align: center;
        padding: 16px;
        letter-spacing: 2px;
    }

    /* Word chip */
    .word-chip {
        display: inline-block;
        background: #DBEAFE;
        color: #1E40AF;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 4px;
        font-weight: 600;
        font-size: 14px;
    }

    /* Panel headers */
    .panel-header {
        font-size: 20px;
        font-weight: 700;
        color: #374151;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }

    /* Status indicator */
    .status-active {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #16A34A;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
    }

    .status-inactive {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #DC2626;
        border-radius: 50%;
        margin-right: 8px;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* Chat messages */
    .chat-entry {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
    }

    /* Confidence bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #2563EB, #16A34A);
        border-radius: 4px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }

    /* Panel divider */
    .panel-divider {
        width: 2px;
        background: #E5E7EB;
        margin: 0 16px;
    }
    </style>
    """, unsafe_allow_html=True)
```

---

## Typography Scale

| Use | Size | Weight | Where |
|-----|------|--------|-------|
| Hearing sentence | 32px | 700 | Right panel main text |
| Detected word | 48px | 800 | Left panel prediction |
| Section headers | 20px | 700 | Panel titles |
| Body text | 16px | 400 | Instructions, labels |
| Captions | 12px | 400 | Timestamps, confidence % |
| Word chips | 14px | 600 | Current sentence words |

---

## Layout Templates

### Two-Panel Layout (Live Recognition)
```python
# 50/50 split with gap
left, right = st.columns([1, 1], gap="large")

# Left — Deaf person (blue tint)
with left:
    st.markdown('<div class="panel-header">🧏 Sign Here</div>',
                unsafe_allow_html=True)
    # webcam component here
    # detected word display
    # word chips
    # control buttons

# Right — Hearing person (green tint)
with right:
    st.markdown('<div class="panel-header">👁️ Reading Panel</div>',
                unsafe_allow_html=True)
    # large sentence display
    # TTS controls
    # conversation history
```

### Reference Grid (4 columns)
```python
cols = st.columns(4)
for i, word in enumerate(words):
    with cols[i % 4]:
        st.image(f"assets/signs/{word}.jpg",
                 caption=word.upper(),
                 use_column_width=True)
```

---

## Accessibility Requirements

| Requirement | Implementation |
|-------------|---------------|
| High contrast text | Minimum 4.5:1 ratio |
| Large touch targets | Buttons minimum 44px tall |
| Color not only indicator | Always pair color with icon/text |
| Keyboard navigable | Streamlit handles this natively |
| Font size control | Slider in sidebar |
| Dark mode | Toggle in sidebar with CSS swap |

### Dark Mode CSS Swap
```python
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F1F5F9; }
    .hearing-sentence { background: #1E293B; color: #E2E8F0; }
    </style>
    """, unsafe_allow_html=True)
```

---

## Do Not
- Use red/orange as the primary color — feels alarming
- Make the hearing panel text smaller than 28px
- Use more than 3 columns on mobile
- Add animations to the sentence display — it distracts from reading
- Use placeholder images in the final demo — get real ASL reference images
