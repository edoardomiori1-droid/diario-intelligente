import streamlit as st

THEMES = {
    "Cyber Matrix": {"main": "#00FF41", "sec": "#008F11", "bg": "#0D0D0D", "card": "#1A1A1A", "txt": "#E0E0E0"},
    "Synthetic Sunset": {"main": "#FF8C00", "sec": "#FF0080", "bg": "#120D16", "card": "#1D1625", "txt": "#F5F5F5"},
    "Deep Space": {"main": "#00FFFF", "sec": "#007FFF", "bg": "#050A10", "card": "#0F1720", "txt": "#E0F7FA"},
    "Crimson Fury": {"main": "#FF0000", "sec": "#8B0000", "bg": "#0F0F0F", "card": "#1C1C1C", "txt": "#FFFFFF"},
    "Arctic Frost": {"main": "#74EBD5", "sec": "#9FACE6", "bg": "#F0F4F8", "card": "#FFFFFF", "txt": "#2C3E50"},
    "Royal Amethyst": {"main": "#FF00FF", "sec": "#7000FF", "bg": "#0A0510", "card": "#160D25", "txt": "#FDF0FF"},
    "Midnight Gold": {"main": "#D4AF37", "sec": "#996515", "bg": "#0A0A0A", "card": "#141414", "txt": "#F4F4F4"},
    "Tokyo Drift": {"main": "#FF69B4", "sec": "#00FFFF", "bg": "#0F0510", "card": "#1A0D1D", "txt": "#FFFFFF"}
}

def apply_synapse_ui(theme_name):
    t = THEMES.get(theme_name, THEMES["Cyber Matrix"])
    
    style = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap');
    
    .stApp {{ background-color: {t['bg']}; color: {t['txt']}; }}
    
    .os-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 3rem; font-weight: bold; text-align: center;
        background: linear-gradient(to right, {t['main']}, {t['sec']});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }}

    .glass-card {{
        background: {t['card']};
        border: 1px solid {t['main']}55;
        border-radius: 20px; padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    .stButton>button {{
        background: linear-gradient(to right, {t['main']}, {t['sec']}) !important;
        color: {t['bg']} !important; border: none !important;
        font-weight: bold !important; border-radius: 12px !important;
        height: 55px; width: 100%; transition: 0.3s;
    }}

    .stButton>button:hover {{ transform: scale(1.02); box-shadow: 0 0 15px {t['main']}; }}
    
    /* Messaggi Chat */
    .user-msg {{ border-right: 4px solid {t['main']}; padding: 10px; margin: 10px 0 10px 40px; text-align: right; background: {t['card']}; }}
    .ai-msg {{ border-left: 4px solid {t['sec']}; padding: 10px; margin: 10px 40px 10px 0; background: {t['card']}; }}
    </style>
    """
    st.markdown(style, unsafe_allow_input=True)
