"""
SYNAPSE NEURAL OS - MASTER BOOTLOADER
------------------------------------
File 01/35 | 01_app.py
Ruolo: Punto di ingresso unico.
"""

import streamlit as st
import importlib

# 1. SETUP SCHERMO (Obbligatorio come prima riga)
st.set_page_config(
    page_title="Synapse Neural OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CARICATORE MODULI
def boot(path):
    try:
        return importlib.import_module(path)
    except:
        return None

def main():
    # Inizializza Memoria (File 02)
    core_init = boot("core.02_core_init")
    if core_init:
        core_init.initialize_session()
    
    # Iniezione Stile (File 06)
    ui_engine = boot("ui.06_ui_engine")
    if ui_engine:
        ui_engine.apply_styles()

    # Controllo Accesso (File 04)
    core_auth = boot("core.04_core_auth")
    if core_auth and not core_auth.is_authenticated():
        # Pagina Registrazione (File 10)
        onboarding = boot("pages.10_page_onboarding")
        if onboarding:
            onboarding.render_setup()
        else:
            st.info("SISTEMA: In attesa della creazione del File 10 (Onboarding)...")
    else:
        st.success("SISTEMA OPERATIVO ONLINE")
        if st.button("Factory Reset"):
            reset = boot("core.05_core_reset")
            if reset: reset.execute_reset()

if __name__ == "__main__":
    main()
