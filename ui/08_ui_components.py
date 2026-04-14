"""
SYNAPSE NEURAL OS - UI COMPONENTS
---------------------------------
File 08/35 | ui/08_ui_components.py
Posizione: /ui/08_ui_components.py

DESCRIZIONE:
Raccolta di funzioni grafiche riutilizzabili. 
Evita la duplicazione di codice HTML/CSS nelle pagine finali.
"""

import streamlit as st
try:
    from ui.07_ui_assets import draw_header_line
except ImportError:
    def draw_header_line(): st.divider()

def section_header(title, icon="🚀"):
    """
    Crea un'intestazione di sezione stilizzata con icona e linea neon.
    """
    st.markdown(f"## {icon} {title}")
    draw_header_line()

def glass_card(title, content, type="info"):
    """
    Crea un contenitore con effetto vetro e bordo colorato in base al tipo.
    """
    colors = {
        "info": "rgba(0, 242, 255, 0.3)",
        "warning": "rgba(255, 165, 0, 0.3)",
        "danger": "rgba(255, 0, 0, 0.3)",
        "success": "rgba(0, 255, 200, 0.3)"
    }
    border_color = colors.get(type, colors["info"])
    
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.03);
        border-left: 5px solid {border_color};
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    ">
        <h4 style="margin-top:0; color:white;">{title}</h4>
        <p style="color: #cccccc; font-size: 0.9em;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def stats_counter(label, value, delta=None):
    """
    Visualizza una statistica in stile 'Dashboard Digitale'.
    """
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption(label)
        st.subheader(value)
    if delta:
        with col2:
            st.metric("", "", delta=delta)

def info_badge(text):
    """Crea un piccolo badge di stato."""
    st.markdown(f"""
        <span style="
            background: rgba(0, 242, 255, 0.1);
            color: #00F2FF;
            padding: 2px 10px;
            border-radius: 20px;
            border: 1px solid #00F2FF;
            font-size: 0.7em;
            font-family: 'Roboto Mono', monospace;
        ">{text}</span>
    """, unsafe_allow_html=True)
