import json
from pathlib import Path

resultats_dir = Path(__file__).resolve().parent.parent / "resultats"
resultats = {}

for fichier in sorted(resultats_dir.glob("*.json")):
    with open(fichier, encoding="utf-8") as f:
        r = json.load(f)
        resultats[r["etiquette"]] = r

etiquettes = list(resultats.keys())

if not etiquettes:
    print("Aucun fichier de resultat trouve dans", resultats_dir)
    exit(0)

# Tri par macro_f1 décroissant
modeles_tries = sorted(resultats.items(), key=lambda item: item[1]["macro_f1"], reverse=True)
meilleur_score = modeles_tries[0][1]["macro_f1"]

print("\n" + "=" * 92)
print("COMPARAISON DES MODELES (Tries par Macro-F1)")
print("=" * 92)
print(f"{'Rang':<5} {'Modele':<32} {'Accuracy':>9} {'Macro-F1':>9} {'Invalides':>10} {'Duree (s)':>10} {'Ecart (pts)':>12}")
print("-" * 92)

for rang, (etiquette, data) in enumerate(modeles_tries, 1):
    inv = data.get("invalides", 0.0)
    ecart_pts = (meilleur_score - data["macro_f1"]) * 100
    ecart_tickets = ecart_pts / (100.0 / 72.0)  # 1 ticket = 100/72 ≈ 1.389 pt
    if rang == 1:
        ecart_str = "Leader"
    else:
        ecart_str = f"-{ecart_pts:.1f} pts (~{ecart_tickets:.1f} tks)"

    print(f"#{rang:<4} {etiquette:<32} {data['accuracy']:>9.3f} {data['macro_f1']:>9.3f} {inv:>10.3f} {data['duree_s']:>10.1f} {ecart_str:>12}")

print("\n" + "-" * 92)
print("Note regle du cours : 1 ticket = 1.39 pt de macro-F1 (100/72).")
print("Seuil significatif : ecart >= 5 tickets (soit ~7 points). En dessous, ecart non significatif.")
print("-" * 92)

print("\n" + "=" * 92)
print("DESACCORDS ENTRE MODELES")
print("=" * 92)
if len(etiquettes) >= 2:
    premier = etiquettes[0]
    total_desaccords = 0
    ids = resultats[premier]["ids"]
    vrais = resultats[premier].get("vrais", [])

    for i, id_ticket in enumerate(ids):
        predictions = [resultats[e]["predits"][i] for e in etiquettes]
        if len(set(predictions)) > 1:
            total_desaccords += 1
            vrai = vrais[i] if i < len(vrais) else "?"
            preds_str = " | ".join(f"{e[:14]}={p}" for e, p in zip(etiquettes, predictions))
            print(f"{id_ticket:<6} (ref: {vrai:<11}) -> {preds_str}")

    print(f"\nTotal des tickets en desaccord : {total_desaccords} / {len(ids)}")
else:
    print("Il faut au moins 2 modeles evalues pour afficher les desaccords.")
print("\n")
