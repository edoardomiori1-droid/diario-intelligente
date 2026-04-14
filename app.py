import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# --- 1. CONFIGURAZIONE API ---
api_funzionante = False
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Usiamo 'gemini-1.5-flash' ma con una configurazione di sicurezza
        model = genai.GenerativeModel('gemini-1.5-flash')
        api_funzionante = True
    except Exception as e:
        st.error(f"Errore API: {e}")
else:
    st.warning("Chiave API mancante nei Secrets!")

# --- 2. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Synapse AI", page_icon="🧠")

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

# --- 3. LOGICA ONBOARDING ---
if st.session_state.user_profile is None:
    st.title("Benvenuto su Synapse ✨")
    with st.form("onboarding"):
        nome = st.text_input("Nome completo")
        nick = st.text_input("Nickname")
        obiettivi = st.text_area("I tuoi obiettivi")
        if st.form_submit_button("Inizia"):
            st.session_state.user_profile = {"nome": nome, "nick": nick, "obiettivi": obiettivi}
            st.rerun()
else:
    # --- 4. APP PRINCIPALE ---
    selected = option_menu(None, ["Diario", "Profilo"], icons=["chat", "person"], orientation="horizontal")

    if selected == "Diario":
        st.header(f"Ciao {st.session_state.user_profile['nick']} 👋")
        
        # Area Chat
        for m in st.session_state.chat_log:
            with st.chat_message(m["role"]):
                st.write(m["content"])

        if prompt := st.chat_input("Raccontami la tua giornata..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            
            if api_funzionante:
                try:
                    # Chiamata diretta senza fronzoli per testare il collegamento
                    response = model.generate_content(prompt)
                    st.session_state.chat_log.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Errore durante la risposta: {e}")
            else:
                st.error("L'API non è configurata correttamente.")
            st.rerun()

    elif selected == "Profilo":
        st.json(st.session_state.user_profile)
        if st.button("Reset Profilo"):
            st.session_state.user_profile = None
            st.rerun()
