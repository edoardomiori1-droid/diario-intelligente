"""
SYNAPSE NEURAL OS - DATA ANALYSIS ENGINE
----------------------------------------
File 17/35 | logic/17_logic_analysis.py
Posizione: /logic/17_logic_analysis.py

DESCRIZIONE:
Analizza i testi inseriti dall'utente per estrarre il 'sentiment'
e identificare trend nelle statistiche neurali.
"""

import streamlit as st

def analyze_sentiment(text):
    """
    Analisi semplificata del tono dell'utente.
    Ritorna un'icona e un colore in base al mood rilevato.
    """
    positive_words = ["felice", "ottimo", "grande", "successo", "carico", "vittoria"]
    negative_words = ["stanco", "triste", "fallimento", "stress", "ansia", "difficile"]
    
    text = text.lower()
    pos_score = sum(1 for word in positive_words if word in text)
    neg_score = sum(1 for word in negative_words if word in text)
    
    if pos_score > neg_score:
        return "⚡ OTTIMIZZATO", "#00FFC8"
    elif neg_score > pos_score:
        return "⚠️ DEGRADATO", "#FF4B4B"
    else:
        return "⚖️ STABILE", "#00F2FF"

def extract_skills_update(text):
    """
    Suggerisce quali skill del radar potrebbero essere influenzate
    dal testo scritto (es. se parlo di studio -> Logica +1).
    """
    updates = {}
    keywords = {
        "LOGICA": ["studio", "codice", "matematica", "scienza", "logica"],
        "CREATIVITÀ": ["disegno", "musica", "arte", "idea", "scrittura"],
        "ENERGIA": ["sport", "allenamento", "corsa", "palestra", "azione"],
        "FOCUS": ["meditazione", "concentrazione", "lavoro", "obiettivi"],
        "SOCIAL": ["amici", "uscita", "festa", "parlato", "conosciuto"]
    }

    for skill, keys in keywords.items():
        if any(k in text.lower() for k in keys):
            updates[skill] = 1 # Incremento suggerito
            
    return updates

def get_weekly_summary():
    """
    Simula un riassunto delle attività basandosi sul numero 
    di frammenti nel Vault e messaggi in Chat.
    """
    chat_count = len(st.session_state.get('chat_history', []))
    vault_count = len(st.session_state.get('vault_data', []))
    
    return {
        "interazioni": chat_count,
        "memorie_archiviate": vault_count,
        "livello_sincronizzazione": min(100, (chat_count + vault_count) * 5)
    }
