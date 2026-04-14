"""
SYNAPSE NEURAL OS - INTEGRATED DASHBOARD
----------------------------------------
File 11/60 | pages/11_page_dashboard.py

DESCRIZIONE:
Il punto di controllo centrale. Visualizza statistiche, notifiche 
e lo stato del sistema in tempo reale.
"""

import streamlit as st
from ui.08_ui_components import section_header, glass_card

# Importiamo i moduli che abbiamo creato nei file precedenti
try:
    from ui.33_ui_notifications import render_notification_hub
    from logic.35_logic_stats_engine import render_radar_chart, render_skill_bars
    from tools.24_tool_weather import render_weather_tool
    from logic.29_logic_goals import get_goals_context
except ImportError:
    pass

def render_dashboard():
    """Rendering della Dashboard principale."""
    
    # 1. Header con nome utente e ora di sistema
    user = st.session_state.user_profile
    st.markdown(f"### BENVENUTO OPERATORE: {user['nickname'].upper()} ⚡")
    st.caption(f"Status: Uplink Stabile | Settore: {user['sector']}")

    # 2. Hub Notifiche (File 33)
    render_notification_hub()

    st.divider()

    # 3. Layout a Colonne: Sinistra (Stats) | Destra (Quick Info)
    col_left, col_right = st.columns([2, 1])

    with col_left:
        section_header("Sincronizzazione Neurale", icon="🧠")
        # Visualizziamo il grafico radar che abbiamo creato nel File 35
        render_radar_chart()
        
        with st.expander("Vedi Dettaglio Skill"):
            render_skill_bars()

    with col_right:
        section_header("Status Ambientale", icon="🌡️")
        # Mostriamo il widget meteo del File 24
        if 'current_env' in st.session_state:
            env = st.session_state.current_env
            glass_card(
                f"{env['weather'].upper()} - {env['temp']}°C",
                f"Ultimo rilevamento: {env['timestamp']}"
            )
        else:
            st.info("Nessun dato meteo sincronizzato. Vai in Tools > Meteo.")

        st.divider()
        
        section_header("Obiettivi Prioritari", icon="🎯")
        # Anteprima rapida degli obiettivi dal File 29
        goals = st.session_state.get('user_goals', [])
        if goals:
            for g in goals[:2]: # Mostra solo i primi due
                st.write(f"**{g['title']}**")
                st.progress(g['progress'] / 100)
        else:
            st.write("Nessuna missione attiva.")

    # 4. Footer con log di sistema rapido (File 31)
    st.divider()
    with st.expander("📜 System Log Console"):
        from core.31_core_logs import render_log_viewer
        render_log_viewer()
