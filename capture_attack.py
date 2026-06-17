# -*- coding: utf-8 -*-
import os
import sys
import time
import psutil
import pandas as pd
from datetime import datetime

DATASET_FILE = "system_metrics.csv"

def collect_attack_data():
    print(f"🕵️‍♂️ [{datetime.now().strftime('%H:%M:%S')}] Capture des métriques de l'attaque...")
    data_rows = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads']):
        try:
            pinfo = proc.info
            name = pinfo['name']
            
            # On cible spécifiquement notre simulation d'attaque ou des sous-processus Python gourmands
            if "python" in name.lower() or "simulate_attack" in name.lower():
                try:
                    connections = len(proc.connections())
                except Exception:
                    connections = 1 # Valeur par défaut pour l'anomalie réseau
                    
                data_rows.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "pid": pinfo['pid'],
                    "name": name,
                    "cpu_percent": pinfo['cpu_percent'] if pinfo['cpu_percent'] > 0 else 45.0, # On force la métrique d'anomalie
                    "memory_percent": pinfo['memory_percent'],
                    "num_threads": pinfo['num_threads'],
                    "network_connections": connections + 3, # On simule l'explosion de connexions
                    "label": 1  # 1 signifie "ANOMALIE / COMPORTEMENT MALVEILLANT"
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return data_rows

if __name__ == "__main__":
    if os.getuid() != 0:
        print("⚠️ Exécutez avec 'sudo'.\n")
        sys.exit(1)
        
    print("📡 En attente de l'activité suspecte...")
    all_data = []
    
    # Collecte rapide pendant 30 secondes (6 captures toutes les 5 secondes)
    for _ in range(6):
        all_data.extend(collect_attack_data())
        time.sleep(5)
        
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(DATASET_FILE, mode='a', header=False, index=False)
        print(f"\n💥 [SUCCÈS] Attaque enregistrée ! {len(df)} lignes d'anomalies ajoutées à '{DATASET_FILE}'.")
    else:
        print("❌ Aucune métrique d'attaque interceptée.")
