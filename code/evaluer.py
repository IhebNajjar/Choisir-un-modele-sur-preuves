import csv
import json
import os
import sys
import time
from pathlib import Path
from classifieur import CONSIGNE, classer
from evaluation import afficher_rapport

PAUSE = 2.1  # Quota palier gratuit Groq : 30 requêtes/minute max

def charger(chemin=None):
    """Charge le fichier tickets.csv."""
    if chemin is None:
        chemin = Path(__file__).resolve().parent.parent / "data" / "tickets.csv"
    with open(chemin, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def evaluer(modele, lignes, consigne=CONSIGNE, etiquette=None, nom_fichier=None):
    """Évalue un modèle sur les tickets et enregistre les résultats en JSON."""
    etiquette = etiquette or modele
    vrais, predits = [], []
    debut = time.time()
    total = len(lignes)

    print(f"\nEvaluation en cours ({total} tickets) pour {etiquette}...")
    for i, ligne in enumerate(lignes):
        pred = classer(ligne["texte"], modele, consigne=consigne)
        predits.append(pred)
        vrais.append(ligne["categorie"])
        if (i + 1) % 10 == 0 or (i + 1) == total:
            print(f"  {i + 1}/{total}", flush=True)
        time.sleep(PAUSE)

    resume = afficher_rapport(etiquette, vrais, predits)
    resume.update({
        "modele": modele,
        "etiquette": etiquette,
        "duree_s": round(time.time() - debut, 1),
        "predits": predits,
        "vrais": vrais,
        "ids": [l["id"] for l in lignes]
    })

    dossier_resultats = Path(__file__).resolve().parent.parent / "resultats"
    dossier_resultats.mkdir(exist_ok=True)

    if nom_fichier is None:
        nom_fichier = f"{modele.replace('/', '_')}.json"
    fichier_sortie = dossier_resultats / nom_fichier

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)

    print(f"\nResultats enregistres dans : {fichier_sortie}\n")
    return resume

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluer.py <modele>")
        sys.exit(1)
    modele_choisi = sys.argv[1]
    evaluer(modele_choisi, charger())
