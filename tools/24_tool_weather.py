"""
SYNAPSE NEURAL OS - ENVIRONMENTAL CONTEXT (WEATHER)
---------------------------------------------------
File 24/35 | tools/24_tool_weather.py
Posizione: /tools/24_tool_weather.py

DESCRIZIONE:
Recupera dati ambientali per arricchire le voci del diario.
Permette all'IA di correlare il mood dell'utente con i fattori esterni.
"""

import streamlit as st
from ui.08_ui_components import section_header, glass_card

def render_weather_tool():
    """Rendering dell'interfaccia Meteo/Ambiente."""
    section_header("Environmental Sensors", icon="🌡️")
    
    st.caption("Dati rilevati per l'integrazione nel Diario Serale.")

    col_data, col_geo = st.columns([1, 1])

    with col_data:
        # Input manuale (per ora) o simulato per non richiedere chiavi API extra
        st.write("Stato Atmosferico:")
        weather_state = st.selectbox("Condizioni", ["Sereno", "Pioggia", "Nuvoloso", "Tempesta", "Neve"])
        temp = st.slider("Temperatura Esterna (°C)", -10, 45, 20)
        
        if st.button("SINCRONIZZA DATI AMBIENTALI"):
            st.session_state.current_env = {
                "weather": weather_state,
                "temp": temp,
                "timestamp": st.session_state.get('current_time', 'Ora')
            }
            st.success("Parametri ambientali fissati nel buffer di oggi.")

    with col_geo:
        glass_card(
            "Analisi Correlazione",
            "L'IA utilizzerà questi dati per analizzare come il clima influisce sulla tua "
            "<b>Efficienza Operativa</b> e sul tuo <b>Bio-Feedback</b>."
        )

    st.divider()
    
    # Log degli ultimi dati ambientali salvati
    if 'current_env' in st.session_state:
        env = st.session_state.current_env
        st.info(f"Ultimo Rilevamento: {env['weather']} | {env['temp']}°C")
