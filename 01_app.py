"""
SYNAPSE NEURAL OS - MASTER BOOTLOADER
------------------------------------
File 01/35 | 01_app.py
Ruolo: Punto di ingresso universale del sistema.

Questo file coordina l'intera architettura. Utilizza un sistema di 
caricamento dinamico per unire i moduli presenti nelle cartelle 
/core, /ui, /logic e /pages.
"""

import streamlit as st
import importlib
import sys

# =================================================================
# 1. CONFIGURAZIONE NATIVA DEL BROWSER
# =================================================================
# Deve essere la prima istruzione Streamlit eseguita.
st.set_page_config(
    page_title="Synapse Neural OS", 
    page_icon="🧠", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# =================================================================
# 2. SISTEMA DI IMPORTAZIONE DINAMICA
# =================================================================
def bootstrap_module(module_path):
    """
    Tenta di caricare un modulo specifico. 
    Se il file non esiste (perché stiamo ancora costruendo i 35 file),
    l'app non crasha ma gestisce l'assenza con eleganza.
    """
    try:
        return importlib.import_module(module_path)
    except ImportError as e:
        # Messaggio di debug per lo sviluppatore durante la costruzione
        print(f"DEBUG: Modulo {module_path} non ancora disponibile.")
        return None

# =================================================================
# 3. PROCEDURA DI AVVIO (BOOT SEQUENCE)
# =================================================================
def main():
    """Funzione principale che governa il flusso dell'OS."""

    # --- STEP 1: Inizializzazione Memoria (File 02) ---
    # Cerchiamo il file nella cartella 'core'
    core_init = bootstrap_module("core.02_core_init")
    
    if core_init:
        core_init.initialize_session()
    else:
        st.error("ERRORE CRITICO: Il Kernel di Memoria (core/02_core_init.py) è mancante.")
        st.stop()

    # --- STEP 2: Iniezione Design System (File 06) ---
    # Applica il CSS futuristico e l'effetto vetro
    ui_engine = bootstrap_module("ui.06_ui_engine")
    if ui_engine:
        ui_engine.apply_universal_styles()
    else:
        st.warning("INTERFACCIA: Design System (ui/06_ui_engine.py) non rilevato. Caricamento stile base...")

    # --- STEP 3: Logica di Accesso (File 04) ---
    # Decide se l'utente deve registrarsi o se può entrare nell'Hub
    core_auth = bootstrap_module("core.04_core_auth")
    
    if core_auth:
        if not core_auth.is_authenticated():
            # --- MOSTRA REGISTRAZIONE (File 10) ---
            onboarding = bootstrap_module("pages.10_page_onboarding")
            if onboarding:
                onboarding.render_setup()
            else:
                st.info("⚡ BENVENUTO IN SYNAPSE OS: In attesa della creazione del Modulo di Setup (File 10)...")
        else:
            # --- MOSTRA HUB PRINCIPALE (File 11) ---
            dashboard = bootstrap_module("pages.11_page_dashboard")
            if dashboard:
                dashboard.render_hub()
            else:
                st.success("✅ Identità Verificata. In attesa della creazione dell'interfaccia Hub (File 11)...")
    else:
        st.error("ERRORE SISTEMA: Modulo Autenticazione (core/04_core_auth.py) mancante.")

# =================================================================
# 4. ESECUZIONE
# =================================================================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"SISTEMA: Errore imprevisto nel ciclo principale: {e}")
        st.info("Suggerimento: Controlla che i percorsi delle cartelle siano corretti.")
