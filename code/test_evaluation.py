from evaluation import (
    accuracy,
    scores_par_classe,
    f1_macro,
    matrice_confusion,
    afficher_rapport,
)

vrais = ["compte", "technique", "compte", "commercial"]
predits = ["compte", "technique", "commercial", "commercial"]

print("Accuracy :", accuracy(vrais, predits))
print("Scores :", scores_par_classe(vrais, predits))
print("Macro-F1 :", f1_macro(scores_par_classe(vrais, predits)))
print("Matrice :", matrice_confusion(vrais, predits))

rapport = afficher_rapport("Test Validation", vrais, predits)
