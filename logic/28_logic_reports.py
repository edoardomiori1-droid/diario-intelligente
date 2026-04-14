"""
SYNAPSE NEURAL OS - NEURAL REPORTING SYSTEM
-------------------------------------------
File 28/35 | logic/28_logic_reports.py
Posizione: /logic/28_logic_reports.py

DESCRIZIONE:
Analizza i dati raccolti nel tempo (Mood, Skill, Social) 
per generare resoconti narrativi tramite l'IA di Gemini.
"""

import streamlit as st
from datetime import datetime, timedelta

try:
    from logic.16_logic_api import get_neural_response
    from ui.08_ui_components import section_header, glass_card
except ImportError:
    pass

def generate_weekly_report():
    """
    Raccoglie i dati dell'ultima settimana e chiede a Gemini 
    di creare un resoconto analitico.
    """
    # 1. Recupero dati ultima settimana
    vault = st.session_state.get('vault_data', [])
    stats = st.session_state.get('user_profile', {}).get('stats', {})
    
    # Filtriamo solo le entrate "Diario" degli ultimi 7 giorni
    recent_entries = [n['content'] for n in vault if n['category'] == 'Diario'][:7]
    combined_text = "\n---\n".join(recent_entries)

    # 2. Costruzione del Prompt per Gemini
    report_prompt = f"""
    Agisci come l'analista di Synapse OS. Analizza i seguenti diari dell'ultima settimana:
    "{combined_text}"
    
    Le statistiche attuali dell'utente sono: {stats}.
    
    COMPITI:
    1. Crea un riassunto di 3 righe sulla settimana dell'operatore.
    2. Identifica il 'Sentiment Prevalente'.
    3. Suggerisci su quale area (Skill) concentrarsi la prossima settimana.
    4. Menziona eventuali persone ricorrenti e l'impatto che sembrano avere.
    """

    if st.button("GENERA REPORT SETTIMANALE"):
        with st.spinner("Sincronizzazione neurale in corso..."):
            report = get_neural_response(report_prompt)
            st.session_state.last_report = report
            st.rerun()

def render_reports_page():
    """Interfaccia per la visualizzazione dei resoconti."""
    section_header("Neural Reports", icon="📈")
    
    col_info, col_action = st.columns([2, 1])
    
    with col_info:
        st.write("In questa sezione puoi generare analisi profonde basate sulla tua cronologia.")
        if 'last_report' in st.session_state:
            glass_card("Resoconto Recente", st.session_state.last_report)
        else:
            st.info("Nessun report generato per questo ciclo operativo.")

    with col_action:
        generate_weekly_report()
        st.divider()
        st.write("Parametri Analisi:")
        st.checkbox("Includi dati Social", value=True)
        st.checkbox("Includi dati Meteo", value=True)
