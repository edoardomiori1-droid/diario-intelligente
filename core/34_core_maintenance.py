"""
SYNAPSE NEURAL OS - SYSTEM MAINTENANCE
--------------------------------------
File 34/60 | core/34_core_maintenance.py
Posizione: /core/34_core_maintenance.py

DESCRIZIONE:
Modulo per la gestione dell'integrità dei dati. 
Permette il wipe selettivo o totale e la riparazione del database.
"""

import streamlit as st
import os

def check_database_integrity():
    """Verifica se il file di salvataggio è integro e leggibile."""
    save_path = "synapse_vault_vault.json"
    if not os.path.exists(save_path):
        return "MISSING", "File database non trovato. Verrà creato al primo salvataggio."
    
    try:
        import json
        with open(save_path, "r", encoding="utf-8") as f:
            json.load(f)
        return "HEALTHY", "Database integro e sincronizzato."
    except Exception as e:
        return "CORRUPTED", f"Errore integrità: {str(e)}"

def factory_reset():
    """Cancella tutti i dati utente e riporta l'OS allo stato iniziale."""
    # Svuota il session_state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Cancella il file fisico
    if os.path.exists("synapse_vault_vault.json"):
        os.remove("synapse_vault_vault.json")
    
    st.warning("HARD RESET COMPLETATO. Ricarica la pagina.")

def render_maintenance_ui():
    """Interfaccia di manutenzione nelle Impostazioni."""
    st.subheader("🛠️ Manutenzione Nucleo")
    
    status, msg = check_database_integrity()
    
    if status == "HEALTHY":
        st.success(f"STATO: {status} - {msg}")
    else:
        st.error(f"STATO: {status} - {msg}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Pulisci Cache Sessione"):
            st.session_state.internal_logs = []
            st.toast("Cache log pulita.")
    
    with col2:
        if st.toggle("Abilita Protocollo Reset Totale"):
            if st.button("🚨 ESEGUI WIPE TOTALE"):
                factory_reset()
                st.rerun()
