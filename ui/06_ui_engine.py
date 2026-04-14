"""
SYNAPSE NEURAL OS - UI ENGINE
-----------------------------
File 06/35 | ui/06_ui_engine.py
Posizione: /ui/06_ui_engine.py

DESCRIZIONE:
Questo modulo gestisce l'iniezione di codice CSS personalizzato.
Crea il design "Glassmorphism" (effetto vetro) e definisce la
palette cromatica universale del sistema.
"""

import streamlit as st

def apply_styles():
    """
    Inietta il CSS nel frontend di Streamlit.
    Viene richiamato dal Bootloader (File 01) ad ogni refresh.
    """
    
    # Definiamo il CSS all'interno di una stringa multi-riga
    style_css = """
    <style>
        /* Sfondo generale e font futuristico */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #050a0f 0%, #0a192f 100%);
            color: #e0e0e0;
            font-family: 'Roboto Mono', monospace;
        }

        /* Effetto VETRO per i contenitori (Cards) */
        div.stButton > button, .stMarkdown, .main .block-container div[data-testid="stVerticalBlock"] > div {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            transition: all 0.3s ease;
        }

        /* Header con font Orbitron */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: #00F2FF !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0px 0px 10px rgba(0, 242, 255, 0.5);
        }

        /* Pulsanti NEON */
        div.stButton > button {
            background: transparent !important;
            border: 1px solid #00F2FF !important;
            color: #00F2FF !important;
            font-weight: bold;
            width: 100%;
        }

        div.stButton > button:hover {
            background: #00F2FF !important;
            color: #050a0f !important;
            box-shadow: 0px 0px 20px #00F2FF;
            transform: translateY(-2px);
        }

        /* Nascondi elementi inutili di Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Barra laterale personalizzata */
        [data-testid="stSidebar"] {
            background-color: rgba(5, 10, 15, 0.9);
            border-right: 1px solid #00F2FF;
        }
    </style>
    """
    
    # Iniezione nel browser
    st.markdown(style_css, unsafe_allow_html=True)

def inject_glass_card(content):
    """
    Funzione di utilità per avvolgere qualsiasi contenuto 
    in una 'card' con effetto vetro.
    """
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(0, 242, 255, 0.2);
        padding: 25px;
        margin-bottom: 20px;
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)
