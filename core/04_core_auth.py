"""
SYNAPSE NEURAL OS - AUTHENTICATION MANAGER
------------------------------------------
File 04/35 | core/04_core_auth.py
Posizione: /core/04_core_auth.py

DESCRIZIONE:
Questo modulo gestisce lo stato di accesso dell'utente.
Verifica se il profilo esiste e fornisce funzioni per il logout
o per recuperare il nome dell'utente in modo sicuro.
"""

import streamlit as st

def is_authenticated():
    """
    Controlla se l'utente ha completato la configurazione iniziale.
    Viene interrogato dal File 01 ad ogni aggiornamento della pagina.
    """
    # Verifichiamo se la chiave 'user_profile' esiste ed è piena
    if 'user_profile' in st.session_state and st.session_state.user_profile is not None:
        return True
    return False

def get_current_user():
    """
    Ritorna i dati del profilo se l'utente è autenticato.
    Altrimenti ritorna un dizionario vuoto per evitare errori.
    """
    if is_authenticated():
        return st.session_state.user_profile
    return {}

def require_auth():
    """
    Funzione di protezione: se chiamata in una pagina che richiede 
    l'accesso, blocca l'esecuzione se l'utente è un ospite.
    """
    if not is_authenticated():
        st.warning("⚠️ ACCESSO NEGATO: Identità neurale non rilevata.")
        st.stop()

def logout():
    """
    Resetta lo stato di autenticazione riportando l'utente al setup.
    """
    st.session_state.user_profile = None
    st.session_state.onboarding_step = 1
    # Registriamo l'evento nei log (se il file 02 è attivo)
    try:
        from core.02_core_init import write_log
        write_log("LOGOUT: Sessione terminata dall'utente.")
    except:
        pass
    st.rerun()
