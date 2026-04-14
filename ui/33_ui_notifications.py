"""
SYNAPSE NEURAL OS - NOTIFICATION SYSTEM
---------------------------------------
File 33/35 | ui/33_ui_notifications.py
Posizione: /ui/33_ui_notifications.py

DESCRIZIONE:
Gestisce gli avvisi utente e i promemoria per la scrittura del diario.
Assicura che l'operatore non dimentichi i protocolli serali.
"""

import streamlit as st
from datetime import datetime

def check_system_notifications():
    """Controlla lo stato del sistema e genera avvisi prioritari."""
    notifications = []
    
    # 1. Promemoria Diario Serale (dalle 21:00 in poi)
    current_hour = datetime.now().hour
    if current_hour >= 21:
        # Controlla se il diario è già stato scritto oggi
        today = datetime.now().strftime("%d/%m/%Y")
        has_diary = any(today in entry.get('timestamp', '') 
                       for entry in st.session_state.get('vault_data', []) 
                       if entry.get('category') == 'Diario')
        
        if not has_diary:
            notifications.append({
                "type": "URGENTE",
                "msg": "Protocollo Revisione Serale non ancora eseguito.",
                "icon": "🌙"
            })

    # 2. Controllo Obiettivi in stallo
    if not st.session_state.get('user_goals'):
        notifications.append({
            "type": "INFO",
            "msg": "Nessun obiettivo attivo. Definire nuove missioni nel modulo Goals.",
            "icon": "🎯"
        })

    return notifications

def render_notification_hub():
    """Visualizza gli avvisi nella parte superiore della Dashboard."""
    notifs = check_system_notifications()
    
    if notifs:
        for n in notifs:
            with st.container():
                if n['type'] == "URGENTE":
                    st.error(f"{n['icon']} **{n['type']}**: {n['msg']}")
                else:
                    st.info(f"{n['icon']} **{n['type']}**: {n['msg']}")

def trigger_toast(message, icon="⚡"):
    """Metodo rapido per notifiche a scomparsa."""
    st.toast(message, icon=icon)
