"""
SYNAPSE NEURAL OS - AI LOGIC PROCESSOR
-------------------------------------
File 15/35 | logic/15_logic_ai.py
Posizione: /logic/15_logic_ai.py

DESCRIZIONE:
Gestisce la costruzione dei prompt per l'IA e la comunicazione 
con il modello linguistico. Integra i dati del profilo utente 
per rendere le risposte iper-personalizzate.
"""

import streamlit as st

def get_system_context():
    """
    Costruisce il 'carattere' dell'IA basandosi sui dati dell'operatore.
    Questo rende l'IA consapevole di chi sei e di cosa deve fare.
    """
    user = st.session_state.get('user_profile', {})
    nickname = user.get('nickname', 'Sconosciuto')
    sector = user.get('sector', 'General')
    stats = user.get('stats', {})
    
    # Costruiamo il System Prompt
    prompt_base = f"""
    Sei il 'Synapse Neural OS', un'interfaccia neurale avanzata. 
    L'operatore attuale è {nickname}, specializzato nel settore {sector}.
    Le sue attitudini attuali sono: {stats}.
    
    REGOLE DI COMPORTAMENTO:
    1. Parla come un'IA futuristica, usa un tono professionale ma con un tocco Cyberpunk.
    2. Chiama l'utente 'Operatore {nickname}'.
    3. Sii conciso ma profondo nelle analisi.
    4. Se l'utente ti chiede dei suoi dati, consulta il contesto che ti ho fornito.
    5. Usa saltuariamente termini tecnici come 'sincronizzazione', 'uplink', 'buffer'.
    """
    return prompt_base

def prepare_ai_payload(user_input):
    """
    Prepara il pacchetto dati completo da inviare all'API.
    Include la cronologia della chat per dare memoria all'IA.
    """
    context = get_system_context()
    
    # Recuperiamo gli ultimi 5 messaggi per non sovraccaricare la memoria
    history = st.session_state.get('chat_history', [])[-5:]
    
    # Formattazione per Gemini/Modelli LLM
    messages = [{"role": "system", "content": context}]
    for msg in history:
        messages.append(msg)
    
    messages.append({"role": "user", "content": user_input})
    
    return messages

def process_ai_response(raw_text):
    """
    Pulisce e formatta la risposta grezza che arriva dall'IA 
    prima di visualizzarla a schermo.
    """
    # Qui potremmo aggiungere filtri per rimuovere caratteri strani
    # o per formattare automaticamente il codice Python.
    clean_text = raw_text.strip()
    return clean_text
