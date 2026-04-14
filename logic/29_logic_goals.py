"""
SYNAPSE NEURAL OS - GOAL & MILESTONE TRACKER
--------------------------------------------
File 29/35 | logic/29_logic_goals.py
Posizione: /logic/29_logic_goals.py

DESCRIZIONE:
Gestisce gli obiettivi a lungo termine dell'operatore.
Permette di monitorare il progresso verso milestone specifiche.
"""

import streamlit as st
from ui.08_ui_components import section_header, glass_card

def render_goals_manager():
    """Interfaccia per la gestione degli obiettivi."""
    section_header("Obiettivi Neurali", icon="🏆")

    if 'user_goals' not in st.session_state:
        st.session_state.user_goals = []

    # 1. CREAZIONE NUOVO OBIETTIVO
    with st.expander("🚀 DEFINISCI NUOVA MISSIONE"):
        col_t, col_c = st.columns([2, 1])
        with col_t:
            goal_title = st.text_input("Titolo Obiettivo", placeholder="Es: Imparare Python")
        with col_c:
            goal_cat = st.selectbox("Area", ["Logica", "Creatività", "Salute", "Social", "Carriera"])
        
        goal_desc = st.text_area("Descrizione del traguardo...")
        
        if st.button("INIZIALIZZA MISSIONE"):
            if goal_title:
                new_goal = {
                    "title": goal_title,
                    "cat": goal_cat,
                    "desc": goal_desc,
                    "progress": 0,
                    "status": "ATTIVO"
                }
                st.session_state.user_goals.append(new_goal)
                st.success(f"Missione '{goal_title}' caricata nel sistema.")
                st.rerun()

    st.divider()

    # 2. LISTA OBIETTIVI ATTIVI
    if not st.session_state.user_goals:
        st.info("Nessuna missione attiva rilevata nel quadrante.")
    else:
        for i, goal in enumerate(st.session_state.user_goals):
            with st.container():
                col_info, col_prog = st.columns([2, 1])
                
                with col_info:
                    st.markdown(f"### {goal['title']} `[{goal['cat']}]`")
                    st.write(goal['desc'])
                
                with col_prog:
                    # Slider per aggiornare il progresso manualmente
                    new_prog = st.slider(
                        "Progresso %", 0, 100, goal['progress'], key=f"goal_{i}"
                    )
                    st.session_state.user_goals[i]['progress'] = new_prog
                    
                    if st.button(f"Archivia #{i}", key=f"del_goal_{i}"):
                        st.session_state.user_goals.pop(i)
                        st.rerun()
                
                # Barra di caricamento visuale
                st.progress(new_prog / 100)
                st.write("---")

def get_goals_context():
    """Ritorna gli obiettivi attivi per l'analisi IA."""
    goals = st.session_state.get('user_profile', [])
    if not goals: return "Nessun obiettivo impostato."
    return str([{g['title']: g['progress']} for g in st.session_state.user_goals])
