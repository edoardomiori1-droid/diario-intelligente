"""
SYNAPSE NEURAL OS - FOCUS ENGINE
--------------------------------
File 20/35 | tools/20_tool_focus.py
Posizione: /tools/20_tool_focus.py

DESCRIZIONE:
Timer per sessioni di Deep Work. Integra la logica Pomodoro 
per ottimizzare i cicli di lavoro e riposo dell'operatore.
"""

import streamlit as st
import time
from ui.08_ui_components import section_header, glass_card

def render_focus_tool():
    """Rendering dell'interfaccia Focus."""
    section_header("Focus Engine", icon="🎯")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Configura la tua sessione di Deep Work:")
        duration = st.slider("Durata Sessione (minuti)", 5, 120, 25)
        
        if "timer_active" not in st.session_state:
            st.session_state.timer_active = False

        if not st.session_state.timer_active:
            if st.button("🚀 INIZIA SEQUENZA FOCUS"):
                st.session_state.timer_active = True
                st.session_state.start_time = time.time()
                st.session_state.end_time = time.time() + (duration * 60)
                st.rerun()
        else:
            remaining = int(st.session_state.end_time - time.time())
            if remaining > 0:
                mins, secs = divmod(remaining, 60)
                st.markdown(f"""
                    <div style='text-align: center; padding: 40px; border: 2px solid #00F2FF; border-radius: 50%; width: 200px; height: 200px; margin: auto;'>
                        <h1 style='color: #00F2FF; font-size: 3em; margin-top: 20px;'>{mins:02d}:{secs:02d}</h1>
                        <p style='font-size: 0.8em; opacity: 0.6;'>FOCUS ATTIVO</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("❌ ABORTISCI MISSIONE"):
                    st.session_state.timer_active = False
                    st.rerun()
                
                # Auto-refresh ogni secondo (nota: Streamlit richiede interazione o script specifici per refresh continui)
                time.sleep(1)
                st.rerun()
            else:
                st.balloons()
                st.success("SESSIONE COMPLETATA: Sincronizzazione Neurale Ottimizzata!")
                st.session_state.timer_active = False

    with col2:
        glass_card(
            "Protocollo Pomodoro",
            "25 min: Focus Totale<br>5 min: Deframmentazione (Pausa)<br><br>"
            "<i>Il silenzio è il tuo miglior uplink.</i>"
        )
