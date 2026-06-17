# -*- coding: utf-8 -*-
import os
import sys
import psutil
import logging
import joblib
import pandas as pd
from datetime import datetime

# --- CONFIGURATION DU SYSTEME DE LOGS ---
LOG_FILE = "zarm_security.log"
MODEL_FILE = "zarm_ia_model.pkl"

logger = logging.getLogger("ZARM")
logger.setLevel(logging.INFO)
log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Éviter de dupliquer les handlers si le script tourne en boucle
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

# --- CHARGEMENT DU CERVEAU IA ---
if not os.path.exists(MODEL_FILE):
    print(f"❌ Erreur : Le modèle IA '{MODEL_FILE}' est introuvable. Entraînez-le d'abord.")
    sys.exit(1)

ia_model = joblib.load(MODEL_FILE)
# ----------------------------------------

def check_root_users():
    logger.info("🔍 [AUDIT-SYS] Vérification des privilèges ROOT...")
    try:
        with open("/etc/passwd", "r") as f:
            for line in f.readlines():
                parts = line.strip().split(":")
                if len(parts) >= 3 and parts[2] == "0" and parts[0] != "root":
                    logger.warning(f"⚠️ [ALERTE] Utilisateur clandestin ROOT détecté : {parts[0]}")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'audit utilisateurs : {e}")

def remediate_process(proc_name, pid):
    """ Action corrective automatique face à l'IA """
    try:
        proc = psutil.Process(pid)
        logger.warning(f"🔥 [REMEDIATION-IA] Neutralisation immédiate de la menace détectée par l'IA (Nom: {proc_name}, PID: {pid})...")
        proc.terminate()
        proc.wait(timeout=3)
        logger.info(f"🛡️ [SUCCÈS-IA] Menace '{proc_name}' (PID: {pid}) neutralisée avec succès.")
    except Exception as e:
        logger.error(f"❌ [ÉCHEC-IA] Impossible de stopper le PID {pid} : {e}")

def check_system_anomalies_with_ia():
    logger.info("🔍 [AUDIT-IA] Analyse comportementale des processus par Machine Learning...")
    anomalies_detected = False
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads']):
        try:
            pinfo = proc.info
            pid = pinfo['pid']
            name = pinfo['name']
            
            # Ne pas s'auto-analyser ou analyser le serveur Streamlit pour éviter les faux positifs en boucle
            if pid == os.getpid() or "streamlit" in name.lower():
                continue
                
            try:
                # Version moderne pour éviter le DeprecationWarning
                connections = len(proc.net_connections())
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                connections = 0
                
            # Préparation des caractéristiques pour la prédiction de l'IA
            features = pd.DataFrame([{
                "cpu_percent": pinfo['cpu_percent'],
                "memory_percent": pinfo['memory_percent'],
                "num_threads": pinfo['num_threads'],
                "network_connections": connections
            }])
            
            # L'IA rend son verdict
            prediction = ia_model.predict(features)[0]
            
            if prediction == 1:
                anomalies_detected = True
                logger.warning(f"🚨 [ALERTE-IA] Comportement ANORMAL détecté sur le processus '{name}' (PID: {pid}) !")
                remediate_process(name, pid)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    if not anomalies_detected:
        logger.info("✅ [CONFORMITÉ-IA] Tous les processus actifs respectent la baseline comportementale.")

if __name__ == "__main__":
    if os.getuid() != 0:
        print("⚠️ Attention : Ce script de supervision doit être exécuté avec 'sudo'.\n")
        sys.exit(1)
        
    logger.info("=== DEMARRAGE DE L'AUDIT DE SECURITE INTELLIGENT ZARM-IA ===")
    check_root_users()
    check_system_anomalies_with_ia()
    logger.info("=== FIN DE L'AUDIT DE SECURITE ===\n")
