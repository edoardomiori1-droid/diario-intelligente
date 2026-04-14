"""
SYNAPSE NEURAL OS - SYSTEM LOG PROCESSOR
----------------------------------------
File 31/35 | core/31_core_logs.py
Posizione: /core/31_core_logs.py

DESCRIZIONE:
Gestisce la registrazione degli eventi di sistema. 
Essenziale per il debug e per monitorare l'attività dell'IA.
"""

import streamlit as st
from datetime import datetime

def add_log(event, level="INFO"):
    """
    Aggiunge un evento alla cronologia di sistema.
    Levels: INFO, WARNING, ERROR, AI_SYNC
    """
    if 'internal_logs' not in st.session_state:
        st.session_state.internal_logs = []
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = {
        "time": timestamp,
        "event": event,
        "level": level
    }
    
    # Manteniamo solo gli ultimi 50 log per non pesare sulla memoria
    st.session_state.internal_logs.insert(0, log_entry)
    if len(st.session_state.internal_logs) > 50:
        st.session_state.internal_logs.pop()

def render_log_viewer():
    """Visualizzatore grafico dei log per il pannello Settings."""
    st.subheader("🛠️ System Terminal Output")
    
    log_text = ""
    for log in st.session_state.get('internal_logs', []):
        color = "#00F2FF" # Cyan per INFO
        if log['level'] == "ERROR": color = "#FF4B4B"
        if log['level'] == "WARNING": color = "#FFCC00"
        if log['level'] == "AI_SYNC": color = "#BB86FC"
        
        log_text += f"<span style='color:{color};'>[{log['time']}] {log['level']}:</span> {log['event']}<br>"
    
    st.markdown(f"""
        <div style="background-color: #0e1117; padding: 15px; border-radius: 5px; 
                    font-family: 'Courier New', monospace; font-size: 0.8em; 
                    height: 300px; overflow-y: auto; border: 1px solid #333;">
            {log_text if log_text else 'Nessun log registrato.'}
        </div>
    """, unsafe_allow_html=True)

def clear_logs():
    """Pulisce la cronologia log."""
    st.session_state.internal_logs = []
