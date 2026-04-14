"""
SYNAPSE NEURAL OS - GLOBAL SEARCH ENGINE
----------------------------------------
File 32/35 | logic/32_logic_search.py
Posizione: /logic/32_logic_search.py

DESCRIZIONE:
Sistema di ricerca centralizzato. Permette di trovare informazioni 
attraverso tutti i moduli dell'OS (Vault, Social, Goals, Diario).
"""

import streamlit as st
from ui.08_ui_components import section_header, glass_card

def perform_global_search(query):
    """Esegue la ricerca in tutti i compartimenti dati."""
    if not query or len(query) < 2:
        return None

    query = query.lower()
    results = {
        "Vault": [],
        "Persone": [],
        "Obiettivi": [],
        "Diario": []
    }

    # 1. Cerca nel Vault & Diario
    for entry in st.session_state.get('vault_data', []):
        if query in entry['title'].lower() or query in entry['content'].lower():
            if entry['category'] == "Diario":
                results["Diario"].append(entry)
            else:
                results["Vault"].append(entry)

    # 2. Cerca nel Social Nexus
    for contact in st.session_state.get('social_contacts', []):
        if query in contact['name'].lower() or query in contact['bio'].lower():
            results["Persone"].append(contact)

    # 3. Cerca negli Obiettivi
    for goal in st.session_state.get('user_goals', []):
        if query in goal['title'].lower() or query in goal['desc'].lower():
            results["Obiettivi"].append(goal)

    return results

def render_search_interface():
    """Interfaccia grafica per la ricerca globale."""
    section_header("Neural Search", icon="🔍")
    
    search_query = st.text_input("Inserisci termine di ricerca...", placeholder="Cerca persone, note o ricordi...")
    
    if search_query:
        res = perform_global_search(search_query)
        
        # Visualizzazione Risultati
        found = False
        for category, items in res.items():
            if items:
                found = True
                st.subheader(f"{category} ({len(items)})")
                for item in items:
                    title = item.get('title') or item.get('name')
                    content = item.get('content') or item.get('bio') or item.get('desc')
                    glass_card(title, content)
        
        if not found:
            st.warning(f"Nessuna corrispondenza trovata per '{search_query}' nei database neurali.")
