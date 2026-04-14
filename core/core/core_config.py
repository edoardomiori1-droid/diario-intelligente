"""
SYNAPSE NEURAL OS - CONFIGURATION ENGINE
----------------------------------------
File 03/35: core/core_config.py
Ruolo: Gestione delle Costanti, Limiti e Parametri Globali

Questo file centralizza i valori 'hardcoded' per evitare ridondanze. 
È il punto di riferimento per le date, i modelli AI e le impostazioni di sicurezza.
"""

import streamlit as st
from datetime import date

def get_settings():
    """
    Ritorna un dizionario globale con tutte le impostazioni del sistema.
    Separare i dati dalla logica permette di aggiornare l'app in un click.
    """
    return {
        # --- METADATI DI SISTEMA ---
        "app_name": "Synapse Neural OS",
        "version": "5.5.0-Platinum",
        "environment": "Production",
        
        # --- CONFIGURAZIONE AI (GEMINI) ---
        # Centralizzato per poter cambiare modello istantaneamente (es. da Flash a Pro)
        "ai_model": "gemini-1.5-flash",
        "ai_temperature": 0.75,     # Bilanciamento tra precisione e creatività
        "ai_max_tokens": 1200,      # Lunghezza massima delle risposte
        
        # --- FIX CALENDARIO & DATE (UNIVERSALE) ---
        # Qui risolviamo il problema del 2010 impostando i limiti del selettore
        "date_min": date(1950, 1, 1),
        "date_max": date.today(),
        "date_default": date(2010, 1, 1), # Default immediato per il target ragazzi
        
        # --- PARAMETRI RADAR (STATISTICHE) ---
        # Definiamo qui i nomi delle skill che appariranno nel grafico
        "stat_labels": ['Socialità', 'Energia', 'Rischio', 'Focus', 'Analisi'],
        "stat_min": 1,
        "stat_max": 10,
        
        # --- SETTORI OPERATIVI ---
        # Lista universale di ambiti di utilizzo per l'utente
        "user_sectors": [
            "Studente / Formazione", 
            "Gaming / Tech", 
            "Business / Career", 
            "Sport / Performance", 
            "Creatività / Design",
            "Personal Growth"
        ],
        
        # --- SICUREZZA & PRIVACY ---
        "security_level": "High (Encrypted Session)",
        "privacy_notice": "I tuoi dati neurale sono criptati e salvati localmente."
    }

def get_theme_names():
    """
    Ritorna la lista dei temi disponibili nel sistema.
    """
    return ["SYNAPSE_PRIME", "CYBER_PUNK", "NOIR_EXECUTIVE", "GHOST_SHELL"]

def get_system_tagline():
    """
    Ritorna il motto dell'applicazione visualizzabile nel footer o nel boot.
    """
    return "Synapse OS: Potenziamento Neurale per la Next-Gen."
