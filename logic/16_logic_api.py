"""
SYNAPSE NEURAL OS - GOOGLE GEMINI CONNECTOR
------------------------------------------
File 16/35 | logic/16_logic_api.py
Posizione: /logic/16_logic_api.py

DESCRIZIONE:
Gestisce la comunicazione diretta con le API di Google Generative AI.
Invia i prompt preparati dal File 15 e riceve le risposte neurali.
"""

import streamlit as st
import google.generativeai as genai

def connect_to_gemini(api_key):
    """Configura la connessione con la chiave fornita."""
    try:
        genai.configure(api_key=api_key)
        # Usiamo flash per velocità o pro per profondità
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"ERRORE CONNESSIONE: {e}")
        return None

def get_neural_response(user_input):
    """
    Invia il prompt all'IA e restituisce il testo della risposta.
    Recupera la chiave API dai 'secrets' di Streamlit o dalla sessione.
    """
    # 1. Recupero API KEY (da impostare nei secrets di Streamlit)
    api_key = st.secrets.get("GOOGLE_API_KEY") or st.session_state.get("temp_api_key")
    
    if not api_key:
        return "⚠️ ERRORE: Chiave API non rilevata. Inseriscila nelle impostazioni."

    # 2. Preparazione contesto (dal File 15)
    try:
        from logic.15_logic_ai import get_system_context
        system_prompt = get_system_context()
    except ImportError:
        system_prompt = "Sei un'IA assistente."

    # 3. Avvio sessione di chat con Gemini
    model = connect_to_gemini(api_key)
    if model:
        try:
            # Creiamo la chat con la cronologia (se disponibile)
            chat = model.start_chat(history=[])
            
            # Uniamo il system prompt alla richiesta dell'utente
            full_prompt = f"{system_prompt}\n\nOPERATORE: {user_input}"
            
            response = chat.send_message(full_prompt)
            return response.text
        except Exception as e:
            return f"❌ ERRORE NEURALE: {str(e)}"
    
    return "SISTEMA OFFLINE: Impossibile contattare il nucleo IA."

def validate_key(key):
    """Verifica se la chiave inserita è formalmente corretta."""
    if len(key) < 30:
        return False
    return True
