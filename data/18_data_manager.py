"""
SYNAPSE NEURAL OS - DATA PERSISTENCE MANAGER
-------------------------------------------
File 18/35 | data/18_data_manager.py
Posizione: /data/18_data_manager.py

DESCRIZIONE:
Gestisce il salvataggio e il caricamento dei dati utente su file JSON.
Assicura che il profilo, il vault e la chat non vadano perduti.
"""

import json
import os
import streamlit as st

SAVE_FILE = "synapse_vault_vault.json"

def save_os_data():
    """
    Raccoglie tutti i dati importanti e li scrive su disco.
    """
    data_to_save = {
        "user_profile": st.session_state.get('user_profile'),
        "vault_data": st.session_state.get('vault_data', []),
        "chat_history": st.session_state.get('chat_history', []),
        "internal_logs": st.session_state.get('internal_logs', [])
    }
    
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"ERRORE SALVATAGGIO: {e}")
        return False

def load_os_data():
    """
    Legge il file JSON e ripristina la sessione dell'utente.
    """
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
            
            # Ripristiniamo le chiavi nel session_state
            st.session_state.user_profile = loaded_data.get("user_profile")
            st.session_state.vault_data = loaded_data.get("vault_data", [])
            st.session_state.chat_history = loaded_data.get("chat_history", [])
            st.session_state.internal_logs = loaded_data.get("internal_logs", [])
            
            return True
        except Exception as e:
            st.error(f"ERRORE CARICAMENTO: {e}")
    return False

def export_as_text():
    """
    Permette all'utente di scaricare i propri dati in formato leggibile.
    """
    content = f"--- SYNAPSE NEURAL OS EXPORT ---\n"
    content += f"User: {st.session_state.user_profile.get('nickname') if st.session_state.user_profile else 'N/A'}\n"
    # Aggiungi qui altri dettagli per l'export
    return content
