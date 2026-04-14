import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import google.generativeai as genai

# --- 1. CONFIGURAZIONE API GEMINI ---
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        api_funzionante = True
    except Exception as e:
        st.error(f"Errore API: {e}")
        api_funzionante = False
else:
    st.warning("Chiave API non trovata nei Secrets!")
    api_funzionante = False

# --- 2. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Synapse AI", page_icon="🧠")

# Inizializzazione sessione
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

# --- 3. SCHERMATA ONBOARDING ---
def show_onboarding():
    st.title("Benvenuto su Synapse ✨")
    with st.form("onboarding_form"):
        nome = st.text_input("Nome completo")
        nick = st.text_input("Nickname")
        obiettivi = st.text_area("I tuoi obiettivi principali")
        if st.form_submit_button("Inizia"):
            st.session_state.user_profile = {"nome": nome, "nick": nick, "obiettivi": obiettivi}
            st.rerun()

# --- 4. APPLICAZIONE PRINCIPALE ---
def show_main_app():
    # Barra di navigazione semplice
    selected = option_menu(
        menu_title=None,
        options=["Diario", "Profilo"],
        icons=["chat", "person"],
        orientation="horizontal"
    )

    if selected == "Diario":
        st.header(f"Ciao {st.session_state.user_profile['nick']} 👋")
        
        # Area messaggi
        for m in st.session_state.chat_log:
            with st.chat_message(m["role"]):
                st.write(m["content"])

        if prompt := st.chat_input("Raccontami la tua giornata..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            
            if api_funzionante:
                context = f"Sei l'assistente di {st.session_state.user_profile['nick']}. Obiettivi: {st.session_state.user_profile['obiettivi']}."
                response = model.generate_content(f"{context}\nUtente: {prompt}")
                st.session_state.chat_log.append({"role": "assistant", "content": response.text})
            else:
                st.session_state.chat_log.append({"role": "assistant", "content": "L'API non è configurata, non posso rispondere!"})
            st.rerun()

    elif selected == "Profilo":
        st.write(st.session_state.user_profile)
        if st.button("Reset Profilo"):
            st.session_state.user_profile = None
            st.rerun()

# Avvio
if st.session_state.user_profile is None:
    show_onboarding()
else:
    show_main_app()
