from collections import defaultdict

CATEGORIES = ["facturation", "technique", "compte", "commercial"]

def accuracy(vrais, predits):
    """Calcule l'exactitude globale (proportion de prédictions correctes)."""
    if not vrais:
        return 0.0
    return sum(1 for v, p in zip(vrais, predits) if v == p) / len(vrais)

def scores_par_classe(vrais, predits, classes=CATEGORIES):
    """Calcule précision, rappel, F1 et support pour chaque catégorie."""
    resultat = {}
    for c in classes:
        vp = sum(1 for v, p in zip(vrais, predits) if v == c and p == c)
        fp = sum(1 for v, p in zip(vrais, predits) if v != c and p == c)
        fn = sum(1 for v, p in zip(vrais, predits) if v == c and p != c)
        precision = vp / (vp + fp) if (vp + fp) else 0.0
        recall = vp / (vp + fn) if (vp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        resultat[c] = {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "support": vp + fn
        }
    return resultat

def f1_macro(scores):
    """Moyenne non pondérée des F1 de chaque catégorie."""
    if not scores:
        return 0.0
    return round(sum(d["f1"] for d in scores.values()) / len(scores), 3)

def taux_invalides(predits):
    """Part des prédictions non conformes ou marquées 'invalide'."""
    if not predits:
        return 0.0
    n = sum(1 for p in predits if p == "invalide")
    return round(n / len(predits), 3)

def matrice_confusion(vrais, predits):
    """Compte les croisements (lignes = vérité, colonnes = prédiction)."""
    mat = defaultdict(lambda: defaultdict(int))
    for v, p in zip(vrais, predits):
        mat[v][p] += 1
    return dict(mat)

def afficher_rapport(etiquette, vrais, predits):
    """Affiche un résumé clair et retourne un dictionnaire sérialisable en JSON."""
    scores = scores_par_classe(vrais, predits)
    f1m = f1_macro(scores)
    acc = accuracy(vrais, predits)
    inv = taux_invalides(predits)

    print(f"\n=== {etiquette} ===")
    print(f"accuracy  : {acc:.3f}")
    print(f"macro-F1  : {f1m:.3f}")
    print(f"invalides : {inv:.3f}\n")

    print(f"{'categorie':<13} {'precision':>10} {'recall':>10} {'F1':>10} {'n':>5}")
    for cat in CATEGORIES:
        s = scores[cat]
        print(f"{cat:<13} {s['precision']:>10.3f} {s['recall']:>10.3f} {s['f1']:>10.3f} {s['support']:>5}")

    print("\nConfusion matrix (lignes = vérité, colonnes = prédiction)")
    mat = matrice_confusion(vrais, predits)
    cols = list(CATEGORIES)
    if any(p == "invalide" for p in predits):
        cols.append("invalide")

    header = f"{'':13} " + " ".join(f"{c[:6]:>7}" for c in cols)
    print(header)
    for cat_true in CATEGORIES:
        row_vals = " ".join(f"{mat.get(cat_true, {}).get(c, 0):>7}" for c in cols)
        print(f"{cat_true:<13} {row_vals}")

    return {
        "accuracy": round(acc, 3),
        "macro_f1": f1m,
        "invalides": inv,
        "scores": scores,
        "matrice": {str(k): dict(v) for k, v in mat.items()}
    }
