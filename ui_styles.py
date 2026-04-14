"""
SYNAPSE NEURAL OS - CORE INTERFACE ENGINE v3.5
File: ui_styles.py
Status: EXECUTIVE / STABLE
Description: Gestione avanzata del design system e dell'iniezione CSS.
"""

import streamlit as st

# ==============================================================================
# 1. ARCHITETTURA TEMI (ENTERPRISE GRADE)
# ==============================================================================
# Ogni tema è un'istanza cromatica isolata per evitare il "color-bleeding" tra pagine.
# Ho rimosso ogni elemento infantile per un look da ufficio di intelligence.

THEMES = {
    "SYNAPSE_PRIME": {
        "id": "PRIME",
        "name": "Synapse Prime (Matrix)",
        "main": "#00FF41",  # Neon Green
        "sec": "#008F11",   # Dark Green
        "bg": "#0A0A0A",    # Pure Black
        "card": "#121212",  # Jet Black
        "txt": "#E0E0E0",   # Platinum
        "border": "#00FF4133",
        "gradient": "linear-gradient(135deg, #00FF41 0%, #008F11 100%)"
    },
    "DEEP_SPACE": {
        "id": "SPACE",
        "name": "Deep Space (Tactical)",
        "main": "#00FFFF",  # Cyan
        "sec": "#0044FF",   # Electric Blue
        "bg": "#05080A",    # Space Black
        "card": "#0D1117",  # Navy Grey
        "txt": "#F0F8FF",   # Alice Blue
        "border": "#00FFFF33",
        "gradient": "linear-gradient(135deg, #00FFFF 0%, #0044FF 100%)"
    },
    "CRIMSON_PROTOCOL": {
        "id": "CRIMSON",
        "name": "Crimson Protocol",
        "main": "#FF0000",  # Pure Red
        "sec": "#800000",   # Maroon
        "bg": "#080808",    # Dark
        "card": "#181818",  # Carbon
        "txt": "#FFFFFF",   # White
        "border": "#FF000033",
        "gradient": "linear-gradient(135deg, #FF0000 0%, #800000 100%)"
    },
    "OBSIDIAN_GOLD": {
        "id": "GOLD",
        "name": "Obsidian Gold (Elite)",
        "main": "#D4AF37",  # Gold
        "sec": "#996515",   # Golden Brown
        "bg": "#050505",    # Rich Black
        "card": "#111111",  # Dark Obsidian
        "txt": "#FFFAF0",   # Ivory
        "border": "#D4AF3733",
        "gradient": "linear-gradient(135deg, #D4AF37 0%, #996515 100%)"
    }
}

# ==============================================================================
# 2. ENGINE DI INIEZIONE CSS (ANTI-Sfarfallio)
# ==============================================================================

def apply_synapse_ui(theme_name):
    """
    Iniezione CSS potenziata. 
    Risolve il bug 'unsafe_allow_input' e blocca i colori tramite variabili root.
    """
    
    # Selezione del tema con fallback di sicurezza
    t = THEMES.get(theme_name, THEMES["SYNAPSE_PRIME"])
    
    # Costruzione del CSS Modulare
    # Nota: Usiamo .replace per iniettare i valori ed evitare bug di formatting {}
    css_content = """
    <style>
    /* ------------------------------------------------------------------
       RESET & CORE VARIABLES
    ------------------------------------------------------------------ */
    :root {
        --syn-main: [MAIN];
        --syn-sec: [SEC];
        --syn-bg: [BG];
        --syn-card: [CARD];
        --syn-txt: [TXT];
        --syn-border: [BORDER];
        --syn-grad: [GRAD];
    }

    /* ------------------------------------------------------------------
       GLOBAL STYLES
    ------------------------------------------------------------------ */
    .stApp {
        background-color: var(--syn-bg);
        color: var(--syn-txt);
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Nascondi header Streamlit per un look OS nativo */
    header, footer, #MainMenu {visibility: hidden;}

    /* ------------------------------------------------------------------
       EXECUTIVE HEADER
    ------------------------------------------------------------------ */
    .os-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: var(--syn-grad);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -5px;
        margin-top: -60px;
        margin-bottom: 20px;
        filter: drop-shadow(0 0 15px [MAIN]33);
        animation: pulse 4s infinite ease-in-out;
    }

    @keyframes pulse {
        0% { opacity: 0.9; transform: scale(0.99); }
        50% { opacity: 1; transform: scale(1); }
        100% { opacity: 0.9; transform: scale(0.99); }
    }

    /* ------------------------------------------------------------------
       GLASS CARDS & CONTAINERS
    ------------------------------------------------------------------ */
    .glass-card {
        background: var(--syn-card);
        border: 1px solid var(--syn-border);
        border-radius: 24px;
        padding: 45px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 25px;
    }
    
    .glass-card:hover {
        border: 1px solid var(--syn-main);
        box-shadow: 0 0 30px [MAIN]11;
    }

    /* ------------------------------------------------------------------
       EXECUTIVE INPUTS (Text, TextArea, Select)
    ------------------------------------------------------------------ */
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] {
        background-color: #00000033 !important;
        border-radius: 12px !important;
        border: 1px solid var(--syn-border) !important;
        transition: 0.3s;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: var(--syn-main) !important;
        box-shadow: 0 0 10px [MAIN]22 !important;
    }

    input, textarea {
        color: var(--syn-txt) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ------------------------------------------------------------------
       PREMIUM BUTTONS
    ------------------------------------------------------------------ */
    .stButton>button {
        background: var(--syn-grad) !important;
        color: #000 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 16px !important;
        height: 65px !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.4s all ease !important;
        box-shadow: 0 4px 15px [MAIN]33 !important;
    }

    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 25px [MAIN]55 !important;
        filter: brightness(1.1);
    }
    
    .stButton>button:active {
        transform: scale(0.98) !important;
    }

    /* ------------------------------------------------------------------
       NEURAL CHAT BUBBLES
    ------------------------------------------------------------------ */
    .user-bubble {
        background: var(--syn-card);
        border-right: 6px solid var(--syn-main);
        padding: 25px;
        margin: 15px 0 15px 80px;
        border-radius: 20px 0 20px 20px;
        box-shadow: -10px 10px 25px rgba(0,0,0,0.3);
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .ai-bubble {
        background: var(--syn-card);
        border-left: 6px solid var(--syn-sec);
        padding: 25px;
        margin: 15px 80px 15px 0;
        border-radius: 0 20px 20px 20px;
        box-shadow: 10px 10px 25px rgba(0,0,0,0.3);
        font-size: 1.05rem;
        line-height: 1.6;
        color: #f1f1f1;
    }

    /* ------------------------------------------------------------------
       CUSTOM SCROLLBAR
    ------------------------------------------------------------------ */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--syn-bg); }
    ::-webkit-scrollbar-thumb { 
        background: var(--syn-border); 
        border-radius: 10px; 
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--syn-main); }
    
    </style>
    """
    
    # Esecuzione rimpiazzi (FIX per stabilità Python 3.14)
    final_css = css_content.replace("[MAIN]", t['main']) \
                           .replace("[SEC]", t['sec']) \
                           .replace("[BG]", t['bg']) \
                           .replace("[CARD]", t['card']) \
                           .replace("[TXT]", t['txt']) \
                           .replace("[BORDER]", t['border']) \
                           .replace("[GRAD]", t['gradient'])
    
    # FIX ERRORE: Cambio unsafe_allow_input in unsafe_allow_html
    st.markdown(final_css, unsafe_allow_html=True)

# ==============================================================================
# 3. EXTRA UTILS: DASHBOARD WIDGETS
# ==============================================================================

def draw_section_title(title, subtitle=""):
    """Disegna un titolo di sezione in stile OS."""
    st.markdown(f"""
        <div style="margin-bottom: 30px; border-left: 4px solid var(--syn-main); padding-left: 20px;">
            <h2 style="margin:0; color:var(--syn-main); text-transform:uppercase; letter-spacing:2px; font-size:1.5rem;">{title}</h2>
            <p style="margin:0; opacity:0.6; font-size:0.9rem;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)
