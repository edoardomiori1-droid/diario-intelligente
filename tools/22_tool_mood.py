"""
SYNAPSE NEURAL OS - MOOD TRACKER
--------------------------------
File 22/35 | tools/22_tool_mood.py
Posizione: /tools/22_tool_mood.py

DESCRIZIONE:
Registra lo stato emotivo giornaliero dell'operatore.
Genera una mappa cromatica del benessere interiore.
"""

import streamlit as st
from datetime import datetime
from ui.08_ui_components import section_header, glass_card

def render_mood_tracker():
    """Rendering dell'interfaccia Mood Tracker."""
    section_header("Bio-Feedback", icon="🧬")

    if 'mood_history' not in st.session_state:
        st.session_state.mood_history = {}

    today = datetime.now().strftime("%d/%m/%Y")

    col_input, col_view = st.columns([1, 1])

    with col_input:
        st.write("Sincronizzazione Stato Emotivo:")
        
        mood_options = {
            "ECCELLENTE (Uplink Totale)": {"color": "#00F2FF", "val": 5},
            "STABILE (Operativo)": {"color": "#00FFC8", "val": 4},
            "NEUTRO (In Attesa)": {"color": "#FFFFFF", "val": 3},
            "AFFATICATO (Buffer Pieno)": {"color": "#FFCC00", "val": 2},
            "CRITICO (Surriscaldamento)": {"color": "#FF4B4B", "val": 1}
        }

        choice = st.radio("Seleziona il tuo stato attuale:", list(mood_options.keys()))

        if st.button("REGISTRA STATO"):
            st.session_state.mood_history[today] = mood_options[choice]
            st.success(f"Stato del {today} registrato.")
            st.rerun()

    with col_view:
        st.write("Cronologia Recente:")
        if not st.session_state.mood_history:
            st.info("Nessun dato bio-metrico registrato.")
        else:
            for day, info in list(st.session_state.mood_history.items())[-5:]:
                st.markdown(f"""
                    <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                        <div style='width: 15px; height: 15px; background: {info['color']}; border-radius: 50%; margin-right: 15px; box-shadow: 0px 0px 5px {info['color']};'></div>
                        <span style='font-family: monospace; font-size: 0.9em;'>{day}: {info['val']}/5</span>
                    </div>
                """, unsafe_allow_html=True)

    st.divider()
    
    # Nota di analisi IA
    if today in st.session_state.mood_history:
        current_val = st.session_state.mood_history[today]['val']
        if current_val <= 2:
            glass_card("Diagnosi IA", "Rilevato stress elevato. Si consiglia attivazione Protocollo Focus (File 20) con sessione breve.", type="warning")
        elif current_val >= 4:
            glass_card("Diagnosi IA", "Stato ottimale rilevato. Momento perfetto per task ad alta intensità logica.", type="success")
