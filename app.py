import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import plotly.graph_objects as go
from ui_styles import apply_synapse_ui, THEMES
from datetime import datetime

# CONFIGURAZIONE INIZIALE
if 'page_init' not in st.session_state:
    st.set_page_config(page_title="Synapse OS", layout="wide", initial_sidebar_state="collapsed")
    st.session_state.update({
        'page_init': True,
        'user_profile': None,
        'chat_log': [],
        'current_theme': "Cyber Matrix",
        'onboarding_step': 1,
        'temp_data': {}
    })

# MOTORE AI
def ask_synapse(prompt):
    if "GEMINI_API_KEY" not in st.secrets:
        return "Errore: Configura la GEMINI_API_KEY nei Secrets di Streamlit Cloud."
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        u = st.session_state.user_profile
        context = f"Sei Synapse OS. Utente: {u['nick']}. Obiettivi: {u['obiettivi']}. Rispondi in modo sintetico e futuristico."
        return model.generate_content(f"{context}\n\n{prompt}").text
    except Exception as e:
        return f"Sincronizzazione Fallita: {str(e)}"

# SCHERMATA ONBOARDING
def show_onboarding():
    apply_synapse_ui(st.session_state.current_theme)
    st.markdown('<div class="os-title">SYNAPSE_INITIALIZATION</div>', unsafe_allow_input=True)
    
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_input=True)
        step = st.session_state.onboarding_step
        
        if step == 1:
            st.subheader("🧬 IDENTITÀ")
            n = st.text_input("Nome Legale")
            ni = st.text_input("Identificativo (Nick)")
            if st.button("PROSEGUI"):
                if n and ni:
                    st.session_state.temp_data.update({"nome": n, "nick": ni})
                    st.session_state.onboarding_step = 2
                    st.rerun()
        
        elif step == 2:
            st.subheader("📡 MATRICE")
            s = st.slider("Socialità", 1, 10, 5)
            e = st.slider("Energia", 1, 10, 5)
            if st.button("PROSEGUI"):
                st.session_state.temp_data.update({"social": s, "energy": e})
                st.session_state.onboarding_step = 3
                st.rerun()
        
        elif step == 3:
            st.subheader("🎨 INTERFACCIA")
            tema = st.selectbox("Pacchetto Colori", list(THEMES.keys()))
            st.session_state.current_theme = tema # Anteprima istantanea
            obj = st.text_area("Obiettivo Primario")
            if st.button("AVVIA SISTEMA"):
                st.session_state.temp_data["obiettivi"] = obj
                st.session_state.user_profile = st.session_state.temp_data
                st.rerun()
        st.markdown('</div>', unsafe_allow_input=True)

# SCHERMATA PRINCIPALE
def show_main():
    apply_synapse_ui(st.session_state.current_theme)
    t = THEMES[st.session_state.current_theme]
    
    selected = option_menu(None, ["Dashboard", "Diario", "Sistema"], 
                          icons=["grid-fill", "cpu-fill", "gear-fill"], 
                          menu_icon="cast", default_index=0, orientation="horizontal",
                          styles={"container": {"background": t['card']}, "nav-link-selected": {"background": t['main'], "color": t['bg']}})

    if selected == "Dashboard":
        st.markdown(f"### <span style='color:{t['main']}'>// BENVENUTO_</span> {st.session_state.user_profile['nick']}", unsafe_allow_input=True)
        u = st.session_state.user_profile
        fig = go.Figure(data=go.Scatterpolar(r=[u['social'], u['energy'], 5], theta=['Social', 'Energia', 'Focus'], fill='toself', line_color=t['main']))
        fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)", font_color="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    elif selected == "Diario":
        for m in st.session_state.chat_log:
            div_class = "user-msg" if m["role"] == "user" else "ai-msg"
            st.markdown(f'<div class="{div_class}">{m["content"]}</div>', unsafe_allow_input=True)
        
        if prompt := st.chat_input("Inserisci log neurale..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            with st.spinner("Processing..."):
                response = ask_synapse(prompt)
                st.session_state.chat_log.append({"role": "assistant", "content": response})
            st.rerun()

    elif selected == "Sistema":
        if st.button("REBOOT (Reset Dati)"):
            st.session_state.user_profile = None
            st.session_state.onboarding_step = 1
            st.rerun()

# LOGICA DI ESECUZIONE
if st.session_state.user_profile is None:
    show_onboarding()
else:
    show_main()
