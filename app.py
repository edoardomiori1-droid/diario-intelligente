import streamlit as st
import pandas as pd
from datetime import date
import os

# Configurazione Pagina Mobile-Friendly
st.set_page_config(page_title="Diario Evolutivo", page_icon="📖")

st.title("Il Mio Diario Intelligente 🧠")

# --- AREA DI SCRITTURA ---
st.subheader("Cosa è successo oggi?")
testo_giorno = st.text_area("Scrivi qui i tuoi pensieri...", height=200)

# --- QUESTIONARIO DINAMICO ---
st.divider()
st.write("### Com'è andata?")

voto = st.slider("Voto alla giornata", 1, 10, 5)

intensita = st.select_slider(
    "Intensità delle emozioni",
    options=["Nessuna", "Lieve", "Media", "Forte", "Incredibile"]
)

# --- SALVATAGGIO ---
if st.button("Salva la giornata"):
    if testo_giorno:
        st.success("Salvato! (Nota: Al momento i dati sono temporanei, presto collegheremo il database)")
        
        # Bozza di Analisi
        st.info(f"Analisi: Oggi hai dato un {voto}/10. Domani vedremo come si evolve questa sensazione di intensità '{intensita}'.")
    else:
        st.warning("Scrivi qualcosa prima di salvare!")

# --- SPAZIO ANALISI FUTURA ---
st.divider()
st.subheader("Il tuo percorso nel tempo")
st.write("Qui appariranno i grafici e i riassunti della tua vita non appena avremo accumulato dati.")
      
