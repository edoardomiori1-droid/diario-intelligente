"""
SYNAPSE NEURAL OS - MEMORY FOUNDATION
-------------------------------------
File 02/35 | core/02_core_init.py
Posizione: /core/02_core_init.py

DESCRIZIONE:
Inizializzazione universale dello Stato della Sessione (Session State).
Questo file definisce la struttura dati che verrà usata da tutti i moduli
successivi (AI, Grafica, Pagine). Previene errori di tipo 'AttributeError'.
"""

import streamlit as st
from datetime import datetime

def initialize_session():
    """
    Crea e configura i registri di memoria al primo avvio assoluto.
    Se l'utente ricarica la pagina, questo modulo protegge i dati esistenti.
    """
    
    # --- SISTEMA DI SICUREZZA ---
    # Inizializziamo solo se il kernel non è già attivo
    if 'system_ready' not in st.session_state:
        
        # 1. REGISTRI IDENTITÀ (USER DATA)
        # Qui salveremo: nickname, età (fix 2010), settore e missione.
        # Valore iniziale: None (segnala al File 01 di mostrare l'Onboarding)
        st.session_state.user_profile = None  
        
        # Gestore degli step della configurazione iniziale
        st.session_state.onboarding_step = 1  
        
        # 2. REGISTRI NEURALI (AI & DIARIO)
        # Una lista di dizionari per conservare la conversazione con l'IA.
        # Formato: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        st.session_state.chat_history = []    
        
        # Buffer per l'analisi dei dati in tempo reale
        st.session_state.current_analysis = ""
        
        # 3. REGISTRI ESTETICI (THEME ENGINE)
        # Permette di cambiare l'intero stile dell'OS con una variabile.
        st.session_state.active_theme = "NEON_CYBER"
        st.session_state.ui_ready = False
        
        # 4. REGISTRI TECNICI (LOGS & METADATA)
        # Informazioni per il debug e per rendere l'OS "vivo".
        st.session_state.system_ready = True
        st.session_state.boot_time = datetime.now().strftime("%H:%M:%S")
        st.session_state.os_version = "V 5.5.0-MASTER"
        
        # Diario degli eventi interno (non visibile all'utente se non richiesto)
        st.session_state.internal_logs = [
            f"BOOT: Kernel Synapse OS caricato alle {st.session_state.boot_time}",
            "MEM: Allocazione registri completata con successo."
        ]
        
        # Stampa tecnica nel terminale per conferma sviluppo
        print(f">>> [SYSTEM] Sessione inizializzata: {st.session_state.os_version}")

def write_log(message):
    """
    Funzione universale richiamabile da ogni file per aggiungere un evento ai log.
    Esempio: write_log("Utente ha completato lo step 1")
    """
    if 'internal_logs' in st.session_state:
        now = datetime.now().strftime("%H:%M:%S")
        st.session_state.internal_logs.append(f"[{now}] {message}")

def get_session_uptime():
    """Ritorna da quanto tempo il sistema è attivo in questa sessione."""
    if 'boot_time' in st.session_state:
        return st.session_state.boot_time
    return "N/A"
