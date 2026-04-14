"""
SYNAPSE NEURAL OS - MAIN ORCHESTRATOR
-------------------------------------
File 30/35 | main.py
Posizione: / (Root)

DESCRIZIONE:
Punto di ingresso principale del sistema. Gestisce il routing,
il caricamento dei dati persistenti e l'autenticazione.
"""

import streamlit as st
from datetime import datetime

# 1. CONFIGURAZIONE PAGINA (Deve essere la prima istruzione Streamlit)
st.set_page_config(
    page_title="SYNAPSE NEURAL OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CARICAMENTO LOGICHE E CORE
try:
    from core.01_core_boot import initialize_system
    from core.04_core_auth import check_auth
    from data.18_data_manager import load_os_data
    from ui.09_ui_sidebar import render_sidebar
    # Import delle pagine per il routing
    from pages.10_page_onboarding import render_onboarding
    from pages.11_page_dashboard import render_dashboard
    from pages.12_page_chat import render_chat
    from pages.13_page_vault import render_vault
    from pages.14_page_settings import render_settings
except ImportError as e:
    st.error(f"ERRORE DI CARICAMENTO MODULI: {e}")

def main():
    # A. Inizializzazione Session State e Boot
    initialize_system()
    
    # B. Caricamento dati da JSON (se esistono)
    if 'data_loaded' not in st.session_state:
        load_os_data()
        st.session_state.data_loaded = True

    # C. Controllo Accesso
    if not st.session_state.get('authenticated', False):
        # Se non è loggato, mostra onboarding/login
        render_onboarding()
    else:
        # D. Rendering Sidebar e Navigazione
        # La sidebar gestisce il valore di st.session_state.current_page
        render_sidebar()
        
        page = st.session_state.get('current_page', 'Dashboard')

        # E. ROUTING LOGIC
        if page == "Dashboard":
            render_dashboard()
        elif page == "Neural Chat":
            render_chat()
        elif page == "Cyber Vault":
            render_vault()
        elif page == "Diario Serale":
            from logic.27_logic_review import render_evening_review
            render_evening_review()
        elif page == "Calendario":
            from calendar_module.26_calendar_core import render_interactive_calendar
            render_interactive_calendar()
        elif page == "Nexus Sociale":
            from social.25_social_nexus import render_social_nexus
            render_social_nexus()
        elif page == "Missioni":
            from logic.29_logic_goals import render_goals_manager
            render_goals_manager()
        elif page == "Settings":
            render_settings()
            
        # F. Auto-salvataggio periodico (opzionale)
        # Qui potresti inserire una logica che salva ogni X interazioni

if __name__ == "__main__":
    main()
