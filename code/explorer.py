import csv
from collections import Counter
from pathlib import Path

# Résout le chemin du fichier tickets.csv (fonctionne quel que soit le dossier courant)
chemin_csv = Path(__file__).resolve().parent.parent / "data" / "tickets.csv"

with open(chemin_csv, encoding="utf-8") as f:
    lignes = list(csv.DictReader(f))

print(f"Total de tickets : {len(lignes)}\n")

for cat, n in Counter(l["categorie"] for l in lignes).most_common():
    pct = 100 * n / len(lignes)
    print(f"{cat:<13} {n:>3} {pct:>5.1f}% {'#' * n}")
