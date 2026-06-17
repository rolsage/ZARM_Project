import psutil

def scan_open_ports():
    """
    Scanne le système à la recherche de toutes les connexions réseau
    qui écoutent (LISTEN) sur la machine.
    """
    open_ports = []
    
    # Récupérer toutes les connexions réseau du système
    connections = psutil.net_connections(kind='inet')
    
    for conn in connections:
        # On ne cible que les ports en attente de connexion (LISTEN)
        if conn.status == 'LISTEN':
            port = conn.laddr.port
            ip = conn.laddr.ip
            pid = conn.pid
            
            # Récupérer le nom du processus grâce à son PID
            try:
                proc = psutil.Process(pid)
                process_name = proc.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Inconnu (Accès restreint)"
                
            open_ports.append({
                "ip": ip,
                "port": port,
                "pid": pid,
                "process": process_name
            })
            
    return open_ports

if __name__ == "__main__":
    print("🔍 [TEST] Lancement d'un scan de vérification des ports...")
    ports_detectes = scan_open_ports()
    for p in ports_detectes:
        print(f"📌 Port ouvert : {p['port']} | IP : {p['ip']} | Processus : {p['process']} (PID: {p['pid']})")
