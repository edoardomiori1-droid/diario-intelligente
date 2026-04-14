"""
SYNAPSE NEURAL OS - MATRIX NOTEPAD
----------------------------------
File 23/35 | tools/23_tool_notepad.py
Posizione: /tools/23_tool_notepad.py

DESCRIZIONE:
Un'area di testo libera per appunti temporanei.
I dati vengono mantenuti nella sessione ma non sporcano il Vault ufficiale.
"""

import streamlit as st
from ui.08_ui_components import section_header

def render_notepad():
    """Rendering dell'interfaccia Notepad."""
    section_header("Matrix Notepad", icon="📝")
    
    # Inizializzazione buffer se vuoto
    if 'notepad_buffer' not in st.session_state:
        st.session_state.notepad_buffer = ""

    st.caption("Buffer temporaneo a scrittura rapida. I dati non sono criptati nel Vault.")

    # Editor di testo a tutto schermo (o quasi)
    note_input = st.text_area(
        label="Comando: SCRIVI_PENSIERI_QUI",
        value=st.session_state.notepad_buffer,
        height=400,
        placeholder="Digita qui i tuoi dati volatili...",
        key="main_notepad_area"
    )

    # Salvataggio automatico nel session_state
    st.session_state.notepad_buffer = note_input

    col_save, col_clear, _ = st.columns([1, 1, 2])
    
    with col_save:
        if st.button("💾 FISSA NEL BUFFER"):
            st.toast("Dati sincronizzati nel buffer di sessione.")
    
    with col_clear:
        if st.button("🗑️ WIPE DATA"):
            st.session_state.notepad_buffer = ""
            st.rerun()

    st.divider()
    
    # Feature "Quick Move": Sposta al Vault
    if st.session_state.notepad_buffer:
        st.subheader("📤 Esportazione Rapida")
        if st.button("Sposta nel Cyber Vault come 'Nota Rapida'"):
            # Logica di migrazione al File 13
            new_entry = {
                "id": len(st.session_state.get('vault_data', [])) + 1,
                "title": f"Quick Note {st.session_state.notepad_buffer[:15]}...",
                "content": st.session_state.notepad_buffer,
                "category": "Idea",
                "timestamp": st.session_state.get('current_time', 'Ora')
            }
            if 'vault_data' not in st.session_state:
                st.session_state.vault_data = []
            st.session_state.vault_data.insert(0, new_entry)
            st.session_state.notepad_buffer = "" # Pulisce dopo lo spostamento
            st.success("Nota migrata nel Vault con successo!")
            st.rerun()
