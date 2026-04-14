"""
SYNAPSE NEURAL OS - SYSTEM SETTINGS
-----------------------------------
File 14/35 | pages/14_page_settings.py
Posizione: /pages/14_page_settings.py

DESCRIZIONE:
Pannello di controllo per la personalizzazione dell'esperienza
e il monitoraggio dell'integrità del sistema.
"""

import streamlit as st

# Import moduli UI e Core
try:
    from ui.09_ui_sidebar import render_sidebar
    from ui.08_ui_components import section_header, glass_card
    from core.05_core_reset import execute_factory_reset
except ImportError:
    pass

def render_settings():
    """Rendering del pannello impostazioni."""
    
    # 1. SIDEBAR & HEADER
    render_sidebar()
    section_header("System Settings", icon="⚙️")
    
    # 2. SEZIONE ESTETICA (THEME ENGINE)
    st.subheader("🎨 Personalizzazione Interfaccia")
    col_theme, col_visual = st.columns(2)
    
    with col_theme:
        theme_choice = st.selectbox(
            "Protocollo Cromatico", 
            ["NEON_CYBER (Default)", "AMBER_VINTAGE", "MATRIX_GREEN", "GHOST_WHITE"]
        )
        if st.button("Applica Tema"):
            st.session_state.active_theme = theme_choice
            st.toast(f"Tema {theme_choice} applicato correttamente.")

    with col_visual:
        st.write("Effetti Visivi")
        st.checkbox("Abilita Blur Vetro", value=True)
        st.checkbox("Animazioni Interfaccia", value=True)

    st.divider()

    # 3. STATO MODULI (DIAGNOSTICA)
    st.subheader("📡 Integrità Moduli")
    
    moduli = {
        "Core Kernel (01-05)": "ONLINE",
        "UI Engine (06-09)": "ONLINE",
        "Neural Pages (10-14)": "ACTIVE",
        "AI Logic (15+)": "PENDING"
    }
    
    cols = st.columns(len(moduli))
    for i, (name, status) in enumerate(moduli.items()):
        with cols[i]:
            color = "#00FFC8" if status != "PENDING" else "#FFCC00"
            st.markdown(f"""
                <div style='border: 1px solid {color}; padding: 10px; border-radius: 5px; text-align: center;'>
                    <p style='font-size: 0.7em; margin-bottom: 5px;'>{name}</p>
                    <b style='color: {color};'>{status}</b>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # 4. ZONA PERICOLO (RESET)
    st.subheader("⚠️ Protocolli Critici")
    with st.expander("FACTORY RESET (ATTENZIONE)"):
        st.warning("Questa azione cancellerà permanentemente il tuo profilo, i log e tutti i dati nel Vault.")
        confirm = st.text_input("Scrivi 'RESET' per confermare l'operazione")
        if st.button("ESEGUI WIPE TOTALE"):
            if confirm == "RESET":
                execute_factory_reset()
            else:
                st.error("Conferma non valida.")

# Se il file viene chiamato direttamente
if __name__ == "__main__":
    render_settings()
