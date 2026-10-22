from classifieur import classer

modele = "openai/gpt-oss-20b"
tests = [
    "Ma facture est trop elevee",
    "Je ne peux plus me connecter a mon compte",
    "L'application ne fonctionne plus",
    "Je souhaite changer mon abonnement",
    " bonjour ! "
]

for texte in tests:
    resultat = classer(texte, modele)
    print(f"Ticket : {texte}")
    print(f"Categorie : {resultat}\n")
