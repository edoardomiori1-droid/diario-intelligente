import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# --- CONFIGURAZIONE API ---
st.set_page_config(page_title="Synapse AI", page_icon="🧠")

def inizializza_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Chiave API non trovata nei Secrets di Streamlit!")
        return None
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Lista di modelli da provare in ordine di stabilità
    modelli_da_provare = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for nome_modello in modelli_da_provare:
        try:
            m = genai.GenerativeModel(nome_modello)
            # Test rapido per vedere se il modello risponde
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

# Carichiamo il modello una sola volta
if 'model' not in st.session_state:
    st.session_state.model = inizializza_ai()

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

# --- SCHERMATA LOGIN/ONBOARDING ---
if st.session_state.user_profile is None:
    st.title("Benvenuto su Synapse ✨")
    with st.form("onboarding"):
        nick = st.text_input("Come ti chiami?")
        obiettivi = st.text_area("Cosa vuoi migliorare nella tua vita?")
        if st.form_submit_button("Inizia il Viaggio"):
            if nick:
                st.session_state.user_profile = {"nick": nick, "obiettivi": obiettivi}
                st.rerun()
            else:
                st.warning("Inserisci almeno il tuo nome!")
else:
    # --- APP PRINCIPALE ---
    selected = option_menu(None, ["Diario", "Profilo"], 
        icons=["chat", "person"], orientation="horizontal")

    if selected == "Diario":
        st.header(f"Ciao {st.session_state.user_profile['nick']} 👋")
        
        # Area Chat
        for m in st.session_state.chat_log:
            with st.chat_message(m["role"]):
                st.write(m["content"])

        if prompt := st.chat_input("Raccontami la tua giornata..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            
            if st.session_state.model:
                try:
                    full_prompt = f"Sei l'assistente di {st.session_state.user_profile['nick']}. Obiettivi: {st.session_state.user_profile['obiettivi']}. Rispondi a: {prompt}"
                    response = st.session_state.model.generate_content(full_prompt)
                    st.session_state.chat_log.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Errore di risposta: {e}")
            else:
                st.error("L'AI non è riuscita a connettersi. Riprova tra 10 minuti o controlla la chiave API.")
            st.rerun()

    elif selected == "Profilo":
        st.write(f"**Nickname:** {st.session_state.user_profile['nick']}")
        st.write(f"**I tuoi Obiettivi:** {st.session_state.user_profile['obiettivi']}")
        if st.button("Reset Totale"):
            st.session_state.user_profile = None
            st.rerun()
