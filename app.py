import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
from ui_styles import apply_synapse_ui, THEMES

# 1. INIT RIGIDO
if 'initialized' not in st.session_state:
    st.set_page_config(page_title="Synapse OS", layout="wide")
    st.session_state.update({
        'initialized': True,
        'user_profile': None,
        'chat_log': [],
        'current_theme': "Cyber Matrix",
        'onboarding_step': 1,
        'temp_data': {}
    })

# 2. MOTORE AI ROBUSTO
def ask_synapse(prompt):
    # Cerchiamo la chiave sia nei secrets che nel session state per sicurezza
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "ERRORE: Chiave API non trovata nei Secrets di Streamlit."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        u = st.session_state.user_profile
        # Creiamo un contesto più forte
        context = f"Sei Synapse OS, l'assistente di {u['nick']}. Il suo obiettivo è: {u['goals']}. Rispondi in modo tecnico e motivante."
        response = model.generate_content(f"{context}\n\nUtente: {prompt}")
        return response.text
    except Exception as e:
        return f"Sincronizzazione Fallita: {str(e)}"

# 3. LOGICA UI
def main():
    apply_synapse_ui(st.session_state.current_theme)

    if st.session_state.user_profile is None:
        # ONBOARDING (Basato sullo stile che ti è piaciuto)
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.markdown('<p class="os-title">SYNAPSE_INIT</p>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            step = st.session_state.onboarding_step
            
            if step == 1:
                st.subheader("🧬 IDENTITÀ")
                nome = st.text_input("Nome e Cognome", key="reg_nome")
                nick = st.text_input("Nickname", key="reg_nick")
                if st.button("PROSEGUI"):
                    if nome and nick:
                        st.session_state.temp_data.update({"nome": nome, "nick": nick})
                        st.session_state.onboarding_step = 2
                        st.rerun()
            
            elif step == 2:
                st.subheader("🎨 INTERFACCIA")
                tema = st.selectbox("Seleziona Tema", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.current_theme))
                st.session_state.current_theme = tema
                goals = st.text_area("Obiettivo Primario", key="reg_goals")
                if st.button("ATTIVA SISTEMA"):
                    if goals:
                        st.session_state.temp_data["goals"] = goals
                        st.session_state.user_profile = st.session_state.temp_data
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # MAIN APP
        t = THEMES[st.session_state.current_theme]
        selected = option_menu(None, ["Dashboard", "Diario", "Sistema"], 
                              icons=["grid", "cpu", "gear"], 
                              orientation="horizontal",
                              styles={"container": {"background": t['card']}, "nav-link-selected": {"background": t['main'], "color": t['bg']}})

        if selected == "Dashboard":
            st.markdown(f'<p class="os-title">{st.session_state.user_profile["nick"]}_CORE</p>', unsafe_allow_html=True)
            st.info(f"Focus Attivo: {st.session_state.user_profile['goals']}")

        elif selected == "Diario":
            # Container per i messaggi
            chat_container = st.container()
            with chat_container:
                for m in st.session_state.chat_log:
                    cls = "user-msg" if m["role"] == "user" else "ai-msg"
                    st.markdown(f'<div class="{cls}">{m["content"]}</div>', unsafe_allow_html=True)
            
            if p := st.chat_input("Inserisci log..."):
                st.session_state.chat_log.append({"role": "user", "content": p})
                with st.spinner("Analisi neurale..."):
                    res = ask_synapse(p)
                    st.session_state.chat_log.append({"role": "assistant", "content": res})
                st.rerun()

        elif selected == "Sistema":
            st.button("REBOOT SISTEMA", on_click=lambda: st.session_state.update({'user_profile': None, 'onboarding_step': 1}))

if __name__ == "__main__":
    main()
