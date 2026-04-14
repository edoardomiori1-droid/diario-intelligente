import streamlit as st

# Dizionario dei Temi: Qui puoi aggiungere infiniti stili
THEMES = {
    "Cyber Matrix": {
        "main": "#00FF41", "sec": "#008F11", "bg": "#0D0D0D", 
        "card": "#161616", "txt": "#E0E0E0", "accent": "#00FF41"
    },
    "Synthetic Sunset": {
        "main": "#FF8C00", "sec": "#FF0080", "bg": "#0D0B10", 
        "card": "#1A1621", "txt": "#F5F5F5", "accent": "#FF8C00"
    },
    "Deep Space": {
        "main": "#00FFFF", "sec": "#007FFF", "bg": "#050A10", 
        "card": "#0F1720", "txt": "#E0F7FA", "accent": "#00FFFF"
    },
    "Crimson Fury": {
        "main": "#FF0000", "sec": "#8B0000", "bg": "#0F0F0F", 
        "card": "#1C1C1C", "txt": "#FFFFFF", "accent": "#FF0000"
    }
}

def apply_synapse_ui(theme_name):
    """
    Inietta il CSS nell'applicazione in modo sicuro.
    Usa il metodo .replace() per evitare bug di Python 3.14 con le parentesi graffe.
    """
    t = THEMES.get(theme_name, THEMES["Cyber Matrix"])
    
    style_template = """
    <style>
    /* 1. RESET E FONT */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp {
        background-color: [BG];
        color: [TXT];
        font-family: 'JetBrains Mono', monospace;
    }

    /* 2. TITOLO NEON ANIMATO */
    .os-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, [MAIN], [SEC]);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 10px [MAIN]44);
    }

    /* 3. CONTENITORI (GLASS CARDS) */
    .glass-card {
        background: [CARD];
        border: 1px solid [MAIN]66;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.7);
        margin-bottom: 25px;
    }

    /* 4. BOTTONI PREMIUM */
    .stButton>button {
        background: linear-gradient(135deg, [MAIN] 0%, [SEC] 100%) !important;
        color: [BG] !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
        padding: 15px 25px !important;
        width: 100% !important;
        height: 60px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px [MAIN]44 !important;
        filter: brightness(1.1);
    }

    /* 5. INPUT E CHAT */
    .stTextInput>div>div>input {
        background-color: #000 !important;
        color: white !important;
        border: 1px solid [MAIN]44 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    
    .user-msg {
        background: [CARD];
        border-right: 5px solid [MAIN];
        padding: 20px;
        margin: 10px 0 10px 60px;
        border-radius: 15px 0 0 15px;
        box-shadow: -5px 5px 15px rgba(0,0,0,0.3);
    }
    
    .ai-msg {
        background: [CARD];
        border-left: 5px solid [SEC];
        padding: 20px;
        margin: 10px 60px 10px 0;
        border-radius: 0 15px 15px 0;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    }

    /* Nascondi elementi Streamlit standard */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """
    
    # Sostituzione manuale per evitare errori di string-formatting
    style = style_template.replace("[MAIN]", t['main']) \
                          .replace("[SEC]", t['sec']) \
                          .replace("[BG]", t['bg']) \
                          .replace("[CARD]", t['card']) \
                          .replace("[TXT]", t['txt'])
                          
    st.markdown(style, unsafe_allow_html=True)
