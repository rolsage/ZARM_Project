import streamlit as st
import pandas as pd
import time
import os
from modules.audit import scan_open_ports
from modules.remediation import kill_process_by_pid

# Politique de sécurité
PROCESS_WHITELIST = ["streamlit", "containerd"]
LOG_FILE = "zarm_actions.log"

# Configuration de la page Streamlit
st.set_page_config(page_title="ZARM - SOC Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Zero-Trust Auto-Remediation Monitor (ZARM)")
st.subheader("Console de Supervision SecOps & Durcissement Système Actif")

# Séparation de l'écran en deux colonnes
col1, col2 = st.columns(2)

with col1:
    st.header("🔍 Ports Réseau et Services Actifs")
    # Exécution du scan d'audit
    ports_detectes = scan_open_ports()
    
    if ports_detectes:
        df_ports = pd.DataFrame(ports_detectes)
        
        # Logique d'évaluation et de remédiation en direct
        status_list = []
        for index, row in df_ports.iterrows():
            if row['process'] in PROCESS_WHITELIST:
                status_list.append("🟢 Conforme (Autorisé)")
            else:
                status_list.append("🚨 NON CONFORME - BLOCAGE")
                # Déclenchement immédiat de la remédiation automatique
                kill_process_by_pid(row['pid'], row['process'])
                
        df_ports['Statut'] = status_list
        st.dataframe(df_ports, use_container_width=True)
    else:
        st.info("Aucun port ouvert détecté.")

with col2:
    st.header("📜 Historique des Remédiations (Logs)")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()
        # Afficher les dernières lignes de log en haut
        st.text_area("Journal d'audit système", "".join(logs[::-1]), height=300)
    else:
        st.info("Aucune action de remédiation enregistrée pour le moment.")

# Système de rafraîchissement automatique toutes les 5 secondes
st.write("---")
st.caption("🔄 Actualisation automatique du moniteur système toutes les 5 secondes...")
time.sleep(5)
st.rerun()
