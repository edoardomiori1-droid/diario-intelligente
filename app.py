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
# 2. CORE INITIALIZATION
# ==============================================================================
if 'initialized' not in st.session_state:
    st.session_state.update({
        'initialized': True,
        'user_profile': None,
        'chat_log': [],
        'current_theme': "Cyber Matrix",
        'onboarding_step': 1,
        'temp_data': {},
        'people_log': [],
        'system_logs': [f"OS Booted at {datetime.now().strftime('%H:%M:%S')}"]
    })

# ==============================================================================
# 3. CSS UI ENGINE (FIXED TYPEERROR VERSION)
# ==============================================================================
def inject_ui(theme_key):
    """Gestione sicura del CSS per evitare TypeError con parentesi graffe."""
    t = THEMES.get(theme_key, THEMES["Cyber Matrix"])
    
    # Usiamo stringhe separate per evitare bug di parsing
    main_color = t['main']
    sec_color = t['sec']
    bg_color = t['bg']
    card_color = t['card']
    txt_color = t['txt']

    css_code = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {{ background-color: {bg_color}; color: {txt_color}; font-family: 'Inter', sans-serif; }}
    
    .os-header {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.5rem; font-weight: 800;
        background: linear-gradient(90deg, {main_color}, {sec_color});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 20px;
    }}

    .glass-card {{
        background: {card_color};
        border: 1px solid {main_color}33;
        border-radius: 20px; padding: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }}

    .chat-user {{
        background: {card_color}; border-right: 4px solid {main_color};
        padding: 15px; border-radius: 12px 0 12px 12px; margin: 10px 0 10px 20%;
    }}

    .chat-ai {{
        background: {card_color}; border-left: 4px solid {sec_color};
        padding: 15px; border-radius: 0 12px 12px 12px; margin: 10px 20% 10px 0;
    }}

    .stButton button {{
        background: linear-gradient(90deg, {main_color}, {sec_color}) !important;
        color: {bg_color} !important; font-weight: bold !important;
        border-radius: 12px !important; border: none !important;
        width: 100%; padding: 12px !important;
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_input=True)

# ==============================================================================
# 4. NEURAL BRAIN
# ==============================================================================
def call_synapse(prompt):
    if "GEMINI_API_KEY" not in st.secrets:
        return "CONFIG_ERROR: Manca la chiave API."
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        up = st.session_state.user_profile
        context = f"Sei Synapse. Utente: {up['nick']}. Tono: {up['vibe']}. Obiettivi: {up['obiettivi']}."
        resp = model.generate_content(f"{context}\n\nUtente: {prompt}")
        return resp.text
    except Exception as e:
        return f"Sincronizzazione fallita: {str(e)}"

# ==============================================================================
# 5. UI MODULES
# ==============================================================================
def run_onboarding():
    inject_ui(st.session_state.current_theme)
    st.markdown('<p class="os-header">SYNAPSE_OS</p>', unsafe_allow_input=True)
    
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_input=True)
        step = st.session_state.onboarding_step
        st.write(f"📂 **MODULO_INIT: {step}/3**")
        st.progress(step/3)

        if step == 1:
            st.subheader("🧬 Anagrafica")
            nome = st.text_input("Nome Cognome")
            nick = st.text_input("Nickname")
            data = st.date_input("Nascita", value=datetime(2000,1,1))
            gen = st.selectbox("Genere", ["M", "F", "Non-Binario", "Altro"])
            if st.button("AVANTI"):
                if nome and nick:
                    st.session_state.temp_data.update({"nome":nome, "nick":nick, "nascita":str(data), "genere":gen})
                    st.session_state.onboarding_step = 2
                    st.rerun()

        elif step == 2:
            st.subheader("📡 Calibrazione")
            s = st.slider("Socialità", 1, 10, 5)
            e = st.slider("Energia", 1, 10, 5)
            r = st.slider("Rischio", 1, 10, 5)
            v = st.radio("Vibe AI", ["Diretto", "Gentile", "Ironico", "Scientifico"])
            if st.button("AVANTI"):
                st.session_state.temp_data.update({"social":s, "energy":e, "risk":r, "vibe":v})
                st.session_state.onboarding_step = 3
                st.rerun()

        elif step == 3:
            st.subheader("🎨 Estetica")
            t = st.selectbox("Tema", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.current_theme))
            if t != st.session_state.current_theme:
                st.session_state.current_theme = t
                st.rerun()
            obj = st.text_area("Obiettivo")
            if st.button("FINISH"):
                st.session_state.temp_data["obiettivi"] = obj
                st.session_state.user_profile = st.session_state.temp_data
                st.rerun()
        st.markdown('</div>', unsafe_allow_input=True)

def run_main():
    inject_ui(st.session_state.current_theme)
    t = THEMES[st.session_state.current_theme]
    
    menu = option_menu(
        None, ["Analisi", "Diario", "Network", "OS"],
        icons=["activity", "cpu", "people", "gear"],
        orientation="horizontal",
        styles={"container": {"background": t['card']}, "nav-link-selected": {"background": t['main'], "color": t['bg']}}
    )

    if menu == "Analisi":
        st.markdown(f"### <span style='color:{t['main']}'>// NEURAL_DASHBOARD</span>", unsafe_allow_input=True)
        up = st.session_state.user_profile
        fig = go.Figure(data=go.Scatterpolar(
            r=[up['social'], up['energy'], up['risk']],
            theta=['Socialità', 'Energia', 'Rischio'],
            fill='toself', line_color=t['main']
        ))
        fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Diario":
        cont = st.container(height=400)
        with cont:
            for m in st.session_state.chat_log:
                cls = "chat-user" if m["role"] == "user" else "chat-ai"
                st.markdown(f'<div class="{cls}">{m["content"]}</div>', unsafe_allow_input=True)
        if p := st.chat_input("Scrivi..."):
            st.session_state.chat_log.append({"role": "user", "content": p})
            r = call_synapse(p)
            st.session_state.chat_log.append({"role": "assistant", "content": r})
            st.rerun()

    elif menu == "OS":
        st.subheader("Impostazioni")
        new_t = st.selectbox("Tema", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.current_theme))
        if st.button("Applica"):
            st.session_state.current_theme = new_t
            st.rerun()
        if st.button("RESET"):
            st.session_state.user_profile = None
            st.rerun()

# ==============================================================================
# 6. BOOT
# ==============================================================================
st.set_page_config(page_title="Synapse", layout="wide")

if st.session_state.user_profile is None:
    run_onboarding()
else:
    run_main()
