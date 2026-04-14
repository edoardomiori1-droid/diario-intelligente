"""
SYNAPSE NEURAL OS - SYSTEM RESET ENGINE
---------------------------------------
File 05/35 | core/05_core_reset.py
Posizione: /core/05_core_reset.py

DESCRIZIONE:
Modulo dedicato alla manutenzione e alla pulizia dei dati.
Permette di svuotare la cache e resettare lo stato della sessione
in modo controllato e sicuro.
"""

import streamlit as st

def execute_factory_reset():
    """
    Esegue un Wipe totale di tutte le variabili di sessione.
    Dopo l'esecuzione, l'utente viene riportato alla schermata di boot.
    """
    # 1. Messaggio di log preventivo
    try:
        from core.02_core_init import write_log
        write_log("CRITICAL: Avvio procedura di Factory Reset.")
    except:
        pass

    # 2. Ciclo di distruzione delle chiavi
    # Eliminiamo ogni singola variabile salvata in st.session_state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # 3. Notifica di successo e riavvio immediato
    st.toast("SISTEMA RESETTATO: Ritorno alle condizioni di fabbrica.", icon="♻️")
    st.rerun()

def soft_reset_chat():
    """
    Resetta solo la cronologia della chat IA.
    Mantiene intatti i dati del profilo utente e le impostazioni.
    """
    if 'chat_history' in st.session_state:
        st.session_state.chat_history = []
        st.toast("Memoria neurale (Chat) ripulita con successo.", icon="🧼")
    else:
        st.info("Nessuna cronologia rilevata da pulire.")

def clear_system_logs():
    """Svuota il registro degli eventi tecnici."""
    if 'internal_logs' in st.session_state:
        st.session_state.internal_logs = ["SISTEMA: Log resettati manualmente."]
        st.success("Registri di sistema svuotati.")
