# -*- coding: utf-8 -*-
import os
import sys
import psutil

# Liste des ports normalement autorisés
AUTHORIZED_PORTS = [8501, 22]

def check_root_users():
    print("🔍 [AUDIT] Vérification des utilisateurs disposant des privilèges ROOT...")
    suspicious_users = []
    try:
        with open("/etc/passwd", "r") as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split(":")
            if len(parts) >= 3:
                username = parts[0]
                uid = parts[2]
                if uid == "0" and username != "root":
                    suspicious_users.append(username)
        if suspicious_users:
            print(f"⚠️ [ALERTE] Utilisateur(s) suspect(s) détecté(s) avec l'UID 0 : {suspicious_users}")
        else:
            print("✅ [CONFORMITÉ] Aucun utilisateur clandestin avec privilèges ROOT détecté.")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de /etc/passwd : {e}")

def remediate_port(port, pid):
    """ Action corrective : Identifie le processus et le neutralise """
    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()
        print(f"🔥 [REMEDIATION] Tentative d'isolement du port {port} (Processus: {proc_name}, PID: {pid})...")
        
        # Arrêt forcé du processus suspect
        proc.terminate()
        proc.wait(timeout=3)
        print(f"🛡️ [SUCCÈS] Le processus suspect '{proc_name}' (PID: {pid}) a été neutralisé. Port {port} fermé.")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
        print(f"❌ [ÉCHEC] Impossible de couper automatiquement le PID {pid} : {e}")

def check_open_ports():
    print("\n🔍 [AUDIT] Analyse des connexions réseau et des ports en écoute...")
    suspicious_found = False
    
    try:
        connections = psutil.net_connections(kind='inet')
        
        for conn in connections:
            if conn.status == 'LISTEN':
                port = conn.laddr.port
                if port not in AUTHORIZED_PORTS:
                    suspicious_found = True
                    pid = conn.pid
                    if pid:
                        print(f"⚠️ [ALERTE] Port non autorisé en écoute détecté : {port} (Géré par le PID : {pid})")
                        # Déclenchement automatique de la remédiation !
                        remediate_port(port, pid)
                    else:
                        print(f"⚠️ [ALERTE] Port non autorisé en écoute détecté : {port} (PID introuvable)")
                        
        if not suspicious_found:
            print("✅ [CONFORMITÉ] Aucun port suspect ouvert sur la machine.")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des ports : {e}")

if __name__ == "__main__":
    if os.getuid() != 0:
        print("⚠️ Attention : Ce script de remédiation système doit être exécuté avec 'sudo'.\n")
        sys.exit(1)
        
    check_root_users()
    check_open_ports()
