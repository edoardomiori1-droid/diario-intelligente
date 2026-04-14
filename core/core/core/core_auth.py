"""
SYNAPSE NEURAL OS - ACCESS & AUTH MANAGER
-----------------------------------------
File 04/35: core/core_auth.py
Ruolo: Gestione dei Permessi e Stato di Accesso

Questo file è il 'filtro' del sistema. Determina se l'utente ha i requisiti
per accedere alle funzionalità avanzate dell'Hub o se deve essere 
reindirizzato alla configurazione iniziale.
"""

import streamlit as st

def is_user_authenticated():
    """
    Verifica se esiste un profilo utente valido nella memoria di sessione.
    Ritorna True se l'utente ha completato l'onboarding, False altrimenti.
    """
    # Controlliamo se la chiave 'user_profile' esiste ed è popolata
    if 'user_profile' in st.session_state and st.session_state.user_profile is not None:
        return True
    return False

def check_setup_progress():
    """
    Ritorna lo step attuale della configurazione iniziale.
    Utilizzato per garantire che l'utente non salti passaggi critici.
    """
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    return st.session_state.onboarding_step

def grant_access(final_profile_data):
    """
    Finalizza la procedura di registrazione.
    Prende i dati temporanei, li valida e li sposta nel profilo definitivo,
    sbloccando l'accesso all'intero OS.
    """
    if final_profile_data:
        # Trasferimento dati nel registro master
        st.session_state.user_profile = final_profile_data
        
        # Log di sistema per tracciare l'evento (Useremo la funzione del File 02)
        from core.core_init import log_system_event
        log_system_event("AUTH: Accesso garantito. Profilo creato con successo.")
        
        # Reset dello step di onboarding per usi futuri
        st.session_state.onboarding_step = 1
        return True
    return False

def revoke_access():
    """
    Disconnette l'utente e lo riporta alla fase di boot iniziale.
    Utile per il logout o per il reset di emergenza.
    """
    st.session_state.user_profile = None
    from core.core_init import log_system_event
    log_system_event("AUTH: Accesso revocato. Sessione terminata.")
