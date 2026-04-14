import streamlit as st
from streamlit_option_menu import option_menu
import datetime

# --- CONFIGURAZIONE ESTETICA ---
st.set_page_config(page_title="Synapse AI", page_icon="🧠", layout="wide")

# CSS per rendere l'app bella su mobile con la barra in basso
st.markdown("""
    <style>
    .stApp { margin-bottom: 60px; }
    [data-testid="stSidebar"] { display: none; } /* Nasconde sidebar standard */
    .nav-link { border-radius: 10px !important; }
    </style>
""", unsafe_allow_input=True)

# --- INIZIALIZZAZIONE SESSIONE ---
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

# --- 1. SCHERMATA ONBOARDING (CONFIGURAZIONE INIZIALE) ---
def show_onboarding():
    st.title("Benvenuto su Synapse ✨")
    st.write("Configura il tuo profilo universale. L'AI userà questi dati per personalizzare ogni risposta.")
    
    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome e Cognome completi")
            nick = st.text_input("Come vuoi essere chiamato?")
            nascita = st.date_input("Data di nascita", min_value=datetime.date(1950, 1, 1))
        with col2:
            lingua = st.selectbox("Lingua", ["Italiano", "English", "Español"])
            tema = st.select_slider("Tema preferito", ["Minimal", "Cyberpunk", "Ocean", "Sunset"])
            colore_guida = st.color_picker("Colore principale dell'interfaccia", "#00FFAA")

        st.divider()
        st.subheader("Dati Personali & Obiettivi")
        sport = st.text_input("Quali sport pratichi?")
        obiettivi = st.text_area("Quali sono i tuoi obiettivi di vita principali?")
        
        st.write("---")
        st.write("### Valutazione Iniziale (1-5)")
        v1 = st.slider("Quanto sei soddisfatto della tua forma fisica?", 1, 5, 3)
        v2 = st.slider("Quanto ti senti stressato ultimamente?", 1, 5, 3)
        v3 = st.slider("Quanto sei costante nei tuoi impegni?", 1, 5, 3)

        if st.form_submit_button("Salva Profilo e Inizia"):
            st.session_state.user_profile = {
                "nome": nome, "nick": nick, "nascita": nascita, "lingua": lingua,
                "tema": tema, "colore": colore_guida, "sport": sport, 
                "obiettivi": obiettivi, "ratings": [v1, v2, v3]
            }
            st.rerun()

# --- 2. L'APPLICAZIONE PRINCIPALE ---
def show_main_app():
    # BARRA DI NAVIGAZIONE INFERIORE (Universale PC/Mobile)
    selected = option_menu(
        menu_title=None,
        options=["Diario", "Calendario", "Persone", "Profilo"],
        icons=["chat-right-dots", "calendar3", "people", "person-vcard"],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#111"},
            "icon": {"color": st.session_state.user_profile['colore'], "font-size": "20px"}, 
            "nav-link-selected": {"background-color": "#333"},
        }
    )

    if selected == "Diario":
        st.header(f"Ciao {st.session_state.user_profile['nick']} 👋")
        st.write("Usa la chat per raccontare la tua giornata. Alla fine genererò un resoconto automatico.")
        
        # Area Chat
        for m in st.session_state.chat_log:
            with st.chat_message(m["role"]):
                st.write(m["content"])

        if prompt := st.chat_input("Raccontami tutto..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            st.rerun()

        if st.button("✨ Genera riassunto e salva giornata"):
            # Qui domani inseriremo il comando per Gemini
            st.success("Riassunto creato! (In attesa di collegamento API)")

    elif selected == "Profilo":
        st.title("Il tuo Profilo Universale")
        st.write(f"**Nome:** {st.session_state.user_profile['nome']}")
        st.write(f"**Sport:** {st.session_state.user_profile['sport']}")
        st.write(f"**Obiettivi:** {st.session_state.user_profile['obiettivi']}")
        if st.button("Reset Profilo"):
            st.session_state.user_profile = None
            st.rerun()

# --- LOGICA DI AVVIO ---
if st.session_state.user_profile is None:
    show_onboarding()
else:
    show_main_app()
