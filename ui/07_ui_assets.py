"""
SYNAPSE NEURAL OS - UI ASSETS & ICONS
-------------------------------------
File 07/35 | ui/07_ui_assets.py
Posizione: /ui/07_ui_assets.py

DESCRIZIONE:
Centralizzazione di icone, simboli e stringhe grafiche.
Assicura che ogni sezione dell'OS utilizzi lo stesso linguaggio visivo.
"""

import streamlit as st

def get_assets():
    """
    Ritorna un dizionario con tutte le icone e i simboli tematici.
    """
    return {
        # --- ICONE NAVIGAZIONE ---
        "nav": {
            "dashboard": "📊",
            "chat": "💬",
            "profile": "👤",
            "settings": "⚙️",
            "vault": "🔐",
            "logout": "🚪"
        },
        
        # --- SIMBOLI STATISTICHE (RADAR) ---
        "stats": {
            "logic": "🧠",
            "creative": "🎨",
            "energy": "⚡",
            "focus": "🎯",
            "social": "🌐"
        },
        
        # --- DECORAZIONI CYBERPUNK ---
        "deco": {
            "separator": "————————————————————————————————",
            "glitch_line": "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░",
            "bullet": "🚀",
            "warning": "⚠️",
            "success": "✅"
        }
    }

def get_system_banners():
    """
    Ritorna stringhe ASCII o HTML per i titoli delle sezioni.
    """
    return {
        "boot_logo": "SYSTEM STARTING...",
        "onboarding_header": "NEURAL LINK ESTABLISHMENT",
        "dashboard_welcome": "WELCOME OPERATOR"
    }

def draw_header_line():
    """Disegna una linea decorativa al neon sotto i titoli."""
    st.markdown("""
        <hr style="height:2px;border:none;color:#00F2FF;background-color:#00F2FF;
        box-shadow: 0px 0px 8px #00F2FF; margin-bottom: 25px;">
    """, unsafe_allow_html=True)

def show_loading_animation():
    """Placeholder per animazioni di caricamento."""
    with st.spinner('Sincronizzazione neurale in corso...'):
        pass
