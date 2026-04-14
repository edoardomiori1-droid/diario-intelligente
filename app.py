import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# ==============================================================================
# 1. ARCHITETTURA DEL DESIGN SYSTEM (10 TEMI PROFESSIONALI)
# ==============================================================================
# Ogni tema definisce la palette cromatica per background, card, testi e accenti.
THEMES = {
    "Cyber Matrix": {
        "main": "#00FF41", "sec": "#008F11", "bg": "#0D0D0D", 
        "card": "#1A1A1A", "txt": "#E0E0E0", "sidebar": "#000000"
    },
    "Synthetic Sunset": {
        "main": "#FF8C00", "sec": "#FF0080", "bg": "#120D16", 
        "card": "#1D1625", "txt": "#F5F5F5", "sidebar": "#120D16"
    },
    "Deep Space": {
        "main": "#00FFFF", "sec": "#007FFF", "bg": "#050A10", 
        "card": "#0F1720", "txt": "#E0F7FA", "sidebar": "#050A10"
    },
    "Crimson Fury": {
        "main": "#FF0000", "sec": "#8B0000", "bg": "#0F0F0F", 
        "card": "#1C1C1C", "txt": "#FFFFFF", "sidebar": "#000000"
    },
    "Arctic Frost": {
        "main": "#74EBD5", "sec": "#9FACE6", "bg": "#F0F4F8", 
        "card": "#FFFFFF", "txt": "#2C3E50", "sidebar": "#E0E7FF"
    },
    "Royal Amethyst": {
        "main": "#FF00FF", "sec": "#7000FF", "bg": "#0A0510", 
        "card": "#160D25", "txt": "#FDF0FF", "sidebar": "#0A0510"
    },
    "Forest Guard": {
        "main": "#C2B280", "sec": "#4F7942", "bg": "#0D110D", 
        "card": "#161D16", "txt": "#ECECEC", "sidebar": "#0D110D"
    },
    "Midnight Gold": {
        "main": "#D4AF37", "sec": "#996515", "bg": "#0A0A0A", 
        "card": "#141414", "txt": "#F4F4F4", "sidebar": "#000000"
    },
    "Tokyo Drift": {
        "main": "#FF69B4", "sec": "#00FFFF", "bg": "#0F0510", 
        "card": "#1A0D1D", "txt": "#FFFFFF", "sidebar": "#0F0510"
    },
    "Carbon Fiber": {
        "main": "#FFFFFF", "sec": "#555555", "bg": "#0A0A0A", 
        "card": "#1A1A1A", "txt": "#F0F0F0", "sidebar": "#000000"
    }
}

# ==============================================================================
# 2. GESTIONE DELLO STATO (SESSION STATE)
# ==============================================================================
def initialize_session():
    """Inizializza tutte le variabili di sessione necessarie per il funzionamento dell'app."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.user_profile = None
        st.session_state.chat_log = []
        st.session_state.current_theme = "Cyber Matrix"
        st.session_state.onboarding_step = 1
        st.session_state.temp_data = {}
        st.session_state.mood_history = []
        st.session_state.people_log = []

initialize_session()
theme = THEMES[st.session_state.current_theme]

# ==============================================================================
# 3. ENGINE ESTETICO (CSS INJECTION)
# ==============================================================================
st.set_page_config(page_title="Synapse Neural OS", page_icon="🧠", layout="wide")

def apply_custom_styles(theme_data):
    """Inietta CSS personalizzato basato sul tema selezionato."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');
        
        /* Reset e Base */
        html, body, [class*="css"] {{
            background-color: {theme_data['bg']};
            color: {theme_data['txt']};
            font-family: 'Inter', sans-serif;
        }}
        
        .stApp {{ background: {theme_data['bg']}; }}

        /* Titoli Cyberpunk */
        .glitch-title {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 3.5rem;
            background: linear-gradient(90deg, {theme_data['main']}, {theme_data['sec']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0px;
            filter: drop-shadow(0 0 10px {theme_data['main']}44);
        }}

        /* Container Moduli */
        .module-container {{
            background-color: {theme_data['card']};
            border: 1px solid {theme_data['main']}33;
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
            margin-top: 30px;
        }}

        /* Form Styling */
        .stTextInput>div>div>input, .stDateInput>div>div>input, .stSelectbox>div>div {{
            background-color: rgba(255,255,255,0.03) !important;
            border: 1px solid {theme_data['main']}22 !important;
            color: {theme_data['txt']} !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }}

        /* Buttons Customization */
        .stButton>button {{
            width: 100%;
            background: linear-gradient(135deg, {theme_data['main']}, {theme_data['sec']}) !important;
            color: {theme_data['bg']} !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 15px !important;
            height: 3.5rem !important;
            transition: 0.4s all ease;
            text-transform: uppercase;
        }}
        .stButton>button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 20px {theme_data['main']}66;
        }}

        /* Chat Bubbles */
        .chat-msg-user {{
            background: {theme_data['card']};
            border-right: 5px solid {theme_data['main']};
            padding: 20px;
            border-radius: 15px 0 15px 15px;
            margin-bottom: 20px;
        }}
        .chat-msg-ai {{
            background: {theme_data['card']};
            border-left: 5px solid {theme_data['sec']};
            padding: 20px;
            border-radius: 0 15px 15px 15px;
            margin-bottom: 20px;
            color: {theme_data['txt']};
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: {theme_data['sidebar']};
            border-right: 1px solid {theme_data['main']}22;
        }}
        </style>
    """, unsafe_allow_input=True)

apply_custom_styles(theme)

# ==============================================================================
# 4. LOGICA INTELLIGENZA ARTIFICIALE
# ==============================================================================
def load_ai_engine():
    """Configura e carica il modello Gemini 1.5."""
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            return genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            st.error(f"Sistema Neurale Offline: {e}")
    return None

model = load_ai_engine()

# ==============================================================================
# 5. SCHERMATA ONBOARDING (MODULI A STEP)
# ==============================================================================
def render_onboarding():
    """Gestisce l'intero flusso di presentazione iniziale."""
    st.markdown('<p class="glitch-title">SYNAPSE_OS</p>', unsafe_allow_input=True)
    st.markdown("<p style='text-align:center; opacity:0.6;'>Inizializzazione protocollo di allineamento neurale...</p>", unsafe_allow_input=True)
    
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        st.markdown('<div class="module-container">', unsafe_allow_input=True)
        
        # Indicatori di progresso
        step = st.session_state.onboarding_step
        cols_prog = st.columns(3)
        for i, c in enumerate(cols_prog):
            if i+1 <= step: c.markdown(f"<div style='height:5px; background:{theme['main']}; border-radius:10px;'></div>", unsafe_allow_input=True)
            else: c.markdown("<div style='height:5px; background:rgba(255,255,255,0.1); border-radius:10px;'></div>", unsafe_allow_input=True)
        
        st.write(f"**MODULO {step} DI 3**")

        if step == 1:
            st.subheader("🧬 Fase 1: Anagrafica Digitale")
            nome = st.text_input("Nome e Cognome", placeholder="Edoardo Miori")
            nick = st.text_input("Identificativo Utente (Nickname)", placeholder="Edo")
            data_n = st.date_input("Data di Nascita", value=datetime(2000, 1, 1))
            genere = st.selectbox("Genere", ["Maschile", "Femminile", "Non binario", "Altro"])
            
            if st.button("PROCEDI ALLA CALIBRAZIONE"):
                if nome and nick:
                    st.session_state.temp_data.update({
                        "nome": nome, "nick": nick, 
                        "nascita": str(data_n), "genere": genere
                    })
                    st.session_state.onboarding_step = 2
                    st.rerun()
                else: st.warning("Sistema: Campi obbligatori mancanti.")

        elif step == 2:
            st.subheader("📡 Fase 2: Profilazione Comportamentale")
            st.write("Configura i tuoi parametri pilota per ottimizzare le risposte dell'AI:")
            
            soc = st.select_slider("Propensione Sociale", options=range(1, 11), value=5)
            ene = st.select_slider("Livello Energia Tipico", options=range(1, 11), value=5)
            ris = st.select_slider("Tolleranza al Rischio", options=range(1, 11), value=5)
            
            tono = st.radio("Stile di comunicazione AI:", 
                           ["Diretto e Analitico", "Gentile e Motivatore", "Ironico e Tagliente", "Scientifico"])
            
            if st.button("CONFIGURA ESTETICA"):
                st.session_state.temp_data.update({
                    "social": soc, "energy": ene, "risk": ris, "vibe": tono
                })
                st.session_state.onboarding_step = 3
                st.rerun()

        elif step == 3:
            st.subheader("🎨 Fase 3: Personalizzazione OS")
            tema_scelto = st.selectbox("Seleziona Pacchetto Colori", list(THEMES.keys()))
            obiettivi = st.text_area("Qual è il tuo obiettivo primario per Synapse?", 
                                   placeholder="Es: Migliorare la disciplina nello studio e monitorare lo sport.")
            
            if st.button("AVVIA SYNAPSE"):
                st.session_state.temp_data.update({
                    "tema": tema_scelto, "obiettivi": obiettivi
                })
                st.session_state.user_profile = st.session_state.temp_data
                st.session_state.current_theme = tema_scelto
                st.balloons()
                time.sleep(1.5)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_input=True)

# ==============================================================================
# 6. APP PRINCIPALE (DASHBOARD, DIARIO, SISTEMA)
# ==============================================================================
def render_main_app():
    """Mostra l'interfaccia principale dopo l'onboarding."""
    
    # Barra di Navigazione
    nav = option_menu(
        None, ["Dashboard", "Diario Neurale", "Network", "Sistema"],
        icons=["cpu", "journal-text", "people", "gear"],
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"background-color": theme['card'], "padding": "0!important", "border-bottom": f"1px solid {theme['main']}22"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "color": theme['txt']},
            "nav-link-selected": {"background-color": theme['main'], "color": theme['bg'], "font-weight": "700"},
        }
    )

    if nav == "Dashboard":
        st.markdown(f"### <span style='color:{theme['main']}'>// DASHBOARD_NEURALE:</span> {st.session_state.user_profile['nick']}", unsafe_allow_input=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        
        with c1:
            st.markdown(f"**Profilo:** {st.session_state.user_profile['nome']}")
            st.markdown(f"**Età:** {st.session_state.user_profile['nascita']}")
            st.markdown(f"**Vibe AI:** {st.session_state.user_profile['vibe']}")
            st.success(f"Sistema: {st.session_state.current_theme} attivo.")

        with c2:
            # Grafico Radar Professionale
            up = st.session_state.user_profile
            categories = ['Socialità', 'Energia', 'Rischio']
            values = [up['social'], up['energy'], up['risk']]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values, theta=categories, fill='toself', 
                line=dict(color=theme['main'], width=3),
                fillcolor=f"{theme['main']}33"
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10], color="#888"), bgcolor="rgba(0,0,0,0)"),
                showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font_color=theme['txt'],
                margin=dict(l=40, r=40, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        with c3:
            st.markdown("**Obiettivi Correnti:**")
            st.info(up['obiettivi'])
            st.metric("Messaggi Loggati", len(st.session_state.chat_log))

    elif nav == "Diario Neurale":
        st.subheader("🖋️ Registro di Comunicazione")
        
        # Area Storico
        chat_container = st.container(height=500)
        with chat_container:
            if not st.session_state.chat_log:
                st.info("Nessun log trovato. Inizia la sincronizzazione neurale scrivendo qui sotto.")
            for m in st.session_state.chat_log:
                tipo = "chat-msg-user" if m["role"] == "user" else "chat-msg-ai"
                label = "UTENTE" if m["role"] == "user" else "SYNAPSE"
                st.markdown(f'<div class="{tipo}"><strong>[{label}]</strong><br>{m["content"]}</div>', unsafe_allow_input=True)

        # Chat Input
        if prompt := st.chat_input("Digita un pensiero..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            
            if model:
                up = st.session_state.user_profile
                # Prompt Engineering Complesso
                system_instruction = (
                    f"Sei Synapse OS, l'assistente neurale di {up['nick']}. "
                    f"Genere: {up['genere']}, Obiettivi: {up['obiettivi']}. "
                    f"Parametri: Socialità {up['social']}/10, Energia {up['energy']}/10, Rischio {up['risk']}/10. "
                    f"Stile comunicativo: {up['vibe']}. Rispondi in modo coerente."
                )
                
                with st.spinner("Processing..."):
                    try:
                        response = model.generate_content(f"{system_instruction}\nMessaggio Utente: {prompt}")
                        st.session_state.chat_log.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Errore di Sincronizzazione: {e}")
            st.rerun()

    elif nav == "Network":
        st.subheader("👥 Cerchio Sociale")
        st.write("Registra le persone chiave per permettere a Synapse di analizzare le tue interazioni.")
        
        with st.form("add_person"):
            col_p1, col_p2 = st.columns(2)
            p_nome = col_p1.text_input("Nome Persona")
            p_rel = col_p2.selectbox("Relazione", ["Famiglia", "Amico", "Lavoro", "Partner"])
            p_note = st.text_area("Note e dettagli importanti")
            if st.form_submit_button("AGGIUNGI AL NETWORK"):
                st.session_state.people_log.append({"nome": p_nome, "relazione": p_rel, "note": p_note})
                st.success("Soggetto aggiunto al database.")
        
        for p in st.session_state.people_log:
            with st.expander(f"{p['nome']} - {p['relazione']}"):
                st.write(p['note'])

    elif nav == "Sistema":
        st.subheader("⚙️ Impostazioni OS")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("### Estetica")
            nuovo_tema = st.selectbox("Cambia Tema", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.current_theme))
            if st.button("AGGIORNA TEMA"):
                st.session_state.current_theme = nuovo_tema
                st.rerun()

        with col_s2:
            st.markdown("### Dati e Privacy")
            if st.button("WIPE_SYSTEM (Reset Totale)"):
                st.session_state.user_profile = None
                st.session_state.onboarding_step = 1
                st.session_state.chat_log = []
                st.rerun()

# ==============================================================================
# 7. LOGICA DI ESECUZIONE (RUN)
# ==============================================================================
if st.session_state.user_profile is None:
    render_onboarding()
else:
    render_main_app()

# ==============================================================================
# FINE CODICE - SYNAPSE NEURAL OS v2.0
# ==============================================================================
