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
    
    # Usiamo un template statico e sostituiamo i valori a mano
    # Questo evita il TypeError su Python 3.14
    style_template = """
    <style>
    .stApp { background-color: __BG__; color: __TXT__; }
    
    .os-title {
        font-family: 'monospace';
        font-size: 3rem; font-weight: bold; text-align: center;
        color: __MAIN__; margin-bottom: 30px;
    }

    .glass-card {
        background: __CARD__;
        border: 1px solid __MAIN__;
        border-radius: 20px; padding: 30px;
    }

    .stButton>button {
        background: linear-gradient(to right, __MAIN__, __SEC__) !important;
        color: __BG__ !important; border: none !important;
        font-weight: bold !important; border-radius: 12px !important;
        height: 55px; width: 100% !important;
    }
    
    .user-msg { border-right: 4px solid __MAIN__; padding: 10px; margin: 10px; text-align: right; background: __CARD__; }
    .ai-msg { border-left: 4px solid __SEC__; padding: 10px; margin: 10px; background: __CARD__; }
    </style>
    """
    
    style = style_template.replace("__BG__", t['bg'])\
                          .replace("__TXT__", t['txt'])\
                          .replace("__MAIN__", t['main'])\
                          .replace("__SEC__", t['sec'])\
                          .replace("__CARD__", t['card'])
                          
    st.markdown(style, unsafe_allow_html=True)
