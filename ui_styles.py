import streamlit as st

# ==============================================================================
# 1. DESIGN SYSTEM - DEFINIZIONE TEMI PROFESSIONALI (Enterprise Level)
# ==============================================================================
# Ogni tema definisce l'intera palette cromatica.
# Usiamo nomi professionali e colori ad alto contrasto per un'esperienza executive.
THEMES = {
    "Synapse Prime (Matrix)": {
        "main": "#00FF41", "sec": "#008F11", "bg": "#0D0D0D", 
        "card": "#1A1A1A", "txt": "#E0E0E0", "sidebar": "#000000"
    },
    "Synthetic Sunset": {
        "main": "#FF8C00", "sec": "#FF0080", "bg": "#120D16", 
        "card": "#1D1625", "txt": "#F5F5F5", "sidebar": "#120D16"
    },
    "Deep Space (Ocean)": {
        "main": "#00FFFF", "sec": "#007FFF", "bg": "#050A10", 
        "card": "#0F1720", "txt": "#E0F7FA", "sidebar": "#050A10"
    },
    "Crimson fury": {
        "main": "#FF0000", "sec": "#8B0000", "bg": "#0F0F0F", 
        "card": "#1C1C1C", "txt": "#FFFFFF", "sidebar": "#000000"
    }
}

# ==============================================================================
# 2. CORE INJECTION - FUNZIONE DI APPLICAZIONE STILE (v3.0)
# ==============================================================================
def apply_synapse_ui(theme_name):
    """
    Inietta il design system nell'applicazione Streamlit.
    Usa variabili CSS (:root) per blindare i colori e prevenire sfarfallii.
    Inietta animazioni globali e transizioni executive.
    """
    # Fallback di sicurezza: se il tema non esiste, usa il principale
    if theme_name not in THEMES:
        theme_name = "Synapse Prime (Matrix)"
    
    t = THEMES[theme_name]
    
    # Costruiamo il CSS in modo modulare senza f-strings complesse 
    # per evitare TypeError su Python 3.14
    css_template = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* DEFINIZIONE VARIABILI CSS (:root) - Blocca i colori preventivamente */
    :root {
        --bg-color: [BG];
        --txt-color: [TXT];
        --main-color: [MAIN];
        --sec-color: [SEC];
        --card-color: [CARD];
        --sidebar-color: [SIDEBAR];
    }
    
    /* RESET E FONT GLOBALI */
    html, body, [class*="css"] {
        background-color: var(--bg-color);
        color: var(--txt-color);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp { background: var(--bg-color); }

    /* TITOLO EXECUTIVE NEON */
    .os-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, var(--main-color), var(--sec-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -3px;
        margin-top: -50px;
        filter: drop-shadow(0 0 10px rgba(0, 255, 170, 0.4));
    }

    /* CARD DI CONTENUTO PREMIUM */
    .glass-card {
        background: var(--card-color);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }

    /* MODIFICA INPUT E TEXTAREA */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: var(--txt-color) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    /* BOTTONI PREMIUM CON TRANSIZIONE */
    .stButton>button {
        background: linear-gradient(135deg, var(--main-color) 0%, var(--sec-color) 100%) !important;
        color: var(--bg-color) !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 14px !important;
        height: 3.5rem !important;
        width: 100% !important;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(0, 255, 170, 0.4) !important;
    }

    /* CHAT E REGISTRO NEURALE */
    .chat-user {
        border-right: 4px solid var(--main-color);
        padding: 15px; margin: 10px 0 10px 100px;
        background: var(--card-color); border-radius: 12px 0 12px 12px;
    }
    .chat-ai {
        border-left: 4px solid var(--sec-color);
        padding: 15px; margin: 10px 100px 10px 0;
        background: var(--card-color); border-radius: 0 12px 12px 12px;
        color: var(--txt-color);
    }

    /* ANIMAZIONE TRANSIZIONE GLOBALE */
    #root, .stApp {
        transition: opacity 0.5s ease;
    }

    /* Nascondi elementi Streamlit standard */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """
    
    # Sostituzione manuale per evitare errori di formato
    style = css_template.replace("[MAIN]", t['main']) \
                        .replace("[SEC]", t['sec']) \
                        .replace("[BG]", t['bg']) \
                        .replace("[CARD]", t['card']) \
                        .replace("[TXT]", t['txt'])
                        
    st.markdown(style, unsafe_allow_input=True)
