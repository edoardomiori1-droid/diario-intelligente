import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import plotly.graph_objects as go
from ui_styles import apply_synapse_ui, THEMES
from datetime import datetime

# CONFIGURAZIONE INIZIALE - Deve essere la prima istruzione
if 'page_init' not in st.session_state:
    st.set_page_config(page_title="Synapse OS", layout="wide")
    st.session_state.update({
        'page_init': True,
        'user_profile': None,
        'chat_log': [],
        'current_theme': "Cyber Matrix",
        'onboarding_step': 1,
        'temp_data': {}
    })

def ask_synapse(prompt):
    if "GEMINI_API_KEY" not in st.secrets:
        return "Errore API Key."
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        u = st.session_state.user_profile
        context = f"Sei Synapse OS. Utente: {u['nick']}. Obiettivi: {u['obiettivi']}."
        return model.generate_content(f"{context}\n\n{prompt}").text
    except:
        return "Errore di connessione."

def show_onboarding():
    # Sicurezza: controlla che il tema esista
    theme_to_apply = st.session_state.get('current_theme', 'Cyber Matrix')
    apply_synapse_ui(theme_to_apply)
    
    st.markdown('<div class="os-title">SYNAPSE_INIT</div>', unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        step = st.session_state.onboarding_step
        
        if step == 1:
            n = st.text_input("Nome")
            ni = st.text_input("Nick")
            if st.button("PROSEGUI"):
                if n and ni:
                    st.session_state.temp_data.update({"nome": n, "nick": ni})
                    st.session_state.onboarding_step = 2
                    st.rerun()
        
        elif step == 2:
            s = st.slider("Socialità", 1, 10, 5)
            e = st.slider("Energia", 1, 10, 5)
            if st.button("PROSEGUI"):
                st.session_state.temp_data.update({"social": s, "energy": e})
                st.session_state.onboarding_step = 3
                st.rerun()
        
        elif step == 3:
            tema = st.selectbox("Tema", list(THEMES.keys()))
            st.session_state.current_theme = tema
            obj = st.text_area("Obiettivo")
            if st.button("AVVIA"):
                st.session_state.temp_data["obiettivi"] = obj
                st.session_state.user_profile = st.session_state.temp_data
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def show_main():
    theme_to_apply = st.session_state.get('current_theme', 'Cyber Matrix')
    apply_synapse_ui(theme_to_apply)
    t = THEMES[theme_to_apply]
    
    selected = option_menu(None, ["Dashboard", "Diario", "Sistema"], 
                          orientation="horizontal",
                          styles={"container": {"background": t['card']}, "nav-link-selected": {"background": t['main'], "color": t['bg']}})

    if selected == "Dashboard":
        st.write(f"### Synapse OS v1.0 - Utente: {st.session_state.user_profile['nick']}")
        st.info(f"Focus: {st.session_state.user_profile['obiettivi']}")

    elif selected == "Diario":
        for m in st.session_state.chat_log:
            div = "user-msg" if m["role"] == "user" else "ai-msg"
            st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)
        
        if p := st.chat_input("Log..."):
            st.session_state.chat_log.append({"role": "user", "content": p})
            st.session_state.chat_log.append({"role": "assistant", "content": ask_synapse(p)})
            st.rerun()

    elif selected == "Sistema":
        if st.button("RESET"):
            st.session_state.user_profile = None
            st.session_state.onboarding_step = 1
            st.rerun()

if st.session_state.user_profile is None:
    show_onboarding()
else:
    show_main()
