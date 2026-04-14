"""
SYNAPSE NEURAL OS - GLOBAL CONFIGURATION
----------------------------------------
File 03/35 | core/03_core_config.py
Posizione: /core/03_core_config.py

DESCRIZIONE:
Single Source of Truth (Sorgente unica di verità). 
Contiene le impostazioni dell'IA, la logica delle date e i nomi 
delle metriche per il grafico radar.
"""

import streamlit as st
from datetime import date

def get_config():
    """
    Restituisce un dizionario completo con tutte le regole del sistema.
    Facilmente richiamabile da qualsiasi altro file.
    """
    return {
        # --- INFO DI SISTEMA ---
        "metadata": {
            "name": "Synapse Neural OS",
            "version": "5.5.0-PLATINUM",
            "engine": "Gemini 1.5 Pro/Flash",
            "build": "2026-FINAL"
        },

        # --- LOGICA CALENDARIO (TARGET 2010) ---
        # Impostiamo il punto di partenza ideale per la registrazione
        "calendar": {
            "min_year": 1950,
            "max_year": date.today().year,
            "default_date": date(2010, 1, 1), # <-- FIX DATA: Apre il calendario sul 2010
            "label": "Data di Nascita Neurale"
        },

        # --- PARAMETRI IA ---
        "ai_logic": {
            "temperature": 0.8,      # Livello di creatività dell'IA
            "max_tokens": 1500,     # Lunghezza massima delle risposte
            "model": "gemini-1.5-flash"
        },

        # --- GRAFICO RADAR (SKILLS) ---
        # Definiamo qui i 5 pilastri del tuo profilo
        "radar_stats": [
            "LOGICA", 
            "CREATIVITÀ", 
            "ENERGIA", 
            "FOCUS", 
            "SOCIAL"
        ],

        # --- SETTORI DI SPECIALIZZAZIONE ---
        "sectors": [
            "Student / Education", 
            "Tech / Coding", 
            "Art / Design", 
            "Gaming / Esports", 
            "Fitness / Health",
            "Business / Startup"
        ]
    }

def get_style_constants():
    """
    Definisce i codici colore e le trasparenze per il File 06 (UI).
    """
    return {
        "main_color": "#00F2FF",      # Cyan Elettrico
        "secondary_color": "#7000FF", # Viola Deep
        "glass_opacity": 0.15,
        "blur_amount": "12px"
    }

def get_privacy_text():
    """Ritorna la nota legale standard per l'onboarding."""
    return (
        "PROTOCOLLO SICUREZZA: I dati inseriti vengono elaborati "
        "esclusivamente per la generazione del profilo locale."
    )
