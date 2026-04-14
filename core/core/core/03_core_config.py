"""
SYNAPSE NEURAL OS - CONFIGURATION & SETTINGS
--------------------------------------------
File 03/35 | core/03_core_config.py
Ruolo: Gestione centralizzata di costanti e parametri universali.

Questo file funge da 'Single Source of Truth'. Contiene le regole 
matematiche per il grafico radar, i settaggi dell'IA e i limiti 
temporali per i calendari (target 2010).
"""

import streamlit as st
from datetime import date

def get_settings():
    """
    Ritorna un dizionario completo con tutte le configurazioni.
    Organizzato per aree tematiche.
    """
    return {
        # --- INFO DI SISTEMA ---
        "system": {
            "os_name": "Synapse Neural OS",
            "version": "5.5.0-PLATINUM",
            "developer": "Universal Edition",
            "update_year": 2026
        },

        # --- PARAMETRI IA (GEMINI ENGINE) ---
        # Centralizzato per switch rapidi tra modelli
        "ai": {
            "model_name": "gemini-1.5-flash",
            "temperature": 0.7,      # Bilanciamento creatività/precisione
            "max_tokens": 1200,      # Lunghezza risposte
            "system_prompt": "Sei l'Intelligenza Centrale di Synapse OS. Sei concisa e brillante."
        },

        # --- LOGICA CALENDARIO (TARGET 2010) ---
        # Questo risolve il problema della selezione della data per i ragazzi
        "date_logic": {
            "min_date": date(1950, 1, 1),      # Limite minimo
            "max_date": date.today(),           # Limite massimo (oggi)
            "default_year": date(2010, 1, 1),  # PUNTO DI PARTENZA: 2010
        },

        # --- STRUTTURA RADAR (SKILLS) ---
        # Queste sono le 5 punte del tuo grafico delle statistiche
        "radar_labels": [
            "SOCIAL (Connessione)", 
            "FOCUS (Concentrazione)", 
            "ENERGY (Vitalità)", 
            "RISK (Coraggio)", 
            "LOGIC (Analisi)"
        ],

        # --- SETTORI OPERATIVI (ONBOARDING) ---
        "sectors": [
            "Student / Learning", 
            "Tech / Development", 
            "Creative / Design", 
            "Esports / Gaming", 
            "Fitness / Sport",
            "Personal Growth"
        ]
    }

def get_style_config():
    """Ritorna i parametri per l'estetica del sistema."""
    return {
        "primary_color": "#00FFC8",  # Verde Neon/Cyan
        "background_blur": "12px",
        "border_radius": "15px",
        "glass_opacity": 0.1
    }

def get_security_notice():
    """Testo universale per la privacy."""
    return "SISTEMA CRITTOGRAFATO: I dati inseriti rimangono locali per la sessione corrente."
