# -*- coding: utf-8 -*-
import streamlit as st
import os
import pandas as pd

# Configuration de la page Streamlit
st.set_page_config(
    page_title="ZARM - SecOps Dashboard",
    page_icon="🛡️",
    layout="wide"
)

LOG_FILE = "zarm_security.log"

def parse_logs(file_path):
    """ Analyse le fichier de log pour extraire les données """
    log_data = []
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=["Horodatage", "Niveau", "Message"])
        
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            # Format attendu : [YYYY-MM-DD HH:MM:SS] [LEVEL] Message
            if line.startswith("[") and "]" in line:
                try:
                    parts = line.split("] ", 2)
                    timestamp = parts[0].replace("[", "")
                    level_part = parts[1].replace("[", "")
                    message = parts[2].strip()
                    
                    log_data.append({
                        "Horodatage": timestamp,
                        "Niveau": level_part,
                        "Message": message
                    })
                except Exception:
                    continue
                    
    return pd.DataFrame(log_data)

# --- TITRE PRINCIPAL ---
st.title("🛡️ Zero-Trust Auto-Remediation Monitor (ZARM)")
st.subheader("Système d'Audit en Temps Réel & Remédiation Automatisée")
st.markdown("---")

# Chargement des données
df_logs = parse_logs(LOG_FILE)

if df_logs.empty:
    st.info("💡 Aucun log détecté pour le moment. Exécutez le script 'monitor.py' pour générer des données.")
else:
    # --- METRIQUES / KPI ---
    total_audits = len(df_logs[df_logs["Message"].str.contains("DEMARRAGE")])
    total_alertes = len(df_logs[df_logs["Niveau"] == "WARNING"])
    total_succes = len(df_logs[df_logs["Message"].str.contains("neutralisé")])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="📊 Audits Système Exécutés", value=total_audits)
        
    with col2:
        # Si des alertes existent, on affiche en rouge/orange
        st.metric(label="⚠️ Menaces Réseau Détectées", value=total_alertes, 
                  delta=f"{total_alertes} critique(s)" if total_alertes > 0 else "0", delta_color="inverse")
        
    with col3:
        st.metric(label="🛡️ Remédiations Automatiques Réussies", value=total_succes,
                  delta="Système Sécurisé" if total_succes == total_alertes and total_succes > 0 else None)

    st.markdown("---")

    # --- CONTROLE & AFFICHAGE DES LOGS ---
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.write("### ⚙️ Filtres de Supervision")
        niveau_filtre = st.multiselect(
            "Filtrer par niveau de criticité :",
            options=df_logs["Niveau"].unique(),
            default=df_logs["Niveau"].unique()
        )
        
        # Filtrage du DataFrame
        df_filtre = df_logs[df_logs["Niveau"].isin(niveau_filtre)]
        
        st.write("### 🚨 État du Système")
        if total_alertes > 0:
            st.error(f"Action requise : {total_alertes} tentative(s) d'intrusion ou anomalie(s) neutralisée(s).")
        else:
            st.success("Conformité Maximale : Aucun port ou utilisateur suspect actif.")

    with col_right:
        st.write(f"### 📋 Registre des Événements ({len(df_filtre)} lignes)")
        
        # Fonction pour colorer le tableau selon la criticité
        def color_level(val):
            if val == "WARNING":
                return "background-color: #ff4b4b; color: white;"
            elif val == "ERROR":
                return "background-color: #ff9292; color: black;"
            elif val == "INFO":
                return "background-color: #2e7d32; color: white;"
            return ""

        # Affichage du tableau stylisé
        st.dataframe(
            df_filtre.style.map(color_level, subset=["Niveau"]),
            use_container_width=True,
            hide_index=True
        )

# Bouton de rafraîchissement manuel
if st.button("🔄 Actualiser le Dashboard"):
    st.rerun()
