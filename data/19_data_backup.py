"""
SYNAPSE NEURAL OS - BACKUP & EXPORT SYSTEM
------------------------------------------
File 19/35 | data/19_data_backup.py
Posizione: /data/19_data_backup.py

DESCRIZIONE:
Genera file scaricabili per l'utente. Gestisce l'esportazione 
del Vault e della cronologia chat in formati leggibili (.txt, .json).
"""

import streamlit as st
import json
from datetime import datetime

def generate_text_export():
    """
    Trasforma l'intero database dell'utente in un diario testuale elegante.
    """
    user = st.session_state.get('user_profile', {})
    vault = st.session_state.get('vault_data', [])
    chat = st.session_state.get('chat_history', [])
    
    export_str = f"=== SYNAPSE NEURAL OS EXPORT - {datetime.now().strftime('%d/%m/%Y')} ===\n"
    export_str += f"OPERATORE: {user.get('nickname', 'N/A')}\n"
    export_str += f"SETTORE: {user.get('sector', 'N/A')}\n"
    export_str += f"{'='*50}\n\n"
    
    export_str += "--- ARCHIVIO VAULT ---\n"
    for entry in vault:
        export_str += f"[{entry['timestamp']}] {entry['title']} ({entry['category']})\n"
        export_str += f"Contenuto: {entry['content']}\n"
        export_str += f"{'-'*30}\n"
    
    export_str += "\n--- CRONOLOGIA NEURALE (CHAT) ---\n"
    for msg in chat:
        role = "IO" if msg['role'] == "user" else "SYNAPSE"
        export_str += f"{role}: {msg['content']}\n"
    
    return export_str

def get_backup_json():
    """Ritorna il JSON completo per il download del backup grezzo."""
    data = {
        "profile": st.session_state.get('user_profile'),
        "vault": st.session_state.get('vault_data'),
        "chat": st.session_state.get('chat_history')
    }
    return json.dumps(data, indent=4)

def render_backup_ui():
    """Mostra i pulsanti di download nella pagina impostazioni o dashboard."""
    st.markdown("### 📥 Esportazione Dati")
    
    col1, col2 = st.columns(2)
    
    with col1:
        txt_data = generate_text_export()
        st.download_button(
            label="📄 Scarica Diario (.txt)",
            data=txt_data,
            file_name=f"synapse_export_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
        
    with col2:
        json_data = get_backup_json()
        st.download_button(
            label="📦 Backup Integrale (.json)",
            data=json_data,
            file_name=f"synapse_backup_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
