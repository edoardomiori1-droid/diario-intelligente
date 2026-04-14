"""
SYNAPSE NEURAL OS - SIDEBAR NAVIGATION
--------------------------------------
File 09/35 | ui/09_ui_sidebar.py
Posizione: /ui/09_ui_sidebar.py

DESCRIZIONE:
Gestisce l'interfaccia di navigazione laterale.
Include il selettore delle pagine e le info rapide sul profilo utente.
"""

import streamlit as st
try:
    from core.04_core_auth import is_authenticated, get_current_user
    from ui.07_ui_assets import get_assets
except ImportError:
    pass

def render_sidebar():
    """
    Disegna la barra laterale con lo stile Synapse.
    """
    assets = get_assets()
    
    with st.sidebar:
        # 1. LOGO E TITOLO
        st.markdown(f"""
            <div style='text-align: center; padding: 10px;'>
                <h2 style='color: #00F2FF; margin-bottom: 0;'>SYNAPSE</h2>
                <p style='font-size: 0.8em; opacity: 0.6;'>NEURAL OS v5.5</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()

        # 2. INFO UTENTE (Se loggato)
        if is_authenticated():
            user = get_current_user()
            st.markdown(f"**OPERATORE:** `{user.get('nickname', 'Unknown').upper()}`")
            st.caption(f"📍 Settore: {user.get('sector', 'General')}")
            
            st.divider()
            
            # 3. MENU DI NAVIGAZIONE
            # Il valore scelto qui cambierà 'st.session_state.active_hub_page'
            options = [
                f"{assets['nav']['dashboard']} Dashboard",
                f"{assets['nav']['chat']} Neural Chat",
                f"{assets['nav']['vault']} Cyber Vault",
                f"{assets['nav']['settings']} Impostazioni"
            ]
            
            selection = st.radio("SISTEMA DI NAVIGAZIONE", options)
            st.session_state.active_hub_page = selection.split(" ")[1]

            st.divider()
            
            # 4. TASTO LOGOUT (In basso)
            if st.button(f"{assets['nav']['logout']} Disconnetti"):
                from core.04_core_auth import logout
                logout()
        
        else:
            # Stato durante l'onboarding
            st.info("🔒 In attesa di inizializzazione profilo...")
            st.caption("Completa il setup per sbloccare i moduli.")

def get_active_page():
    """Ritorna il nome della pagina selezionata nella sidebar."""
    return st.session_state.get('active_hub_page', 'Dashboard')
