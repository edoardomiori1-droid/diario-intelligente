"""
SYNAPSE NEURAL OS - LIFE TRACKER
--------------------------------
File 21/35 | tools/21_tool_tracker.py
Posizione: /tools/21_tool_tracker.py

DESCRIZIONE:
Monitoraggio delle abitudini quotidiane e degli obiettivi rapidi.
Calcola un punteggio di efficienza basato sui task completati.
"""

import streamlit as st
from ui.08_ui_components import section_header, glass_card

def render_tracker():
    """Rendering dell'interfaccia Life Tracker."""
    section_header("Life Tracker", icon="📊")
    
    # Inizializzazione obiettivi se non presenti
    if 'daily_tasks' not in st.session_state:
        st.session_state.daily_tasks = [
            {"task": "Idratazione ottimale", "done": False},
            {"task": "Sessione Deep Work", "done": False},
            {"task": "Allenamento fisico", "done": False},
            {"task": "Lettura / Studio", "done": False},
            {"task": "Meditazione / Focus", "done": False}
        ]

    col_tasks, col_stats = st.columns([2, 1])

    with col_tasks:
        st.write("Protocolli Giornalieri:")
        for i, item in enumerate(st.session_state.daily_tasks):
            # Checkbox stilizzate (Streamlit standard con logica OS)
            st.session_state.daily_tasks[i]['done'] = st.checkbox(
                item['task'], 
                value=item['done'], 
                key=f"task_{i}"
            )
        
        if st.button("♻️ RESET PROTOCOLLI (Nuovo Giorno)"):
            for item in st.session_state.daily_tasks:
                item['done'] = False
            st.rerun()

    with col_stats:
        # Calcolo efficienza
        total = len(st.session_state.daily_tasks)
        completed = sum(1 for t in st.session_state.daily_tasks if t['done'])
        efficiency = int((completed / total) * 100)
        
        # Visualizzazione Grafica
        st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #00F2FF;'>
                <p style='font-size: 0.8em; color: #00F2FF;'>EFFICIENZA OPERATIVA</p>
                <h1 style='margin: 0; color: white;'>{efficiency}%</h1>
                <div style='background: #111; border-radius: 10px; height: 10px; margin-top: 15px;'>
                    <div style='background: #00F2FF; width: {efficiency}%; height: 10px; border-radius: 10px; box-shadow: 0px 0px 10px #00F2FF;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        glass_card("Status", "Completa i protocolli per mantenere l'uplink stabile.")
