# -*- coding: utf-8 -*-
import os
import sys
import time
import psutil
import pandas as pd
from datetime import datetime

DATASET_FILE = "system_metrics.csv"

def collect_system_data():
    print(f"⏳ [{datetime.now().strftime('%H:%M:%S')}] Collecte des métriques en cours...")
    data_rows = []
    
    # On parcourt tous les processus qui tournent actuellement sur Kali
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads']):
        try:
            # Récupération des informations du processus
            pinfo = proc.info
            pid = pinfo['pid']
            name = pinfo['name']
            cpu = pinfo['cpu_percent']
            memory = pinfo['memory_percent']
            threads = pinfo['num_threads']
            
            # On regarde combien de connexions réseau ce processus possède
            try:
                connections = len(proc.connections())
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                connections = 0
                
            # On ajoute une ligne de données
            data_rows.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "pid": pid,
                "name": name,
                "cpu_percent": cpu,
                "memory_percent": memory,
                "num_threads": threads,
                "network_connections": connections,
                "label": 0  # 0 signifie "Comportement Normal"
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
            
    return data_rows

if __name__ == "__main__":
    if os.getuid() != 0:
        print("⚠️ Attention : Pour collecter toutes les métriques système, exécutez avec 'sudo'.\n")
        sys.exit(1)
        
    print("🚀 Démarrage du collecteur de données ZARM-IA...")
    print("Le script va collecter l'activité de vos processus pendant 1 minute.")
    print("Laissez-le tourner...")
    
    all_data = []
    
    # On fait 12 collectes espacées de 5 secondes (soit 1 minute au total)
    for i in range(12):
        all_data.extend(collect_system_data())
        time.sleep(5)
        
    # Sauvegarde dans un fichier CSV
    df = pd.DataFrame(all_data)
    
    # Si le fichier existe déjà, on ajoute à la suite, sinon on le crée
    if not os.path.exists(DATASET_FILE):
        df.to_csv(DATASET_FILE, index=False)
    else:
        df.to_csv(DATASET_FILE, mode='a', header=False, index=False)
        
    print(f"\n✅ [SUCCÈS] Collecte terminée ! {len(df)} lignes enregistrées dans '{DATASET_FILE}'.")
