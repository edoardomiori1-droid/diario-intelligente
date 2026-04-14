"""
SYNAPSE NEURAL OS - UNIVERSAL EDITION
-------------------------------------
File 01/35: app.py
Ruolo: Master Bootloader & Orchestrator

Questo file rappresenta il punto di ingresso unico del sistema. 
È progettato per essere agnostico e modulare: non contiene logica di business, 
ma importa i componenti necessari dai dipartimenti specifici (/core, /ui, /pages).
"""

import streamlit as st

# --- IMPORTAZIONE MODULI DI SISTEMA (FUTURI FILE) ---
# Questi file verranno creati nei passaggi successivi per mantenere l'ordine.

from core.core_init import initialize_session     # File 02: Inizializza la memoria
from core.core_config import get_system_config    # File 06: Carica le costanti
from ui.ui_css_injector import inject_styles      # File 14: Inietta il CSS universale
from ui.ui_navigation import render_nav_bar      # File 18: Gestisce il menu

def main():
    """
    Funzione principale di controllo.
    Gestisce il ciclo di vita dell'applicazione e il passaggio tra le fasi.
    """
    
    # 1. SETUP AMBIENTE DI ESECUZIONE
    # Configura i parametri della pagina web (Titolo, Icona, Layout)
    # Questa è l'unica istruzione di configurazione permessa in app.py
    st.set_page_config(
        page_title="Synapse Neural OS",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # 2. INIZIALIZZAZIONE REGISTRI (CORE)
    # Richiama il modulo che crea il 'Session State'. Senza questo, l'app crasha.
    # Vedremo questo dettaglio nel File 02.
    initialize_session()

    # 3. CARICAMENTO MOTORE GRAFICO (UI)
    # Inietta il codice CSS personalizzato per ottenere l'effetto Glassmorphism.
    # Vedremo questo dettaglio nel File 14.
    inject_styles()

    # 4. LOGICA DI ROUTING (LOGIC)
    # Determina se l'utente deve vedere la configurazione iniziale o l'HUB.
    
    # CONTROLLO IDENTITÀ:
    # Se la variabile 'user_profile' è vuota, l'utente è nuovo o ha resettato.
    if st.session_state.user_profile is None:
        
        # Carichiamo il modulo Onboarding (File 20)
        from pages.page_ob_intro import render_onboarding_sequence
        render_onboarding_sequence()
        
    else:
        # L'utente è autenticato e il profilo è caricato.
        # Carichiamo la barra di navigazione universale (File 18)
        current_page = render_nav_bar()
        
        # SMISTAMENTO PAGINE HUB:
        if current_page == "Dashboard":
            from pages.page_dash_main import render_dashboard_hub # File 23
            render_dashboard_hub()
            
        elif current_page == "Neural Chat":
            from pages.page_chat_interface import render_neural_chat # File 26
            render_neural_chat()
            
        elif current_page == "System Settings":
            from pages.page_settings_main import render_sys_settings # File 27
            render_sys_settings()
            
        # PREDISPOSIZIONE PER ESPANSIONI FUTURE (FILE 28-35)
        # Qui verranno aggiunti i collegamenti ai moduli futuri.

# --- PUNTO DI AVVIO CRITICO ---
# Assicura che l'app venga eseguita solo quando richiamata direttamente.
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Gestione errori universale per evitare il crash bianco della pagina
        st.error(f"SISTEMA: Errore critico durante il boot: {e}")
        st.info("Eseguire un Factory Reset dalle impostazioni o ricaricare la pagina.")
