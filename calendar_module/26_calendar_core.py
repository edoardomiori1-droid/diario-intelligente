"""
SYNAPSE NEURAL OS - INTERACTIVE CALENDAR
----------------------------------------
File 26/35 | calendar_module/26_calendar_core.py
Posizione: /calendar_module/26_calendar_core.py

DESCRIZIONE:
Modulo di visualizzazione temporale. Permette di consultare lo storico
di chat, mood e statistiche filtrandoli per data.
"""

import streamlit as st
from datetime import date
from ui.08_ui_components import section_header, glass_card

def render_interactive_calendar():
    """Rendering del calendario e del visualizzatore dati storici."""
    section_header("Calendario Neurale", icon="📅")
    
    # 1. SELETTORE DATA (Interattivo)
    # Impostiamo il default al 2010 come da tua specifica iniziale per la navigazione
    col_cal, col_preview = st.columns([1, 2])
    
    with col_cal:
        st.write("Seleziona un punto nel tempo:")
        selected_date = st.date_input(
            "Navigazione Temporale",
            value=date.today(),
            key="calendar_nav"
        )
        formatted_date = selected_date.strftime("%d/%m/%Y")
        st.info(f"Visualizzazione: {formatted_date}")

    with col_preview:
        # Recuperiamo i dati salvati per quella data
        # Cerchiamo nel Vault, nel Mood e nei Log
        day_data = fetch_data_by_date(formatted_date)
        
        if not day_data['has_content']:
            st.warning("Nessuna traccia neurale rilevata in questa data.")
        else:
            st.success(f"Dati recuperati per il giorno {formatted_date}")

    st.divider()

    # 2. VISUALIZZAZIONE DETTAGLIATA DEL GIORNO SELEZIONATO
    if day_data['has_content']:
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("📝 Scritti e Note")
            for note in day_data['notes']:
                glass_card(note['title'], note['content'])
        
        with c2:
            st.subheader("📊 Statistiche e Mood")
            if day_data['mood']:
                st.markdown(f"**Mood Registrato:** {day_data['mood']['val']}/5")
                st.markdown(f"<div style='width:100%; height:10px; background:{day_data['mood']['color']}; border-radius:5px;'></div>", unsafe_allow_html=True)
            
            # Qui mostreremo anche un piccolo riassunto delle attività
            st.metric("Messaggi in Chat", day_data['chat_count'])
            st.metric("Frammenti Vault", len(day_data['notes']))

def fetch_data_by_date(target_date):
    """
    Interroga il session_state per estrarre tutto ciò che è 
    successo in una data specifica.
    """
    vault = st.session_state.get('vault_data', [])
    mood_history = st.session_state.get('mood_history', {})
    
    # Filtriamo le note del vault che hanno il timestamp della data selezionata
    day_notes = [n for n in vault if target_date in n.get('timestamp', '')]
    
    # Recuperiamo il mood
    day_mood = mood_history.get(target_date)
    
    # Contiamo i messaggi chat (se salvati con data)
    chat_count = sum(1 for m in st.session_state.get('chat_history', []) if target_date in m.get('timestamp', ''))

    has_content = len(day_notes) > 0 or day_mood is not None
    
    return {
        "has_content": has_content,
        "notes": day_notes,
        "mood": day_mood,
        "chat_count": chat_count
    }
