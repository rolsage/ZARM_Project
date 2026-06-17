# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

DATASET_FILE = "system_metrics.csv"
MODEL_FILE = "zarm_ia_model.pkl"

print("📊 Chargement du dataset système...")
df = pd.read_csv(DATASET_FILE)

# 1. Sélection des "Features" (les critères que l'IA doit analyser)
X = df[["cpu_percent", "memory_percent", "num_threads", "network_connections"]]

# 2. Sélection de la cible "Target" (ce que l'IA doit deviner)
y = df["label"]

# 3. Séparation des données : 80% pour l'entraînement, 20% pour tester l'efficacité de l'IA
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"🏋️‍♂️ Entraînement du modèle RandomForest sur {len(X_train)} échantillons...")
# Création et entraînement de l'intelligence artificielle
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Évaluation des performances de notre modèle
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n🎯 --- RÉSULTATS DE L'ENTRAÎNEMENT ---")
print(f"Précision globale de l'IA : {accuracy * 100:.2f} %")
print("\n📋 Rapport détaillé :")
print(classification_report(y_test, y_pred))

# 5. Sauvegarde du cerveau de l'IA pour l'utiliser dans notre moniteur en temps réel
joblib.dump(model, MODEL_FILE)
print(f"💾 [SUCCÈS] Le modèle IA a été entraîné et sauvegardé sous '{MODEL_FILE}' !")
