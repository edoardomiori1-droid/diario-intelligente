"""
SYNAPSE NEURAL OS - CENTRAL DASHBOARD
-------------------------------------
File 11/35 | pages/11_page_dashboard.py
Posizione: /pages/11_page_dashboard.py

DESCRIZIONE:
L'interfaccia principale dell'OS. Visualizza il profilo neurale 
attraverso grafici radar e fornisce l'accesso rapido ai moduli core.
"""

import streamlit as st
import plotly.graph_objects as go

# Import moduli interni
try:
    from ui.08_ui_components import section_header, glass_card, stats_counter
    from ui.09_ui_sidebar import render_sidebar
    from core.03_core_config import get_config
except ImportError:
    pass

def render_hub():
    """Rendering della Dashboard principale."""
    
    # 1. ATTIVAZIONE SIDEBAR (Navigazione)
    render_sidebar()
    
    # 2. HEADER DINAMICO
    user = st.session_state.user_profile
    nickname = user.get('nickname', 'Operatore')
    
    st.markdown(f"<h1>WELCOME, {nickname.upper()}</h1>", unsafe_allow_html=True)
    st.caption(f"Sincronizzazione Neurale: ATTIVA | Sessione: {st.session_state.get('session_id', 'N/A')}")
    st.divider()

    # 3. LAYOUT A COLONNE (Grafico a sinistra, Info a destra)
    col_left, col_right = st.columns([3, 2])

    with col_left:
        section_header("Profilo Neurale", icon="🧠")
        render_radar_chart(user.get('stats', {}))

    with col_right:
        section_header("Stato Sistema", icon="🛰️")
        
        # Widget rapidi
        stats_counter("Settore Operativo", user.get('sector', 'N/A'))
        stats_counter("Data Inizializzazione", user.get('birth_date', 'N/A'))
        
        st.write("") # Spaziatore
        
        glass_card(
            "Diagnostica", 
            f"Kernel: {st.session_state.get('os_version', 'V5.5')}<br>"
            f"Uptime: {st.session_state.get('boot_time', 'N/A')}<br>"
            "Status: <span style='color:#00FFC8;'>OPTIMAL</span>"
        )

    # 4. LOG DI SISTEMA (In basso)
    with st.expander("👁️ VISUALIZZA LOG DI SISTEMA"):
        for log in st.session_state.get('internal_logs', [])[-5:]: # Mostra gli ultimi 5
            st.code(log)

def render_radar_chart(stats):
    """Genera il grafico radar basato sulle skill dell'utente."""
    if not stats:
        st.warning("Nessun dato statistico rilevato.")
        return

    categories = list(stats.keys())
    values = list(stats.values())
    
    # Il grafico deve chiudersi su se stesso, quindi ripetiamo il primo valore
    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(0, 242, 255, 0.2)',
        line=dict(color='#00F2FF', width=2),
        name='Neural Profile'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=20, b=20),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)
