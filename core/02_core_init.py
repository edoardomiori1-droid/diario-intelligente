"""
SYNAPSE NEURAL OS - MEMORY FOUNDATION ENGINE
--------------------------------------------
File 02/35 | core/02_core_init.py
Ruolo: Inizializzazione Universale della Memoria di Sessione.

Questo modulo garantisce che all'avvio dell'applicazione tutte le 
variabili di stato (Session State) siano dichiarate e pronte all'uso. 
Senza questo file, il sistema andrebbe in crash cercando di leggere 
dati non ancora esistenti.
"""

import streamlit as st
from datetime import datetime

def initialize_session():
    """
    Esegue il boot dei registri di memoria. 
    Viene richiamato una sola volta per sessione dal file 01_app.py.
    """
    
    # --- CONTROLLO DI INTEGRITÀ ---
    # Inizializziamo solo se il sistema non è già stato 'visto'
    if 'system_initialized' not in st.session_state:
        
        # 1. REGISTRO PROFILO (USER IDENTITY)
        # Contiene: nickname, età, settore, missione, e dati del grafico radar.
        # È impostato a None finché l'onboarding non viene completato.
        st.session_state.user_profile = None  
        
        # 2. SISTEMA DI NAVIGAZIONE (ROUTING)
        # 'setup_step' guida l'utente attraverso i file della cartella /pages.
        st.session_state.setup_step = 1  
        st.session_state.active_hub_page = "Dashboard"
        
        # 3. MEMORIA NEURALE (AI & CHAT HISTORY)
        # Una lista di dizionari che memorizzano lo storico conversazionale.
        # Esempio: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        st.session_state.chat_history = []    
        
        # 4. ENGINE ESTETICO (THEME & UI STATE)
        # Memorizza il tema attivo e lo stato di visibilità degli elementi.
        st.session_state.active_theme = "SYNAPSE_PLATINUM"
        st.session_state.sidebar_visible = False
        
        # 5. REGISTRI TECNICI (METADATA & LOGS)
        # Informazioni critiche per il monitoraggio del sistema.
        st.session_state.update({
            'system_initialized': True,                      # Flag di avvio completato
            'boot_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'os_version': "5.5.0-PLATINUM",                 # Versione Master
            'session_id': f"SYN-{datetime.now().strftime('%d%m%y-%H%M')}",
            'system_logs': ["BOOT: Kernel Synapse OS caricato correttamente."]
        })
        
        # Stampa tecnica invisibile all'utente (visibile nei log server)
        print(f">>> [SYSTEM] Sessione {st.session_state.session_id} inizializzata.")

def add_log(event_description):
    """
    Funzione di utilità universale per registrare eventi nel diario di sistema.
    Esempio: add_log("Utente ha cambiato il tema")
    """
    if 'system_logs' in st.session_state:
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.system_logs.append(f"[{timestamp}] {event_description}")

def get_profile_status():
    """
    Ritorna True se il profilo è completo, utile per il routing veloce.
    """
    return st.session_state.user_profile is not None
