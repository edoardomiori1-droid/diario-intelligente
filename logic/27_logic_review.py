"""
SYNAPSE NEURAL OS - EVENING REVIEW ENGINE
-----------------------------------------
File 27/35 | logic/27_logic_review.py
Posizione: /logic/27_logic_review.py

DESCRIZIONE:
Gestisce la procedura di fine giornata. Trasforma i pensieri sparsi 
in entrate strutturate nel diario e aggiorna le skill dell'operatore.
"""

import streamlit as st
from datetime import datetime

try:
    from ui.08_ui_components import section_header, glass_card
    from logic.17_logic_analysis import extract_skills_update, analyze_sentiment
except ImportError:
    pass

def render_evening_review():
    """Interfaccia guidata per il diario serale."""
    section_header("Revisione Serale", icon="🌙")
    
    st.write("Configurazione terminale per il backup della giornata...")
    
    # Area di scrittura libera
    entry_text = st.text_area(
        "Cosa è successo oggi? (Nomina persone, attività e stati d'animo)",
        height=250,
        placeholder="Esempio: Oggi ho lavorato con Marco al progetto X. Mi sento soddisfatto ma un po' stanco..."
    )

    if st.button("Sincronizza Giornata con il Sistema"):
        if entry_text:
            # 1. ANALISI DEL SENTIMENT E DELLE SKILL
            sentiment, color = analyze_sentiment(entry_text)
            skill_updates = extract_skills_update(entry_text)
            
            # 2. AGGIORNAMENTO PROFILO (STATISTICHE)
            if skill_updates:
                for skill, val in skill_updates.items():
                    if skill in st.session_state.user_profile['stats']:
                        # Incrementiamo la skill (fino a un massimo di 10)
                        current = st.session_state.user_profile['stats'][skill]
                        st.session_state.user_profile['stats'][skill] = min(10, current + 0.1)
                st.toast("⚡ Statistiche Neurali aggiornate in base al racconto!")

            # 3. SALVATAGGIO NEL VAULT (MEMORIA STORICA)
            new_entry = {
                "id": len(st.session_state.get('vault_data', [])) + 1,
                "title": f"Diario Serale - {datetime.now().strftime('%d/%m/%Y')}",
                "content": entry_text,
                "category": "Diario",
                "sentiment": sentiment,
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.vault_data.insert(0, new_entry)
            
            # 4. FEEDBACK VISIVO
            st.success("Sessione giornaliera archiviata correttamente.")
            glass_card(f"Analisi IA: {sentiment}", f"Ho rilevato progressi nelle seguenti aree: {list(skill_updates.keys()) if skill_updates else 'Mantenimento generale'}")
            
            # Salvataggio su file automatico (se File 18 è pronto)
            try:
                from data.18_data_manager import save_os_data
                save_os_data()
            except:
                pass
        else:
            st.error("Il buffer è vuoto. Inserisci i dati della giornata.")

def get_review_summary():
    """Genera un riassunto per la dashboard."""
    return f"Ultima revisione: {datetime.now().strftime('%d/%m/%Y')}"
