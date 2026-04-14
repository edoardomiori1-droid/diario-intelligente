"""
SYNAPSE NEURAL OS - MAIN CORE v3.5
File: app.py
Status: EXECUTIVE / STABLE
Description: Motore principale dell'OS. Gestisce Onboarding, Dashboard e Neural Chat.
"""

import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import plotly.graph_objects as go
import pandas as pd
import time
from datetime import datetime

# Importiamo il design system dal file creato in precedenza
from ui_styles import apply_synapse_ui, THEMES, draw_section_title

# ==============================================================================
# 1. GLOBAL SYSTEM INITIALIZATION
# ==============================================================================

def initialize_neural_state():
    """
    Inizializza lo stato del sistema. 
    Assicura che tutte le variabili necessarie siano presenti per evitare KeyError.
    """
    # Configurazione pagina (deve essere la prima istruzione Streamlit)
    if 'system_initialized' not in st.session_state:
        st.set_page_config(
            page_title="Synapse Neural OS",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Setup dello stato iniziale
        st.session_state.update({
            'system_initialized': True,
            'boot_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_profile': None,           # Dati utente salvati post-onboarding
            'chat_history': [],             # Log della chat neurale
            'current_theme_id': "SYNAPSE_PRIME",
            'onboarding_stage': 1,          # Progresso configurazione
            'draft_data': {},               # Dati temporanei
            'system_logs': ["System Boot Successful", "Neural Engine Standby"]
        })

# ==============================================================================
# 2. NEURAL ENGINE (AI INTEGRATION)
# ==============================================================================

def call_neural_engine(user_prompt):
    """
    Gestisce la comunicazione con l'API Google Gemini.
    Integra il contesto del profilo utente per risposte personalizzate di alto livello.
    """
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "CRITICAL_ERROR: API_KEY_MISSING. Verificare i Secrets di Streamlit Cloud."
    
    try:
        genai.configure(api_key=api_key)
        # Utilizziamo il modello più veloce e reattivo per un'esperienza OS fluida
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Estrazione contesto profilo
        profile = st.session_state.user_profile
        context = f"""
        Identità Utente: {profile.get('nick')}
        Obiettivi Primari: {profile.get('objectives')}
        Parametri Neurali: Socialità {profile.get('social')}/10, Energia {profile.get('energy')}/10, Rischio {profile.get('risk')}/10.
        
        ISTRUZIONI OPERATIVE:
        Sei SYNAPSE OS. Rispondi in modo analitico, executive e preciso. 
        Usa un linguaggio tecnico ma chiaro. Non usare emoji. 
        Il tuo compito è ottimizzare le prestazioni dell'utente.
        """
        
        full_query = f"{context}\n\nUSER_INPUT: {user_prompt}"
        response = model.generate_content(full_query)
        
        # Registriamo l'evento nei log di sistema
        st.session_state.system_logs.append(f"AI_RESPONSE_GENERATED at {datetime.now().strftime('%H:%M:%S')}")
        
        return response.text
    
    except Exception as e:
        error_msg = f"NEURAL_LINK_FAILURE: {str(e)}"
        st.session_state.system_logs.append(error_msg)
        return error_msg

# ==============================================================================
# 3. INTERFACE MODULE: ONBOARDING PROTOCOL
# ==============================================================================

def run_onboarding_protocol():
    """
    Gestisce la fase di configurazione iniziale con un'estetica di alto prestigio.
    Diviso in step per una chiarezza assoluta.
    """
    apply_synapse_ui(st.session_state.current_theme_id)
    
    # Header centrato
    st.markdown('<p class="os-header">SYNAPSE_OS</p>', unsafe_allow_html=True)
    
    _, central_col, _ = st.columns([1, 2, 1])
    
    with central_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        stage = st.session_state.onboarding_stage
        st.write(f"**PROTOCOLLO DI INIZIALIZZAZIONE // STAGE {stage}**")
        st.progress(stage / 3)
        st.write("---")

        if stage == 1:
            draw_section_title("Identità Biometrica", "Inserimento dati anagrafici primari")
            
            nome = st.text_input("NOME COMPLETO", placeholder="Edoardo Miori")
            alias = st.text_input("ALIAS DI SISTEMA", placeholder="EDO_01")
            
            col_a, col_b = st.columns(2)
            nascita = col_a.date_input("DATA DI NASCITA", value=datetime(2000, 1, 1))
            settore = col_b.selectbox("SETTORE OPERATIVO", ["Engineering", "Finance", "Creative", "Health", "Student"])
            
            if st.button("SINCRONIZZA DATI >>"):
                if nome and alias:
                    st.session_state.draft_data.update({
                        "name": nome, "nick": alias, "dob": str(nascita), "sector": settore
                    })
                    st.session_state.onboarding_stage = 2
                    st.rerun()
                else:
                    st.error("ERRORE: Parametri identità incompleti.")

        elif stage == 2:
            draw_section_title("Matrice Neurale", "Calibrazione parametri della personalità")
            
            st.write("Definisci i livelli della tua matrice operativa (Scala 1-10):")
            s_val = st.select_slider("SOCIALITÀ (Interazione esterna)", options=range(1, 11), value=5)
            e_val = st.select_slider("ENERGIA (Output operativo)", options=range(1, 11), value=5)
            r_val = st.select_slider("RISCHIO (Propensione al cambiamento)", options=range(1, 11), value=5)
            
            st.write("---")
            draw_section_title("Configurazione Estetica", "Selezione interfaccia cromatica")
            selected_theme = st.selectbox(
                "THEME_PACK", 
                options=list(THEMES.keys()),
                format_func=lambda x: THEMES[x]["name"]
            )
            
            # Cambia il tema in tempo reale per anteprima
            if selected_theme != st.session_state.current_theme_id:
                st.session_state.current_theme_id = selected_theme
                st.rerun()

            if st.button("VALIDA MATRICE >>"):
                st.session_state.draft_data.update({
                    "social": s_val, "energy": e_val, "risk": r_val
                })
                st.session_state.onboarding_stage = 3
                st.rerun()

        elif stage == 3:
            draw_section_title("Obiettivi Strategici", "Definizione traguardi a breve e lungo termine")
            
            objectives = st.text_area(
                "OBIETTIVO PRIMARIO", 
                placeholder="Es: Ottimizzazione del workflow professionale e miglioramento della condizione atletica.",
                height=150
            )
            
            st.write("---")
            st.warning("Nota: Una volta avviato, il sistema richiederà un reboot completo per modificare questi parametri.")
            
            if st.button("AVVIA SYNAPSE_OS"):
                if objectives:
                    st.session_state.draft_data["objectives"] = objectives
                    # Trasferimento dati definitivo
                    st.session_state.user_profile = st.session_state.draft_data
                    st.session_state.system_logs.append("User Profile Linked Successfully")
                    st.rerun()
                else:
                    st.error("ERRORE: Definire almeno un obiettivo strategico.")
                    
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. INTERFACE MODULE: EXECUTIVE MAIN APP
# ==============================================================================

def run_main_application():
    """
    L'interfaccia principale del sistema. 
    Gestisce la Dashboard, il Diario Neurale e la gestione Sistema.
    """
    # Blindatura tema
    apply_synapse_ui(st.session_state.current_theme_id)
    theme = THEMES[st.session_state.current_theme_id]
    profile = st.session_state.user_profile
    
    # Navigation Executive Bar
    # Nota: Il menu blu seguirà ora correttamente la selezione
    selected_menu = option_menu(
        None, ["Dashboard", "Neural Log", "System Ops"],
        icons=["grid-3x3-gap-fill", "terminal-fill", "toggles"],
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"background-color": "transparent", "padding": "0", "margin-bottom": "30px"},
            "nav-link": {
                "font-family": "JetBrains Mono", 
                "color": "white", 
                "font-size": "14px", 
                "text-transform": "uppercase",
                "border-radius": "10px",
                "margin": "0 10px"
            },
            "nav-link-selected": {
                "background-color": theme['main'], 
                "color": theme['bg'],
                "font-weight": "800"
            }
        }
    )

    # --- SEZIONE A: DASHBOARD ---
    if selected_menu == "Dashboard":
        st.markdown(f'<p class="os-header">{profile["nick"]}_CORE</p>', unsafe_allow_html=True)
        
        col_main, col_side = st.columns([2, 1])
        
        with col_main:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            draw_section_title("Analisi Parametrica Persona", "Radar chart dei tratti neurali")
            
            # Grafico Radar Professionale (Plotly)
            categories = ['Socialità', 'Energia', 'Rischio', 'Focus', 'Analisi']
            # I valori focus e analisi sono simulati basandosi sugli altri parametri
            values = [
                profile['social'], 
                profile['energy'], 
                profile['risk'], 
                (profile['energy'] + profile['risk']) / 2,
                (profile['social'] + profile['energy']) / 2
            ]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values, theta=categories, fill='toself',
                line_color=theme['main'], fillcolor=f"{theme['main']}33"
            ))
            
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 10], color="#555", gridcolor="#333"),
                    angularaxis=dict(color="#888")
                ),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=80, r=80, t=40, b=40),
                font=dict(family="JetBrains Mono", color="#FFF")
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_side:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            draw_section_title("Dati Sessione", "Metriche operative real-time")
            st.write(f"**Uptime:** {st.session_state.boot_timestamp}")
            st.write(f"**Settore:** {profile['sector']}")
            st.write(f"**Tema Attivo:** {theme['name']}")
            st.write("---")
            st.write("**Obiettivo Primario:**")
            st.info(profile['objectives'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Widget Log di Sistema
            with st.expander("Visualizza Log di Sistema"):
                for log in reversed(st.session_state.system_logs[-5:]):
                    st.code(f"> {log}")

    # --- SEZIONE B: NEURAL LOG (CHATTING) ---
    elif selected_menu == "Neural Log":
        st.markdown(f'<p class="os-header">NEURAL_LOG</p>', unsafe_allow_html=True)
        
        # Container per la chat con altezza fissa
        chat_container = st.container(height=500)
        
        with chat_container:
            if not st.session_state.chat_history:
                st.write("Protocollo di comunicazione pronto. Inserire query per iniziare l'analisi.")
            
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f'<div class="user-bubble"><strong>{profile["nick"].upper()}</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-bubble"><strong>SYNAPSE_OS</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        
        # Area input in basso
        if user_input := st.chat_input("Inserisci log neurale..."):
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.spinner("Sincronizzazione neurale in corso..."):
                ai_reply = call_neural_engine(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
            
            st.rerun()

    # --- SEZIONE C: SYSTEM OPS ---
    elif selected_menu == "System Ops":
        st.markdown(f'<p class="os-header">SYSTEM_OPS</p>', unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            draw_section_title("Manutenzione Interfaccia", "Modifica parametri visivi")
            new_theme = st.selectbox(
                "CAMBIA TEMA OS", 
                options=list(THEMES.keys()),
                index=list(THEMES.keys()).index(st.session_state.current_theme_id),
                format_func=lambda x: THEMES[x]["name"]
            )
            if st.button("AGGIORNA CORE VISIVO"):
                st.session_state.current_theme_id = new_theme
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_right:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            draw_section_title("Protocollo Reset", "Cancellazione totale dati sessione")
            st.error("ATTENZIONE: Questa azione è irreversibile.")
            if st.button("WIPE_ALL_DATA"):
                # Reset totale dello stato
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. EXECUTION BOOTLOADER
# ==============================================================================

if __name__ == "__main__":
    initialize_neural_state()
    
    # Routing principale: Onboarding o App?
    if st.session_state.user_profile is None:
        run_onboarding_protocol()
    else:
        run_main_application()

# FINE CODICE app.py
