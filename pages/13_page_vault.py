"""
SYNAPSE NEURAL OS - CYBER VAULT
-------------------------------
File 13/35 | pages/13_page_vault.py
Posizione: /pages/13_page_vault.py

DESCRIZIONE:
Sistema di archiviazione dati persistente per l'operatore.
Permette di creare, visualizzare e gestire note criptate (simulate).
"""

import streamlit as st
from datetime import datetime

# Import moduli UI e Core
try:
    from ui.09_ui_sidebar import render_sidebar
    from ui.08_ui_components import section_header, glass_card
except ImportError:
    pass

def render_vault():
    """Rendering del modulo Caveau."""
    
    # 1. SIDEBAR & HEADER
    render_sidebar()
    section_header("Cyber Vault", icon="🔐")
    
    # Inizializziamo il database del vault se non esiste
    if 'vault_data' not in st.session_state:
        st.session_state.vault_data = []

    # 2. INTERFACCIA DI INSERIMENTO
    with st.expander("➕ ARCHIVIA NUOVO FRAMMENTO"):
        col_title, col_cat = st.columns([3, 1])
        with col_title:
            note_title = st.text_input("Titolo del Frammento", placeholder="Es: Password Terminale X")
        with col_cat:
            category = st.selectbox("Categoria", ["Segreto", "Idea", "Codice", "Diario"])
        
        note_content = st.text_area("Contenuto del dato...")
        
        if st.button("CRIPTA E ARCHIVIA"):
            if note_title and note_content:
                new_entry = {
                    "id": len(st.session_state.vault_data) + 1,
                    "title": note_title,
                    "content": note_content,
                    "category": category,
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                st.session_state.vault_data.insert(0, new_entry) # Mette il più recente in alto
                st.success("Dato archiviato con successo nel Vault.")
                st.rerun()
            else:
                st.error("Compila tutti i campi per procedere.")

    st.write("") # Spaziatore

    # 3. VISUALIZZAZIONE DATI ARCHIVIATI
    if not st.session_state.vault_data:
        st.info("Il Vault è vuoto. Nessun frammento neurale rilevato.")
    else:
        # Usiamo un layout a griglia per le note
        for entry in st.session_state.vault_data:
            with st.container():
                # Icona dinamica in base alla categoria
                icon = "🌑"
                if entry['category'] == "Segreto": icon = "🔴"
                elif entry['category'] == "Idea": icon = "💡"
                elif entry['category'] == "Codice": icon = "💻"
                
                # Visualizzazione tramite Glass Card
                glass_card(
                    f"{icon} {entry['title']} | <span style='font-size:0.7em; opacity:0.5;'>{entry['timestamp']}</span>",
                    f"<b>Categoria: {entry['category']}</b><br><br>{entry['content']}"
                )
                
                # Tasto per eliminare (piccolo in fondo)
                if st.button(f"Elimina Frammento #{entry['id']}", key=f"del_{entry['id']}"):
                    st.session_state.vault_data.remove(entry)
                    st.rerun()

# Se il file viene chiamato direttamente per test
if __name__ == "__main__":
    render_vault()
