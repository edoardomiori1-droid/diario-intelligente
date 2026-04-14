"""
SYNAPSE NEURAL OS - MASTER BOOTLOADER
------------------------------------
File 01/35 | 01_app.py
Posizione: Root / (Principale)

DESCRIZIONE:
Questo è il punto di ingresso universale. Il Bootloader coordina 
l'ordine di esecuzione: prima la memoria (CORE), poi lo stile (UI), 
infine le pagine (PAGE). Utilizza importlib per navigare nelle 
sottocartelle in modo dinamico e sicuro.
"""

import streamlit as st
import importlib
import sys

# =================================================================
# 1. CONFIGURAZIONE NATIVA DEL BROWSER (CRITICO)
# =================================================================
# Deve essere la prima istruzione assoluta di Streamlit.
st.set_page_config(
    page_title="Synapse Neural OS", 
    page_icon="🧠", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Per un look pulito da OS
)

# =================================================================
# 2. SISTEMA DI CARICAMENTO MODULI (ENGINE)
# =================================================================
def load_system_module(module_path):
    """
    Tenta di importare un modulo specifico dalle sottocartelle.
    Se il file non esiste ancora, l'app mostra un avviso pulito.
    """
    try:
        return importlib.import_module(module_path)
    except ImportError:
        return None

# =================================================================
# 3. PROCEDURA DI AVVIO (SEQUENZA DI BOOT)
# =================================================================
def main():
    """Governa l'intero ciclo di vita dell'applicazione."""

    # --- FASE 1: Inizializzazione Memoria (File 02) ---
    # Cerchiamo il file core_init dentro la cartella 'core'
    core_init = load_system_module("core.02_core_init")
    
    if core_init:
        # Crea i registri (Session State) necessari per non far crashare l'app
        core_init.initialize_session()
    else:
        st.error("ERRORE KERNEL: Il File 'core/02_core_init.py' non è stato trovato.")
        st.stop()

    # --- FASE 2: Iniezione Estetica (File 06) ---
    # Carichiamo il motore grafico per applicare il CSS futuristico
    ui_engine = load_system_module("ui.06_ui_engine")
    if ui_engine:
        ui_engine.apply_styles()
    else:
        # Messaggio temporaneo finché non creiamo il file 06
        st.info("SISTEMA: Caricamento interfaccia base (Design System 06 non rilevato).")

    # --- FASE 3: Logica di Accesso & Routing (File 04) ---
    # Il File 04 decide se mandare l'utente al setup o all'Hub
    core_auth = load_system_module("core.04_core_auth")
    
    if core_auth:
        if not core_auth.is_authenticated():
            # --- MOSTRA PAGINA ONBOARDING (File 10) ---
            onboarding = load_system_module("pages.10_page_onboarding")
            if onboarding:
                onboarding.render_setup()
            else:
                st.warning("⚠️ ATTIVAZIONE RICHIESTA: Crea il File 'pages.10_page_onboarding.py'.")
        else:
            # --- MOSTRA HUB OPERATIVO (File 11) ---
            dashboard = load_system_module("pages.11_page_dashboard")
            if dashboard:
                dashboard.render_hub()
            else:
                st.success("✅ IDENTITÀ CONFERMATA: In attesa della creazione della Dashboard (File 11).")
    else:
        st.error("ERRORE SICUREZZA: Modulo di Autenticazione (core/04_core_auth.py) mancante.")

# =================================================================
# 4. ESECUZIONE DEL KERNEL
# =================================================================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Gestore di errori 'di ultima istanza' per evitare schermate bianche
        st.error(f"SISTEMA: Errore imprevisto durante l'esecuzione: {e}")
