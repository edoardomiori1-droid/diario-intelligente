import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import google.generativeai as genai

# --- CONFIGURAZIONE API GEMINI ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Configura la chiave API nei Secrets di Streamlit!")

# --- CONFIGURAZIONE ESTETICA ---
st.set_page_config(page_title="Synapse AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { margin-bottom: 60px; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_input=True)

# --- INIZIALIZZAZIONE SESSIONE ---
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

# --- 1. SCHERMATA ONBOARDING ---
def show_onboarding():
    st.title("Benvenuto su Synapse ✨")
    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome completo")
            nick = st.text_input("Nickname per l'AI")
        with col2:
            nascita = st.date_input("Data di nascita")
            colore = st.color_picker("Colore interfaccia", "#00FFAA")
        
        obiettivi = st.text_area("I tuoi obiettivi principali")
        
        if st.form_submit_button("Inizia"):
            st.session_state.user_profile = {
                "nome": nome, "nick": nick, "colore": colore, "obiettivi": obiettivi
            }
            st.rerun()

# --- 2. APPLICAZIONE PRINCIPALE ---
def show_main_app():
    selected = option_menu(
        menu_title=None,
        options=["Diario", "Calendario", "Persone", "Profilo"],
        icons=["chat-right-dots", "calendar3", "people", "person-vcard"],
        orientation="horizontal",
        styles={"icon": {"color": st.session_state.user_profile['colore']}}
    )

    if selected == "Diario":
        st.header(f"Ciao {st.session_state.user_profile['nick']} 👋")
        
        # Display messaggi
        for m in st.session_state.chat_log:
            with st.chat_message(m["role"]):
                st.write(m["content"])

        if prompt := st.chat_input("Raccontami la tua giornata..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            
            # Chiamata a Gemini
            context = f"Sei l'assistente di un diario intelligente. L'utente si chiama {st.session_state.user_profile['nick']} e i suoi obiettivi sono {st.session_state.user_profile['obiettivi']}."
            full_prompt = f"{context}\n\nUtente dice: {prompt}"
            
            response = model.generate_content(full_prompt)
            st.session_state.chat_log.append({"role": "assistant", "content": response.text})
            st.rerun()

    elif selected == "Profilo":
        st.title("Il tuo Profilo")
        st.write(st.session_state.user_profile)
        if st.button("Reset"):
            st.session_state.user_profile = None
            st.rerun()

# --- AVVIO ---
if st.session_state.user_profile is None:
    show_onboarding()
else:
    show_main_app()
