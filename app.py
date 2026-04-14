import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import plotly.graph_objects as go
from ui_styles import apply_synapse_ui, THEMES
import time

# ==============================================================================
# 1. INITIALIZATION ENGINE (PREVENZIONE ERRORI)
# ==============================================================================
def initialize_system():
    """Configura lo stato iniziale se non presente."""
    if 'system_ready' not in st.session_state:
        # Prima istruzione assoluta per Streamlit
        st.set_page_config(page_title="Synapse OS", layout="wide", initial_sidebar_state="collapsed")
        
        st.session_state.update({
            'system_ready': True,
            'user_profile': None,      # Conterrà i dati dell'utente
            'chat_log': [],            # Storico conversazione
            'current_theme': "Cyber Matrix",
            'onboarding_step': 1,      # Step della registrazione
            'temp_registration': {}    # Dati temporanei durante onboarding
        })

# ==============================================================================
# 2. NEURAL BRAIN (GOOGLE GEMINI 1.5)
# ==============================================================================
def call_synapse_ai(user_input):
    """Gestisce la comunicazione con l'AI con gestione errori avanzata."""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "CONFIG_ERROR: Chiave API mancante nei Secrets di Streamlit."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Recupero sicuro dei dati utente (Paracadute)
        profile = st.session_state.get('user_profile', {})
        user_nick = profile.get('nick', 'Sconosciuto')
        user_goals = profile.get('goals', 'Ottimizzazione generale')
        
        # Prompt di sistema istruito
        prompt_context = f"""
        Sei SYNAPSE OS, un'intelligenza artificiale di alto livello integrata nel sistema operativo di {user_nick}.
        Il tuo obiettivo primario è assisterlo in: {user_goals}.
        Il tuo tono è futuristico, sintetico, professionale e leggermente ironico.
        Usa termini tecnici e mantieni un'estetica cyberpunk nelle tue risposte.
        """
        
        full_query = f"{prompt_context}\n\nUTENTE: {user_input}"
        response = model.generate_content(full_query)
        return response.text
    
    except Exception as e:
        return f"SYNAPSE_CRASH: Impossibile stabilire connessione neurale. Dettaglio: {str(e)}"

# ==============================================================================
# 3. UI MODULES (ONBOARDING & MAIN)
# ==============================================================================
def run_onboarding():
    """Gestisce la prima configurazione dell'utente."""
    apply_synapse_ui(st.session_state.current_theme)
    
    # Layout centrato
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.markdown('<p class="os-title">SYNAPSE_INIT</p>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        step = st.session_state.onboarding_step
        
        if step == 1:
            st.subheader("🧬 FASE 1: ACQUISIZIONE DATI")
            nome = st.text_input("Nome Legale", placeholder="Inserisci nome...")
            nick = st.text_input("Alias (Nickname)", placeholder="Inserisci alias...")
            
            if st.button("PROSEGUI"):
                if nome and nick:
                    st.session_state.temp_registration.update({"nome": nome, "nick": nick})
                    st.session_state.onboarding_step = 2
                    st.rerun()
                else:
                    st.error("ERRORE: Inserire parametri validi per procedere.")
        
        elif step == 2:
            st.subheader("🎯 FASE 2: MATRICE OBIETTIVI")
            goals = st.text_area("Cosa vuoi ottimizzare con Synapse?", 
                                placeholder="Es: Voglio migliorare la mia forma fisica e il mio focus nel lavoro...")
            
            st.write("---")
            st.subheader("🎨 PERSONALIZZAZIONE")
            tema_scelto = st.selectbox("Interfaccia Visiva", list(THEMES.keys()))
            st.session_state.current_theme = tema_scelto
            
            if st.button("ATTIVA PROTOCOLLO"):
                if goals:
                    # Salvataggio finale del profilo
                    st.session_state.temp_registration["goals"] = goals
                    st.session_state.user_profile = st.session_state.temp_registration
                    st.success("Sincronizzazione completata. Benvenuto nel sistema.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("ERRORE: Definire almeno un obiettivo.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def run_main_app():
    """L'interfaccia principale dopo il login."""
    apply_synapse_ui(st.session_state.current_theme)
    t = THEMES.get(st.session_state.current_theme)
    profile = st.session_state.user_profile
    
    # Menu superiore Premium
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Diario AI", "Configurazione"],
        icons=["cpu", "chat-right-text", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"background-color": t['card'], "border": f"1px solid {t['main']}"},
            "nav-link": {"color": t['txt'], "font-family": "JetBrains Mono"},
            "nav-link-selected": {"background-color": t['main'], "color": t['bg']}
        }
    )

    # SEZIONE 1: DASHBOARD
    if selected == "Dashboard":
        st.markdown(f'<p class="os-title">{profile["nick"].upper()}_OS</p>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📡 STATUS PROTOCOLLI")
            st.write(f"**Identità:** {profile['nome']}")
            st.write(f"**Focus Attivo:** {profile['goals']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_b:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("⚙️ CORE")
            st.write("Uptime: 99.9%")
            st.write(f"Theme: {st.session_state.current_theme}")
            st.markdown('</div>', unsafe_allow_html=True)

    # SEZIONE 2: DIARIO AI
    elif selected == "Diario AI":
        st.markdown(f'<p class="os-title">NEURAL_LOG</p>', unsafe_allow_html=True)
        
        # Area messaggi
        for message in st.session_state.chat_log:
            div_class = "user-msg" if message["role"] == "user" else "ai-msg"
            st.markdown(f'<div class="{div_class}">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Input chat
        if user_query := st.chat_input("Inserisci input neurale..."):
            # Aggiungi messaggio utente
            st.session_state.chat_log.append({"role": "user", "content": user_query})
            
            # Chiama AI
            with st.spinner("Sincronizzazione in corso..."):
                ai_response = call_synapse_ai(user_query)
                st.session_state.chat_log.append({"role": "assistant", "content": ai_response})
            
            st.rerun()

    # SEZIONE 3: SISTEMA
    elif selected == "Configurazione":
        st.markdown('<p class="os-title">SYS_CONFIG</p>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        st.subheader("🛠 CAMBIO INTERFACCIA")
        nuovo_tema = st.selectbox("Seleziona nuovo set di colori", list(THEMES.keys()), 
                                 index=list(THEMES.keys()).index(st.session_state.current_theme))
        if st.button("AGGIORNA ESTETICA"):
            st.session_state.current_theme = nuovo_tema
            st.rerun()
            
        st.write("---")
        st.subheader("🛑 RESET DI FABBRICA")
        if st.button("ESEGUI REBOOT TOTALE"):
            # Pulisce tutto il session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. EXECUTION
# ==============================================================================
initialize_system()

if st.session_state.user_profile is None:
    run_onboarding()
else:
    run_main_app()
