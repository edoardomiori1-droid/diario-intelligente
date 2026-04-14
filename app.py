import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import pandas as pd
import plotly.graph_objects as go
from ui_styles import apply_synapse_ui, THEMES
from datetime import datetime
import time

# ==============================================================================
# 1. CORE INITIALIZATION ENGINE
# ==============================================================================
# Deve essere la primissima istruzione assoluta
if 'page_init' not in st.session_state:
    st.set_page_config(
        page_title="Synapse Neural OS v2.0",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    # Inizializzazione Session State per prevenire TypeError
    st.session_state.update({
        'page_init': True,
        'user_profile': None,      # Conterrà i dati dell'onboarding
        'chat_log': [],            # Storico conversazione Diario
        'current_theme': "Synapse Prime (Matrix)",
        'onboarding_step': 1,      # Step dell'onboarding
        'temp_reg_data': {}        # Dati temporanei di registrazione
    })

# ==============================================================================
# 2. AI LOGIC (GEMINI NEURAL ENGINE)
# ==============================================================================
def get_ai_response(prompt):
    """Gestisce la comunicazione con l'API Gemini incorporando il contesto utente."""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "ERROR_AI: GEMINI_API_KEY non trovata nei Secrets di Streamlit."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Recupero dati profilo per il prompt contestuale
        up = st.session_state.user_profile
        nick = up.get('nick', 'Sconosciuto')
        goals = up.get('goals', 'Ottimizzazione generale della vita')
        
        # Prompt ingegnerizzato
        system_context = f"""
        PROFILO UTENTE SYNAPSE OS:
        - Nome: {up['nome']} (Alias: {nick})
        - Età: {up['data_nascita']} | Genere: {up['genere']}
        - Matrice Neurale: Socialità {up['social']}, Energia {up['energia']}, Rischio {up['rischio']}
        - Tono Richiesto: {up['vibe_ai']}
        - Obiettivo Primario: {goals}
        
        ISTRUZIONI: Rispondi come SYNAPSE, un'entità digitale executive. Sii conciso, professionale,
        diretto e utilizza termini tecnici. Evita emoji e linguaggio infantile.
        """
        
        full_query = f"{system_context}\n\nINPUT_UTENTE: {prompt}"
        response = model.generate_content(full_query)
        return response.text
    except Exception as e:
        return f"CRASH_SISTEMA: Connessione neurale fallita. Dettaglio: {str(e)}"

# ==============================================================================
# 3. UIMODULE: ONBOARDING PROTOCOL
# ==============================================================================
def render_onboarding():
    """Schermata di configurazione iniziale (Professional & Seria)."""
    # Applichiamo il tema attuale preventivamente per bloccare i colori
    apply_synapse_ui(st.session_state.current_theme)
    
    st.markdown('<p class="os-header">SYNAPSE_INIT</p>', unsafe_allow_input=True)
    
    col_a, col_main, col_c = st.columns([1, 2, 1])
    
    with col_main:
        st.markdown('<div class="glass-card">', unsafe_allow_input=True)
        step = st.session_state.onboarding_step
        
        # Header Modulo
        st.write(f"📂 **MODULO PROTOCOLLO_INIT: {step}/3**")
        st.progress(step / 3)
        st.write("---")

        if step == 1:
            st.subheader("🧬 Modulo I: Identità Biometrica")
            nome_c = st.text_input("Nome e Cognome", placeholder="Edoardo Miori")
            nick = st.text_input("Nickname di Sistema", placeholder="Edo")
            col1, col2 = st.columns(2)
            dn = col1.date_input("Data di Nascita", value=datetime(2000, 1, 1))
            genere = col2.selectbox("Identità", ["Maschile", "Femminile", "Non binario", "Non specificato"])
            
            if st.button("SALVA E PROSEGUI >>"):
                if nome_c and nick:
                    st.session_state.temp_reg_data.update({
                        "nome": nome_c, "nick": nick, 
                        "data_nascita": str(dn), "genere": genere
                    })
                    st.session_state.onboarding_step = 2
                    st.rerun()
                else: st.warning("Dati insufficienti per l'inizializzazione.")

        elif step == 2:
            st.subheader("📡 Modulo II: Matrice Neurale")
            st.write("Imposta i tuoi parametri pilota (1-10):")
            col1, col2, col3 = st.columns(3)
            s = col1.select_slider("Socialità", range(1, 11), 5)
            e = col2.select_slider("Energia", range(1, 11), 5)
            r = col3.select_slider("Rischio", range(1, 11), 5)
            
            st.write("---")
            vibe = st.radio("Stile di comunicazione AI desiderato:", 
                           ["Diretto e Analitico", "Gentile e Motivatore", "Ironico e Scientifico"])
            
            if st.button("CONFIGURA ESTETICA >>"):
                st.session_state.temp_reg_data.update({"social":s, "energia":e, "rischio":r, "vibe_ai":vibe})
                st.session_state.onboarding_step = 3
                st.rerun()

        elif step == 3:
            st.subheader("🎨 Modulo III: Personalizzazione OS")
            st.write("Seleziona il tuo pacchetto colori d'interfaccia:")
            tema_scelto = st.selectbox("Seleziona Tema", list(THEMES.keys()), index=0)
            
            # Anteprima istantanea del tema scelto
            if tema_scelto != st.session_state.current_theme:
                st.session_state.current_theme = tema_scelto
                st.rerun()
            
            st.write("---")
            goals = st.text_area("Cosa vuoi ottimizzare questo mese?", placeholder="Es: Produttività sul lavoro e sport.")
            
            if st.button("AVVIA PROTOCOLLO SYNAPSE"):
                if goals:
                    # Salvataggio definitivo del profilo
                    st.session_state.temp_reg_data["goals"] = goals
                    st.session_state.user_profile = st.session_state.temp_reg_data
                    st.success("Analisi Neurale completata. Avvio Synapse OS.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else: st.warning("Definire almeno un obiettivo primario.")
        
        st.markdown('</div>', unsafe_allow_input=True)

# ==============================================================================
# 4. UIMODULE: MAIN APPLICATION HUB
# ==============================================================================
def render_main_app():
    """L'app principale dopo il login (Executive Dashboard e Diario)."""
    # Blindatura Cromatica Definitiva
    apply_synapse_ui(st.session_state.current_theme)
    t = THEMES[st.session_state.current_theme]
    
    # Navigation Bar (st.option_menu con stile fisso)
    # Questa barra segue la navigazione e il menu blu si sposta
    menu = option_menu(
        None, ["Dashboard", "Diario Neurale", "Network", "Sistema"],
        icons=["cpu-fill", "journal-text", "people-fill", "gear-fill"],
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"background-color": t['card'], "padding": "0!important", "border": f"1px solid {t['main']}22"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "color": t['txt']},
            "nav-link-selected": {"background-color": t['main'], "color": t['bg'], "font-weight": "700"}
        }
    )

    # AREA CONTENUTO
    if menu == "Dashboard":
        st.markdown(f"### <span style='color:{t['main']}'>// DASHBOARD_GENERALE:</span> {st.session_state.user_profile['nick']}", unsafe_allow_input=True)
        
        up = st.session_state.user_profile
        col_chart, col_data = st.columns([1, 1])
        
        # Grafico Radar Personality (Executive Look)
        with col_chart:
            st.markdown('<div class="glass-card" style="padding:20px">', unsafe_allow_input=True)
            categories = ['Socialità', 'Energia', 'Rischio']
            values = [up['social'], up['energia'], up['rischio']]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values, theta=categories, fill='toself', 
                line_color=t['main'], fillcolor=f"{t['main']}33"
            ))
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 10], color="#888")),
                showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font_color="white",
                margin=dict(l=40, r=40, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_input=True)

        with col_data:
            st.markdown(f"Età: {up['data_nascita']} | Vibe AI: {up['vibe_ai']}")
            st.write("**OBIETTIVI CORRENTI:**")
            st.info(up['goals'])
            st.metric("Messaggi Loggati", len(st.session_state.chat_log))

    elif menu == "Diario Neurale":
        st.subheader("🖋️ Registro di Comunicazione")
        
        # Area Storico Messaggi
        chat_container = st.container(height=500)
        with chat_container:
            if not st.session_state.chat_log:
                st.info("Nessun log trovato. Inizia la sincronizzazione scrivendo qui sotto.")
            for m in st.session_state.chat_log:
                div_class = "chat-user" if m["role"] == "user" else "chat-ai"
                # Aggiungiamo un prefisso per professionalità
                prefix = "UTENTE:" if m["role"] == "user" else "SYNAPSE:"
                st.markdown(f'<div class="{div_class}"><strong>{prefix}</strong><br>{m["content"]}</div>', unsafe_allow_input=True)

        # Input Messaggio (st.chat_input è in basso)
        if prompt := st.chat_input("Digita un pensiero..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            
            with st.spinner("Processing neurale..."):
                response = get_ai_response(prompt)
                st.session_state.chat_log.append({"role": "assistant", "content": response})
            st.rerun() # Ricarica per mostrare subito la risposta

    elif menu == "Network":
        st.subheader("👥 Cerchio Sociale")
        st.info("Funzionalità in fase di addestramento.")

    elif menu == "Sistema":
        st.subheader("⚙️ Configurazione")
        st.markdown('<div class="glass-card">', unsafe_allow_input=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Estetica OS**")
            n_t = st.selectbox("Cambia Tema", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.current_theme))
            if st.button("APPLICA TEMA"):
                st.session_state.current_theme = n_t
                st.rerun()
                
        with col2:
            st.write("**Manutenzione Dati**")
            if st.button("WIPE_SYSTEM (Reset Totale)"):
                st.session_state.update({'user_profile': None, 'onboarding_step': 1, 'chat_log': []})
                st.rerun()
        st.markdown('</div>', unsafe_allow_input=True)

# ==============================================================================
# 5. EXECUTION ENGINE
# ==============================================================================
# Se il profilo non esiste, avvia onboarding, altrimenti l'app principale
if st.session_state.user_profile is None:
    render_onboarding()
else:
    render_main_app()

# ==============================================================================
# FINE CODICE SYNAPSE OS v2.0
# ==============================================================================
