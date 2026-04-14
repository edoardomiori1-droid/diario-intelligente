"""
SYNAPSE NEURAL OS - NEURAL CHAT INTERFACE
-----------------------------------------
File 12/35 | pages/12_page_chat.py
Posizione: /pages/12_page_chat.py

DESCRIZIONE:
Interfaccia di dialogo tra l'operatore e l'intelligenza centrale.
Gestisce la visualizzazione dei messaggi e l'invio dei prompt.
"""

import streamlit as st

# Import moduli UI e Core
try:
    from ui.09_ui_sidebar import render_sidebar
    from ui.08_ui_components import section_header, info_badge
    from core.05_core_reset import soft_reset_chat
except ImportError:
    pass

def render_chat():
    """Rendering del modulo di conversazione."""
    
    # 1. SIDEBAR & HEADER
    render_sidebar()
    
    col_title, col_actions = st.columns([3, 1])
    with col_title:
        section_header("Neural Chat", icon="💬")
    with col_actions:
        if st.button("🧼 Pulisci Memoria"):
            soft_reset_chat()
            st.rerun()

    # 2. CONTENITORE MESSAGGI (Scrollable)
    # Visualizziamo lo storico salvato nel File 02
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"""
                <div style='background: rgba(0, 242, 255, 0.05); padding: 15px; border-radius: 10px; 
                border-right: 3px solid #00F2FF; margin: 10px 0 10px 50px; text-align: right;'>
                    <span style='color: #00F2FF; font-size: 0.8em;'>OPERATORE</span><br>{content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; 
                border-left: 3px solid #7000FF; margin: 10px 50px 10px 0;'>
                    <span style='color: #7000FF; font-size: 0.8em;'>SYNAPSE IA</span><br>{content}
                </div>
                """, unsafe_allow_html=True)

    # 3. AREA DI INPUT (Chat Bar)
    st.write("---")
    prompt = st.chat_input("Invia un comando o un pensiero alla rete...")

    if prompt:
        # Aggiungiamo il messaggio dell'utente alla memoria (File 02)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Simulazione risposta IA (In attesa del modulo Logic 15)
        # Qui potrai collegare l'API di Gemini
        response = f"Ricevuto, Operatore. Sto analizzando il tuo input: '{prompt}'. Sistema in attesa di integrazione API."
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Refresh per mostrare i nuovi messaggi
        st.rerun()

# Se il file viene chiamato direttamente (test)
if __name__ == "__main__":
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    render_chat()
