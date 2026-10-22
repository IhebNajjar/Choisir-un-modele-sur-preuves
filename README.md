# Atelier 2 — Choisir un Modèle sur Preuves
### Machine Learning Appliqué · 3e Année DSI

Ce dépôt contient la réalisation complète de l'**Atelier 2** portant sur l'évaluation rigoureuse et le choix sur preuves de modèles de langage (LLMs) pour le tri et le routage automatique de tickets de support client.

---

## 🎯 Objectif du Projet

Classifier automatiquement des tickets entrants en français vers 4 équipes :
- `facturation` : montant, facture, paiement, remboursement
- `technique` : panne, anomalie de fonctionnement
- `compte` : accès au compte, données personnelles
- `commercial` : choix d'offre, abonnement, résiliation

Le jeu de test (`data/tickets.csv`) contient **72 tickets annotés** avec une distribution volontairement déséquilibrée (`facturation` 30.6 %, `technique` 27.8 %, `compte` 22.2 %, `commercial` 19.4 %).

La métrique de décision retenue est le **Macro-F1** afin de protéger équitablement la catégorie minoritaire.

---

## 📊 Résultats du Benchmark

Les évaluations ont été menées avec une température de 0.0 et un format JSON strict imposé.

| Rang | Modèle / Configuration | Accuracy | Macro-F1 | Invalides (%) | Durée (s) | Écart vs Leader |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 **1** | **`gpt-oss-120b + 4 exemples`** *(Few-shot)* | **0.972** | **0.970** | **0.0 %** | 216.2 s | **Leader** |
| 🥈 **2** | **`qwen/qwen3.8-27b`** *(Zero-shot)* | 0.958 | 0.956 | 0.0 % | 224.1 s | -1.4 pts (~1.0 ticket) |
| 🥉 **3** | **`openai/gpt-oss-120b`** *(Zero-shot)* | 0.917 | 0.917 | 0.0 % | 493.5 s | -5.3 pts (~3.8 tickets) |
| **4** | **`openai/gpt-oss-20b`** *(Zero-shot)* | 0.903 | 0.902 | 1.4 % | 213.2 s | -6.8 pts (~4.9 tickets) |

### 💡 Enseignements Clés
1. **Le Prompt Engineering domine la taille du modèle** : Ajouter seulement 4 exemples (un par catégorie) à `gpt-oss-120b` fait passer le macro-F1 de **0.917** à **0.970** (+5.3 points, soit ~3.8 tickets en plus). Le gain apporté par le few-shot est supérieur à l'écart entre modèles en zero-shot.
2. **Efficacité Zero-shot** : En zero-shot, `qwen/qwen3.8-27b` (27B) bat largement `openai/gpt-oss-120b` (120B) tout en étant 2.2 fois plus rapide.

---

## 📁 Structure du Répertoire

```text
atelier2/
├── data/
│   └── tickets.csv                     # 72 tickets de test annotés
├── code/
│   ├── essai.py                        # Test rapide de la connexion à l'API Groq
│   ├── explorer.py                     # Analyse de la distribution du jeu de test
│   ├── classifieur.py                  # Client Groq, prompts (Zero-shot & Few-shot), gestion d'erreurs
│   ├── test_classifieur.py             # Validation fonctionnelle du classifieur
│   ├── evaluation.py                   # Calcul manuel des métriques (Accuracy, Macro-F1, Matrice)
│   ├── test_evaluation.py              # Tests unitaires des fonctions métriques
│   ├── evaluer.py                      # Moteur d'évaluation sur 72 tickets avec pause quota
│   ├── comparer.py                     # Tableau comparatif et analyse des désaccords
│   └── variante.py                     # Évaluation de la variante Few-shot
├── resultats/
│   ├── openai_gpt-oss-20b.json         # Preuve JSON modèle 1
│   ├── openai_gpt-oss-120b.json        # Preuve JSON modèle 2
│   ├── qwen_qwen3.8-27b.json           # Preuve JSON modèle 3
│   └── openai_gpt-oss-120b_variante.json # Preuve JSON variante 4 exemples
├── fiche_de_decision.md                # Synthèse et fiche de décision pour la mise en production
├── .gitignore
└── README.md
```

---

## 🚀 Reproduction des Résultats

### 1. Prérequis
```powershell
python -m pip install groq
$env:GROQ_API_KEY = "votre_cle_groq"
```

### 2. Exécution
```powershell
cd code

# Explorer les données
python explorer.py

# Évaluer les modèles
python evaluer.py openai/gpt-oss-20b
python evaluer.py openai/gpt-oss-120b
python evaluer.py qwen/qwen3.8-27b

# Évaluer la variante Few-shot
python variante.py

# Afficher la comparaison finale
python comparer.py
```
