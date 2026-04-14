import streamlit as st

THEMES = {
    "Cyber Matrix": {"main": "#00FF41", "sec": "#008F11", "bg": "#0D0D0D", "card": "#161616", "txt": "#E0E0E0"},
    "Synthetic Sunset": {"main": "#FF8C00", "sec": "#FF0080", "bg": "#0D0B10", "card": "#1A1621", "txt": "#F5F5F5"},
    "Deep Space": {"main": "#00FFFF", "sec": "#007FFF", "bg": "#050A10", "card": "#0F1720", "txt": "#E0F7FA"},
    "Crimson Fury": {"main": "#FF0000", "sec": "#8B0000", "bg": "#0F0F0F", "card": "#1C1C1C", "txt": "#FFFFFF"}
}

def apply_synapse_ui(theme_name):
    # Se il tema non esiste più o è corrotto, usa Cyber Matrix
    if theme_name not in THEMES:
        theme_name = "Cyber Matrix"
    
    t = THEMES[theme_name]
    
    style = f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; }}
    
    .os-title {{
        font-family: 'Courier New', monospace;
        font-size: 3rem; font-weight: bold; text-align: center;
        background: linear-gradient(to right, {t['main']}, {t['sec']});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }}

    .glass-card {{
        background: {t['card']};
        border: 1px solid {t['main']};
        border-radius: 15px; padding: 25px;
        margin-bottom: 20px;
    }}

    .stButton>button {{
        background: linear-gradient(to right, {t['main']}, {t['sec']}) !important;
        color: {t['bg']} !important; font-weight: bold !important;
        border-radius: 10px !important; border: none !important;
        height: 50px; width: 100%;
    }}

    .user-msg {{ border-right: 4px solid {t['main']}; padding: 15px; margin: 10px 0 10px 40px; background: {t['card']}; text-align: right; }}
    .ai-msg {{ border-left: 4px solid {t['sec']}; padding: 15px; margin: 10px 40px 10px 0; background: {t['card']}; }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)
