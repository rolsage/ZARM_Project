import psutil
import logging

# Configuration d'un fichier de log pour garder une trace des actions de sécurité
logging.basicConfig(
    filename='zarm_actions.log',
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def kill_process_by_pid(pid, process_name="Inconnu"):
    """
    Neutralise un processus suspect en utilisant son PID
    et enregistre l'action dans les logs de sécurité.
    """
    try:
        # Cibler le processus
        proc = psutil.Process(pid)
        
        # Enregistrer l'action de remédiation
        message = f"🔴 [REMEDIATION] Tentative de neutralisation du processus suspect : {process_name} (PID: {pid})"
        print(message)
        logging.info(message)
        
        # Terminer le processus proprement, puis de force si nécessaire
        proc.terminate()
        proc.wait(timeout=3)
        
        success_msg = f"🔒 [SUCCÈS] Le processus {process_name} (PID: {pid}) a été arrêté avec succès."
        print(success_msg)
        logging.info(success_msg)
        return True
        
    except psutil.NoSuchProcess:
        err_msg = f"⚠️ [ERREUR] Impossible de tuer le PID {pid} : le processus n'existe plus."
        print(err_msg)
        logging.warning(err_msg)
        return False
    except psutil.AccessDenied:
        err_msg = f"❌ [ÉCHEC] Privilèges insuffisants pour arrêter le PID {pid} ({process_name})."
        print(err_msg)
        logging.error(err_msg)
        return False
    except psutil.TimeoutExpired:
        # Si le processus refuse de s'arrêter proprement, on force le kill
        proc.kill()
        force_msg = f"⚡ [FORCE] Le processus {process_name} (PID: {pid}) a été tué de force (SIGKILL)."
        print(force_msg)
        logging.info(force_msg)
        return True

if __name__ == "__main__":
    print("🛠️ [TEST] Module de remédiation chargé. Prêt à intervenir.")
