# 🛡️ ZARM — Zero-Trust Auto-Remediation Monitor

ZARM est un outil de sécurité active (SecOps) développé en Python qui applique une philosophie **Zero-Trust** au niveau du système d'exploitation Linux. Il combine un audit continu des services réseau et un moteur de remédiation automatisé capable de neutraliser instantanément les menaces ou les processus non autorisés.

## ✨ Fonctionnalités
- **Audit Système en Temps Réel :** Analyse des sockets réseau et détection des connexions en état d'écoute (`LISTEN`) via `psutil`.
- **Politique Zero-Trust (Whitelist) :** Identification immédiate de tout processus non répertorié ou suspect ouvrant un port sur la machine.
- **Remédiation Active Automatique :** Neutralisation propre (`SIGTERM`) ou forcée (`SIGKILL`) des processus malveillants à la volée.
- **Dashboard SOC Dynamique :** Interface graphique interactive développée avec **Streamlit** se rafraîchissant toutes les 5 secondes avec journalisation des incidents dans un fichier de logs (`zarm_actions.log`).

## 🛠️ Architecture Technique
- **Langage :** Python 3
- **Framework UI :** Streamlit
- **Librairies clés :** `psutil`, `pandas`
- **OS Cible :** Linux (Kali Linux / Ubuntu Server)

## 🚀 Installation & Utilisation

1. Cloner le dépôt :
   ```bash
   git clone [https://github.com/ton-username/ZARM_Project.git](https://github.com/ton-username/ZARM_Project.git)
   cd ZARM_Project
