# -*- coding: utf-8 -*-
import time
import socket
import threading

def cpu_stress():
    # Simule une forte activité CPU (calculs inutiles en boucle)
    print("🔥 [ATTACK SIM] Stress CPU activé...")
    while True:
        _ = 25 * 25

def network_stress():
    # Simule des connexions réseau répétées (recherche de ports ouverts / scan)
    print("🌐 [ATTACK SIM] Connexions réseau suspectes activées...")
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            # Tente de se connecter sur un port local aléatoire
            s.connect(("127.0.0.1", 4444))
            s.close()
        except Exception:
            pass
        time.sleep(0.1)

if __name__ == "__main__":
    print("⚠️ DÉMARRAGE DE LA SIMULATION D'ANOMALIE [NOM : backdoor_simulation] ⚠️")
    
    # Lancement des deux activités suspectes dans des threads séparés
    t1 = threading.Thread(target=cpu_stress, daemon=True)
    t2 = threading.Thread(target=network_stress, daemon=True)
    
    t1.start()
    t2.start()
    
    # Garde le script actif pendant 40 secondes
    time.sleep(40)
    print("🛑 Fin de la simulation d'attaque.")
