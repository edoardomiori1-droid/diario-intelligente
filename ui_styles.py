import streamlit as st

THEMES = {
    "Cyber Matrix": {"main": "#00FF41", "sec": "#008F11", "bg": "#0D0D0D", "card": "#161616", "txt": "#E0E0E0"},
    "Synthetic Sunset": {"main": "#FF8C00", "sec": "#FF0080", "bg": "#0D0B10", "card": "#1A1621", "txt": "#F5F5F5"},
    "Deep Space": {"main": "#00FFFF", "sec": "#007FFF", "bg": "#050A10", "card": "#0F1720", "txt": "#E0F7FA"},
    "Crimson Fury": {"main": "#FF0000", "sec": "#8B0000", "bg": "#0F0F0F", "card": "#1C1C1C", "txt": "#FFFFFF"}
}

def apply_synapse_ui(theme_name):
    t = THEMES.get(theme_name, THEMES["Cyber Matrix"])
    
    # Usiamo ID univoci per il CSS per evitare sovrapposizioni al click
    style = f"""
    <style>
    :root {{
        --main: {t['main']};
        --sec: {t['sec']};
        --bg: {t['bg']};
        --card: {t['card']};
        --txt: {t['txt']};
    }}
    
    .stApp {{ background-color: var(--bg); color: var(--txt); }}
    
    /* Titolo Premium */
    .os-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.2rem; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, var(--main), var(--sec));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 8px rgba(0,255,170,0.3));
        margin-bottom: 30px;
    }}

    .glass-card {{
        background: var(--card);
        border: 1px solid var(--main);
        border-radius: 20px; padding: 35px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }}

    /* Bottoni e Input Fixed */
    .stButton>button {{
        background: linear-gradient(135deg, var(--main), var(--sec)) !important;
        color: var(--bg) !important; border: none !important;
        font-weight: bold !important; border-radius: 12px !important;
        height: 55px; width: 100% !important; transition: 0.3s;
    }}
    
    .stTextInput>div>div>input {{
        background-color: #000 !important; border: 1px solid #333 !important;
        color: white !important; border-radius: 10px !important;
    }}

    /* Messaggi Diario */
    .user-msg {{ border-right: 4px solid var(--main); padding: 15px; margin: 10px 0 10px 50px; background: var(--card); border-radius: 10px 0 0 10px; }}
    .ai-msg {{ border-left: 4px solid var(--sec); padding: 15px; margin: 10px 50px 10px 0; background: var(--card); border-radius: 0 10px 10px 0; }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)
