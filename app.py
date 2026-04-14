import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import json

# ==============================================================================
# 1. DESIGN SYSTEM - 10 PACCHETTI CROMATICI PROFESSIONALI
# ==============================================================================
# Ogni pacchetto definisce l'intera identità visiva del sistema
THEMES = {
    "Cyber Matrix": {
        "main": "#00FF41", "sec": "#008F11", "bg": "#0D0D0D", 
        "card": "#1A1A1A", "txt": "#E0E0E0", "sidebar": "#000000", "accent": "#00FF41"
    },
    "Synthetic Sunset": {
        "main": "#FF8C00", "sec": "#FF0080", "bg": "#120D16", 
        "card": "#1D1625", "txt": "#F5F5F5", "sidebar": "#120D16", "accent": "#FF8C00"
    },
    "Deep Space": {
        "main": "#00FFFF", "sec": "#007FFF", "bg": "#050A10", 
        "card": "#0F1720", "txt": "#E0F7FA", "sidebar": "#050A10", "accent": "#00FFFF"
    },
    "Crimson Fury": {
        "main": "#FF0000", "sec": "#8B0000", "bg": "#0F0F0F", 
        "card": "#1C1C1C", "txt": "#FFFFFF", "sidebar": "#000000", "accent": "#FF0000"
    },
    "Arctic Frost": {
        "main": "#74EBD5", "sec": "#9FACE6", "bg": "#F0F4F8", 
        "card": "#FFFFFF", "txt": "#2C3E50", "sidebar": "#E0E7FF", "accent": "#74EBD5"
    },
    "Royal Amethyst": {
        "main": "#FF00FF", "sec": "#7000FF", "bg": "#0A0510", 
        "card": "#160D25", "txt": "#FDF0FF", "sidebar": "#0A0510", "accent": "#FF00FF"
    },
    "Forest Guard": {
        "main": "#C2B280", "sec": "#4F7942", "bg": "#0D110D", 
        "card": "#161D16", "txt": "#ECECEC", "sidebar": "#0D110D", "accent": "#C2B280"
    },
    "Midnight Gold": {
        "main": "#D4AF37", "sec": "#996515", "bg": "#0A0A0A", 
        "card": "#141414", "txt": "#F4F4F4", "sidebar": "#000000", "accent": "#D4AF37"
    },
    "Tokyo Drift": {
        "main": "#FF69B4", "sec": "#00FFFF", "bg": "#0F0510", 
        "card": "#1A0D1D", "txt": "#FFFFFF", "sidebar": "#0F0510", "accent": "#FF69B4"
    },
    "Carbon Fiber": {
        "main": "#FFFFFF", "sec": "#555555", "bg": "#0A0A0A", 
        "card": "#1A1A1A", "txt": "#F0F0F0", "sidebar": "#000000", "accent": "#FFFFFF"
    }
}

# ==============================================================================
# 2. CORE INITIALIZATION & SESSION MANAGEMENT
# ==============================================================================
st.set_page_config(
    page_title="Synapse Neural OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def init_os():
    """Inizializza tutte le variabili di stato per prevenire errori di ricarica."""
    defaults = {
        'initialized': True,
        'user_profile': None,
        'chat_log': [],
        'current_theme': "Cyber Matrix",
        'onboarding_step': 1,
        'temp_data': {},
        'people_log': [],
        'system_logs': [f"OS Booted at {datetime.now().strftime('%H:%M:%S')}"],
        'session_start': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_os()

# ==============================================================================
# 3. ADVANCED CSS UI ENGINE
# ==============================================================================
def inject_ui(theme_key):
    """Genera e inietta il codice CSS basato sul tema attivo."""
    t = THEMES.get(theme_key, THEMES["Cyber Matrix"])
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');
        
        /* Global Background */
        .stApp {{
            background-color: {t['bg']};
            color: {t['txt']};
            font-family: 'Inter', sans-serif;
        }}

        /* Header Styling */
        .os-header {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 3.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, {t['main']}, {t['sec']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            letter-spacing: -4px;
            margin-bottom: 5px;
            filter: drop-shadow(0 0 12px {t['main']}33);
        }}

        /* Glassmorphism Cards */
        .glass-card {{
            background: {t['card']};
            border: 1px solid {t['main']}22;
            border-radius: 24px;
            padding: 45px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            margin-bottom: 20px;
        }}

        /* Customized Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {t['sidebar']};
            border-right: 1px solid {t['main']}11;
        }}

        /* Chat UI */
        .chat-bubble-user {{
            background: {t['card']};
            border: 1px solid {t['main']}44;
            border-right: 4px solid {t['main']};
            padding: 18px;
            border-radius: 18px 0 18px 18px;
            margin: 12px 0;
            margin-left: 20%;
            font-size: 0.95rem;
        }}
        .chat-bubble-ai {{
            background: {t['card']};
            border: 1px solid {t['sec']}44;
            border-left: 4px solid {t['sec']};
            padding: 18px;
            border-radius: 0 18px 18px 18px;
            margin: 12px 0;
            margin-right: 20%;
            color: {t['txt']};
            font-size: 0.95rem;
        }}

        /* Inputs & Forms */
        .stTextInput input, .stTextArea textarea, .stSelectbox div {{
            background-color: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid {t['main']}33 !important;
            color: white !important;
            border-radius: 12px !important;
        }}

        /* Cyber Buttons */
        .stButton button {{
            width: 100%;
            background: linear-gradient(135deg, {t['main']}, {t['sec']}) !important;
            color: {t['bg']} !important;
            font-weight: 800 !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 18px !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .stButton button:hover {{
            transform: scale(1.03) translateY(-2px);
            box-shadow: 0 15px 30px {t['main']}55;
        }}

        /* Scrollbar */
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: {t['bg']}; }}
        ::-webkit-scrollbar-thumb {{ background: {t['main']}44; border-radius: 10px; }}
        </style>
    """, unsafe_allow_input=True)

# ==============================================================================
# 4. NEURAL INTELLIGENCE CORE
# ==============================================================================
def call_synapse_brain(user_input):
    """Gestisce la comunicazione con l'API Gemini incorporando il contesto utente."""
    if "GEMINI_API_KEY" not in st.secrets:
        return "ERROR: API KEY NOT FOUND NEI SECRETS."
    
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        up = st.session_state.user_profile
        # Engineering del prompt basato sui dati dell'onboarding
        system_context = f"""
        PROFILO UTENTE SYNAPSE OS:
        - Nome: {up['nome']} (Alias: {up['nick']})
        - Età: {up['nascita']} | Genere: {up['genere']}
        - Matrice Neurale: Socialità {up['social']}/10, Energia {up['energy']}/10, Rischio {up['risk']}/10
        - Tono Richiesto: {up['vibe']}
        - Obiettivo Focus: {up['obiettivi']}
        
        ISTRUZIONI: Rispondi come un'entità digitale evoluta chiamata Synapse. 
        Sii conciso, preciso e adatta il linguaggio al 'Tono Richiesto'.
        """
        
        response = model.generate_content(f"{system_context}\n\nINPUT_UTENTE: {user_input}")
        return response.text
    except Exception as e:
        st.session_state.system_logs.append(f"AI_CRASH: {str(e)}")
        return f"Sincronizzazione fallita. Errore loggato nel sistema."

# ==============================================================================
# 5. ONBOARDING SEQUENCE (THE MODULES)
# ==============================================================================
def run_onboarding():
    """Schermate di configurazione iniziale."""
    inject_ui(st.session_state.current_theme)
    st.markdown('<p class="os-header">SYNAPSE_OS</p>', unsafe_allow_input=True)
    
    _, container, _ = st.columns([1, 2, 1])
    
    with container:
        st.markdown('<div class="glass-card">', unsafe_allow_input=True)
        step = st.session_state.onboarding_step
        
        # Header Modulo
        st.write(f"📂 **SISTEMA_INIT_STEP: {step}/3**")
        st.progress(step / 3)

        if step == 1:
            st.subheader("🧬 Modulo I: Identità Biometrica")
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input("Nome Legale")
                nick = st.text_input("Alias di Sistema")
            with c2:
                data_n = st.date_input("Ciclo di Nascita", value=datetime(2000, 1, 1))
                gen = st.selectbox("Genere", ["Maschile", "Femminile", "Non-Binario", "Cyborg/Altro"])
            
            if st.button("PROSSIMA FASE >>"):
                if nome and nick:
                    st.session_state.temp_data.update({"nome": nome, "nick": nick, "nascita": str(data_n), "genere": gen})
                    st.session_state.onboarding_step = 2
                    st.rerun()
                else:
                    st.error("Dati insufficienti per l'inizializzazione.")

        elif step == 2:
            st.subheader("📡 Modulo II: Matrice Comportamentale")
            st.info("Questi valori influenzeranno l'analisi dei dati e il tono dell'AI.")
            
            s = st.select_slider("Indice di Socialità", range(1, 11), 5)
            e = st.select_slider("Livello Energetico Base", range(1, 11), 5)
            r = st.select_slider("Propensione al Rischio/Novità", range(1, 11), 5)
            
            v = st.radio("Scegli lo Stile di Comunicazione:", 
                        ["Diretto e Onesto", "Gentile e Empatico", "Ironico e Tagliente", "Scientifico e Freddo"])
            
            if st.button("CONFIGURA ESTETICA >>"):
                st.session_state.temp_data.update({"social": s, "energy": e, "risk": r, "vibe": v})
                st.session_state.onboarding_step = 3
                st.rerun()

        elif step == 3:
            st.subheader("🎨 Modulo III: Personalizzazione OS")
            tema = st.selectbox("Pacchetto Colori Interfaccia", list(THEMES.keys()))
            
            # Anteprima dinamica del tema
            if tema != st.session_state.current_theme:
                st.session_state.current_theme = tema
                st.rerun()
                
            obj = st.text_area("Cosa vuoi ottimizzare nella tua vita?", 
                              placeholder="Es: Bilanciamento tra allenamento e studio, gestione ansia sociale...")
            
            if st.button("AVVIA PROTOCOLLO SYNAPSE"):
                st.session_state.temp_data.update({"obiettivi": obj})
                st.session_state.user_profile = st.session_state.temp_data
                st.session_state.system_logs.append("User Profile Created Successfully.")
                st.balloons()
                time.sleep(1.2)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_input=True)

# ==============================================================================
# 6. MAIN APPLICATION HUB
# ==============================================================================
def run_main_app():
    """L'app principale dopo il login."""
    inject_ui(st.session_state.current_theme)
    t = THEMES[st.session_state.current_theme]
    
    # Navigation Bar
    menu = option_menu(
        None, ["Modulo Analisi", "Diario Neurale", "Network", "OS Settings"],
        icons=["activity", "cpu-fill", "people-fill", "terminal"],
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"background-color": t['card'], "border": f"1px solid {t['main']}22", "padding": "0!important"},
            "nav-link-selected": {"background-color": t['main'], "color": t['bg'], "font-weight": "bold"}
        }
    )

    if menu == "Modulo Analisi":
        st.markdown(f"### <span style='color:{t['main']}'>// NEURAL_DASHBOARD:</span> {st.session_state.user_profile['nick']}", unsafe_allow_input=True)
        
        c1, c2, c3 = st.columns([1.2, 2, 1])
        with c1:
            st.markdown('<div class="glass-card" style="padding:25px">', unsafe_allow_input=True)
            st.write("**PROFILO BIOMETRICO**")
            st.write(f"👤 {st.session_state.user_profile['nome']}")
            st.write(f"🎂 {st.session_state.user_profile['nascita']}")
            st.write(f"🎭 {st.session_state.user_profile['vibe']}")
            st.markdown('</div>', unsafe_allow_input=True)
            
            st.metric("Log Sessione", len(st.session_state.chat_log))

        with c2:
            # Radar Chart Plotly
            up = st.session_state.user_profile
            fig = go.Figure(data=go.Scatterpolar(
                r=[up['social'], up['energy'], up['risk']],
                theta=['Socialità', 'Energia', 'Rischio'],
                fill='toself', line_color=t['main'], fillcolor=f"{t['main']}22"
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10], color="#555"), bgcolor="rgba(0,0,0,0)"),
                showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font_color="white",
                margin=dict(l=40, r=40, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        with c3:
            st.write("**TARGET_FOCUS:**")
            st.info(up['obiettivi'])
            if st.button("Modifica Focus"):
                st.toast("Funzione in arrivo!")

    elif menu == "Diario Neurale":
        st.subheader("Registro delle Sincronizzazioni")
        
        # Chat History Display
        chat_area = st.container(height=500)
        with chat_area:
            if not st.session_state.chat_log:
                st.write("_Nessun log presente nel database. Inizia la prima comunicazione._")
            for m in st.session_state.chat_log:
                css_class = "chat-bubble-user" if m["role"] == "user" else "chat-bubble-ai"
                st.markdown(f'<div class="{css_class}">{m["content"]}</div>', unsafe_allow_input=True)

        # Chat Input logic
        if p := st.chat_input("Inserisci log neurale..."):
            st.session_state.chat_log.append({"role": "user", "content": p})
            with st.spinner("Synapse sta elaborando..."):
                response = call_synapse_brain(p)
                st.session_state.chat_log.append({"role": "assistant", "content": response})
            st.rerun()

    elif menu == "Network":
        st.subheader("Gestione Cerchio Sociale")
        with st.expander("Aggiungi Persona al Database"):
            with st.form("add_p"):
                pn = st.text_input("Nome")
                pr = st.selectbox("Relazione", ["Amico", "Partner", "Famiglia", "Lavoro", "Competitor"])
                nt = st.text_area("Note comportamentali")
                if st.form_submit_button("REGISTRA"):
                    st.session_state.people_log.append({"nome": pn, "rel": pr, "note": nt})
                    st.success(f"{pn} registrato.")
        
        for pe in st.session_state.people_log:
            st.write(f"👤 **{pe['nome']}** - ({pe['rel']})")

    elif menu == "OS Settings":
        st.subheader("Parametri di Sistema")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.write("**Interfaccia Visiva**")
            new_theme = st.selectbox("Switch Tema", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.current_theme))
            if st.button("Aggiorna Protocollo Colori"):
                st.session_state.current_theme = new_theme
                st.rerun()
        
        with col_s2:
            st.write("**Manutenzione**")
            if st.button("WIPE_ALL_DATA (Reset)"):
                st.session_state.user_profile = None
                st.session_state.onboarding_step = 1
                st.rerun()
            
            # Mostra i log tecnici
            with st.expander("Vedi System Logs"):
                for log in st.session_state.system_logs:
                    st.code(log)

# ==============================================================================
# 7. BOOT LOADER
# ==============================================================================
if st.session_state.user_profile is None:
    run_onboarding()
else:
    run_main_app()

# ==============================================================================
# FINE CODICE - SYNAPSE NEURAL OS v3.5
# ==============================================================================
