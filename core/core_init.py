"""
SYNAPSE NEURAL OS - MEMORY ARCHITECTURE
---------------------------------------
File 02/35: core/core_init.py
Ruolo: Inizializzazione Universale dei Registri di Memoria

Questo modulo è il pilastro su cui poggia l'intera persistenza dell'app.
Viene richiamato come primissima istruzione in app.py. 
Il suo compito è verificare se le variabili di stato esistono; 
se non esistono, le crea definendo il tipo di dato (Liste, Dizionari, Stringhe).
"""

import streamlit as st
from datetime import datetime

def initialize_session():
    """
    Esegue il boot della memoria di sessione.
    Garantisce che ogni modulo dell'app trovi le variabili di cui ha bisogno.
    """
    
    # --- IL 'CHECK' DI SICUREZZA ---
    # Questo controllo impedisce al sistema di sovrascrivere i dati 
    # ogni volta che la pagina viene aggiornata (Rerun).
    if 'system_ready' not in st.session_state:
        
        # 1. REGISTRO IDENTITÀ (DATI PROFILO)
        # Inizialmente None. Quando questo diventa un dizionario, 
        # app.py capisce che deve mostrare la Dashboard invece del Setup.
        st.session_state.user_profile = None  
        
        # 2. SISTEMA DI ROUTING (LOGICA DI NAVIGAZIONE)
        # 'step' guida l'utente attraverso le fasi di registrazione.
        # 'active_page' gestisce il menu principale dell'Hub.
        st.session_state.onboarding_step = 1  
        st.session_state.active_page = "Home"
        
        # 3. DATABASE CHAT (MEMORIA NEURALE)
        # Una lista di messaggi. Ogni volta che parli con l'IA, 
        # il messaggio viene aggiunto qui per mantenere il filo del discorso.
        st.session_state.chat_history = []    
        
        # 4. SKIN ENGINE (ESTETICA VISIVA)
        # Memorizza il nome del tema attivo per iniettare i colori corretti 
        # in ogni componente grafico.
        st.session_state.active_theme = "SYNAPSE_PRIME" 
        
        # 5. BUFFER DI SISTEMA (STORAGE TEMPORANEO)
        # Durante la registrazione (onboarding), i dati vengono salvati qui 
        # 'a matita' prima di essere confermati e scritti nel profilo finale.
        st.session_state.temp_storage = {}    
        
        # 6. REGISTRI TECNICI E METRICHE
        # Qui memorizziamo i dati 'sotto il cofano' che rendono l'app professionale.
        st.session_state.update({
            'system_ready': True,                             # Stato operativo
            'boot_time': datetime.now().strftime("%H:%M:%S"), # Timestamp di avvio
            'session_id': f"SYS-{datetime.now().strftime('%d%m%y')}", # ID univoco sessione
            'os_version': "5.5.0-PLATINUM",                  # Versione software
            'logs': ["SYSTEM: Kernel online", "MEMORY: Allocated"] # Storico eventi
        })
        
        # Feedback visivo nel terminale dello sviluppatore
        print(">>> [SYNAPSE OS] Memoria di sistema configurata con successo.")

def log_system_event(message):
    """
    Funzione universale richiamabile da qualsiasi altro dei 35 file.
    Permette di aggiungere un messaggio alla lista dei log di sistema.
    """
    if 'logs' in st.session_state:
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.logs.append(f"[{timestamp}] {message}")

def reset_memory():
    """
    Pulisce selettivamente la memoria per permettere un reboot pulito 
    senza dover ricaricare l'intera pagina web.
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
