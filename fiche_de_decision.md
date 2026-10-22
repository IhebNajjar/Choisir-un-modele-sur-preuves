# Fiche de Décision — Atelier 2 : Choisir un Modèle sur Preuves

**Auteur** : Étudiant DSI-31  
**Date** : 22/10/2026  
**Projet** : Guichet automatique de tri et routage de tickets clients  

---

## 1. Contexte, Tâche et Jeu de Test

- **Tâche** : Classifier automatiquement les requêtes entrantes vers 4 équipes cibles :
  - `facturation` (montant, facture, paiement, remboursement)
  - `technique` (panne, anomalie de fonctionnement)
  - `compte` (accès, mot de passe, données personnelles)
  - `commercial` (offres, abonnements, résiliation)
- **Jeu de test** : 72 tickets annotés à la main (`tickets.csv`), rédigés en conditions réelles (fautes, style SMS, messages courts ou ambigus).
- **Distribution des classes** :
  - `facturation` : 22 tickets (30.6 %)
  - `technique` : 20 tickets (27.8 %)
  - `compte` : 16 tickets (22.2 %)
  - `commercial` : 14 tickets (19.4 %) — *classe minoritaire*

---

## 2. Métrique de Décision Retenue

- **Métrique choisie** : **Macro-F1** (fixée **avant** de voir les résultats des modèles).
- **Justification** :  
  L'accuracy globale est trompeuse en présence de classes déséquilibrées. Un modèle ignorant la catégorie minoritaire (`commercial`, 19.4 %) pourrait quand même atteindre plus de 80 % d'accuracy tout en pénalisant gravement le service commercial.  
  Le macro-F1 calcule la moyenne arithmétique non pondérée des F1 de chaque catégorie, garantissant que chaque équipe est protégée de manière équitable.
- **Règle de décision** :  
  Sur 72 tickets, 1 ticket représente $\approx 1{,}4$ point de macro-F1. Un modèle n'est déclaré significativement supérieur que si l'écart est d'au moins **5 tickets ($\approx 7$ points de macro-F1)**. En dessous, l'écart peut être attribué au bruit statistique.

---

## 3. Résultats Comparatifs du Benchmark

Les évaluations ont été réalisées sur le même jeu de test de 72 tickets, avec une température de 0.0 et un format JSON strict imposé.

| Modèle / Configuration | Accuracy | Macro-F1 | Invalides (%) | Durée (s) | Statut |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **gpt-oss-120b + 4 exemples** *(Few-shot)* | **0.972** | **0.970** | **0.0 %** | 216.2 s | **1er (Meilleur global)** |
| **qwen/qwen3.8-27b** *(Zero-shot)* | 0.958 | 0.956 | 0.0 % | 224.1 s | **2e (Meilleur Zero-shot)** |
| **openai/gpt-oss-120b** *(Zero-shot)* | 0.917 | 0.917 | 0.0 % | 493.5 s | 3e |
| **openai/gpt-oss-20b** *(Zero-shot)* | 0.903 | 0.902 | 1.4 % | 213.2 s | 4e |

---

## 4. Analyse et Interprétation des Résultats

1. **Impact du Prompt Engineering (Few-shot)** :
   - En ajoutant simplement **4 exemples** à la consigne (un par catégorie), `gpt-oss-120b` passe de **0.917** à **0.970** de macro-F1 (+5.3 points, soit $\approx 3.8$ tickets supplémentaires bien classés).
   - **Conclusion majeure de l'atelier** : Le gain apporté par 4 exemples bien choisis est supérieur à l'écart entre les modèles en zero-shot. Le prompt engineering s'avère être un levier plus puissant que la seule taille du modèle.

2. **Zero-shot : Architecture vs Taille** :
   - En zero-shot, `qwen/qwen3.8-27b` (27B) surpasse largement `openai/gpt-oss-120b` (120B) : **0.956 vs 0.917** (+3.9 points), tout en étant plus de 2 fois plus rapide (224 s vs 493 s).
   - `openai/gpt-oss-20b` obtient 0.902 et produit 1 réponse invalide (rejet JSON sur message très court), soulignant une fragilité du plus petit modèle face au formatage strict.

3. **Analyse des erreurs (Matrice de Confusion)** :
   - Pour la configuration gagnante (`gpt-oss-120b + 4 exemples`) :
     - `technique` : 20/20 bien routés ($F1 = 1.000$)
     - `compte` : 16/16 bien routés ($F1 = 1.000$)
     - `facturation` : 22/22 bien routés ($F1 = 0.957$)
     - `commercial` : 12/14 bien routés ($F1 = 0.923$, 2 tickets routés en facturation).
   - La classe `commercial` reste la seule présentant des confusions résiduelles, typiquement sur des tickets où le client mentionne un montant d'abonnement ou un litige tarifaire avant de demander une résiliation (ex: T040, T066).

---

## 5. Décision et Recommandation de Mise en Production

- **Option recommandée pour la production** :
  - **Recommandation n°1 (Qualité maximale)** : Déployer **`openai/gpt-oss-120b` avec la consigne à 4 exemples (Few-shot)**. Elle atteint le score record de **0.970 de Macro-F1** (70 tickets bien classés sur 72) avec 0 % d'invalides.
  - **Recommandation n°2 (Coût / Efficacité Zero-shot)** : Si l'on souhaite un modèle léger et rapide sans complexifier le prompt, **`qwen/qwen3.8-27b`** est le choix idéal (0.956 Macro-F1, excellente latence, aucun coût de contexte supplémentaire).
