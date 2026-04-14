"""
SYNAPSE NEURAL OS - SOCIAL NEXUS
--------------------------------
File 25/35 | social/25_social_nexus.py
Posizione: /social/25_social_nexus.py

DESCRIZIONE:
Database dei contatti e delle relazioni. Fornisce all'IA le informazioni 
necessarie per identificare le persone menzionate nel diario.
"""

import streamlit as st
from ui.08_ui_components import section_header, glass_card

def render_social_nexus():
    """Rendering del modulo contatti."""
    section_header("Social Nexus", icon="👥")

    if 'social_contacts' not in st.session_state:
        st.session_state.social_contacts = []

    # 1. INPUT NUOVO CONTATTO
    with st.expander("➕ AGGIUNGI NUOVO PROFILO"):
        col_name, col_rel = st.columns([2, 1])
        with col_name:
            name = st.text_input("Nome/Nickname")
        with col_rel:
            rel = st.selectbox("Relazione", ["Amico", "Famiglia", "Lavoro", "Partner", "Altro"])
        
        bio = st.text_area("Note e informazioni chiave (es. carattere, interessi)")
        
        if st.button("SINCRONIZZA PROFILO"):
            if name:
                new_contact = {"name": name, "rel": rel, "bio": bio}
                st.session_state.social_contacts.append(new_contact)
                st.success(f"Profilo di {name} aggiunto al Nexus.")
                st.rerun()

    st.divider()

    # 2. VISUALIZZAZIONE CONTATTI
    if not st.session_state.social_contacts:
        st.info("Nessun contatto registrato nel Nexus.")
    else:
        # Griglia di contatti
        cols = st.columns(2)
        for i, contact in enumerate(st.session_state.social_contacts):
            with cols[i % 2]:
                glass_card(
                    f"{contact['name']} ({contact['rel']})",
                    contact['bio']
                )
                if st.button(f"Rimuovi {contact['name']}", key=f"rel_{i}"):
                    st.session_state.social_contacts.pop(i)
                    st.rerun()

def get_contact_context():
    """Ritorna una stringa con tutti i contatti per il System Prompt dell'IA."""
    contacts = st.session_state.get('social_contacts', [])
    if not contacts: return "Nessun contatto noto."
    
    ctx = "L'utente conosce queste persone: "
    for c in contacts:
        ctx += f"{c['name']} ({c['rel']}: {c['bio']}); "
    return ctx
