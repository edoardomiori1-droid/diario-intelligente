"""
SYNAPSE NEURAL OS - ONBOARDING SYSTEM
-------------------------------------
File 10/35 | pages/10_page_onboarding.py
Posizione: /pages/10_page_onboarding.py

DESCRIZIONE:
Modulo di configurazione iniziale. Gestisce la creazione del profilo
utente e l'assegnazione delle statistiche base.
"""

import streamlit as st
from datetime import date

# Importiamo i moduli di supporto che abbiamo creato nei file precedenti
try:
    from core.03_core_config import get_config, get_privacy_text
    from ui.08_ui_components import section_header, glass_card
    from ui.07_ui_assets import draw_header_line
except ImportError:
    pass

def render_setup():
    """Esegue l'interfaccia di registrazione step-by-step."""
    
    config = get_config()
    
    # TITOLO PRINCIPALE
    st.markdown("<h1 style='text-align: center;'>NEURAL INITIALIZATION</h1>", unsafe_allow_html=True)
    st.caption(f"<p style='text-align: center;'>{get_privacy_text()}</p>", unsafe_allow_html=True)
    st.divider()

    # Layout a colonna centrale per un look pulito
    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        # --- STEP 1: DATI ANAGRAFICI ---
        if st.session_state.onboarding_step == 1:
            section_header("Identità", icon="👤")
            
            nickname = st.text_input("Scegli il tuo Nickname Operatore", placeholder="Es: Neo_01")
            
            # IL FIX DEL 2010: impostiamo il valore di default dalle config
            birth_date = st.date_input(
                "Data di Nascita Neurale",
                value=config['calendar']['default_date'],
                min_value=config['calendar']['min_date'],
                max_value=config['calendar']['max_date']
            )
            
            sector = st.selectbox("Settore Operativo", config['sectors'])

            if st.button("PROCEDI ALLA FASE 2 →"):
                if nickname:
                    st.session_state.temp_profile = {
                        "nickname": nickname,
                        "birth_date": str(birth_date),
                        "sector": sector
                    }
                    st.session_state.onboarding_step = 2
                    st.rerun()
                else:
                    st.error("Inserire un nickname per continuare.")

        # --- STEP 2: ASSEGNAZIONE STATISTICHE (RADAR) ---
        elif st.session_state.onboarding_step == 2:
            section_header("Parametri Neurali", icon="📊")
            st.info("Assegna i valori base alle tue attitudini (da 1 a 10).")

            stats = {}
            for s in config['radar_stats']:
                stats[s] = st.select_slider(f"Livello {s}", options=range(1, 11), value=5)

            col_back, col_next = st.columns(2)
            with col_back:
                if st.button("← INDIETRO"):
                    st.session_state.onboarding_step = 1
                    st.rerun()
            
            with col_next:
                if st.button("COMPLETA SINCRONIZZAZIONE ✅"):
                    # Uniamo i dati e salviamo nel profilo definitivo
                    full_profile = st.session_state.temp_profile
                    full_profile["stats"] = stats
                    
                    # SALVATAGGIO FINALE NELLA MEMORIA CENTRALE (File 02)
                    st.session_state.user_profile = full_profile
                    st.balloons()
                    st.success("Sincronizzazione completata. Benvenuto nel Sistema.")
                    st.rerun() # Questo riavvio manderà l'utente alla Dashboard (File 11) via File 01

def save_profile_to_memory(data):
    """Funzione interna per il commit dei dati."""
    st.session_state.user_profile = data
