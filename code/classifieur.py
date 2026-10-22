import json
import os
import time
from groq import Groq, RateLimitError

CATEGORIES = ["facturation", "technique", "compte", "commercial"]

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    # Récupération automatique si lancée hors session rechargée
    import subprocess
    try:
        api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY", "")
    except Exception:
        pass
client = Groq(api_key=api_key)

CONSIGNE = """Tu es un agent de tri du service client.
Classe le ticket dans exactement une categorie :
- facturation : montant, facture, paiement, remboursement.
- technique : un service ne fonctionne pas comme prevu.
- compte : acces au compte ou donnees personnelles.
- commercial : choix d'offre, abonnement, resiliation.
Si plusieurs categories semblent possibles, retiens l'intention
principale du client : ce qu'il veut obtenir.
Reponds uniquement par un objet JSON de la forme
{"categorie": "<une des quatre>"}."""

def classer(texte, modele, consigne=CONSIGNE, temperature=0.0):
    try:
        reponse = client.chat.completions.create(
            model=modele,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": consigne},
                {"role": "user", "content": texte}
            ],
        )
    except RateLimitError:
        print("Rate limit, pause 70s...")
        time.sleep(70)
        return classer(texte, modele, consigne, temperature)
    except Exception as e:
        print(f"Erreur API ({type(e).__name__}): {e}")
        return "invalide"

    try:
        contenu = reponse.choices[0].message.content
        donnees = json.loads(contenu)
        categorie = donnees.get("categorie", "")
    except (json.JSONDecodeError, AttributeError):
        return "invalide"

    categorie = str(categorie).strip().lower()
    return categorie if categorie in CATEGORIES else "invalide"

CONSIGNE_EXEMPLES = CONSIGNE + """

Exemples :
"Le geste commercial promis n'est pas sur mon releve."  -> {"categorie": "facturation"}
"Je paie chaque mois et rien ne marche depuis jeudi."   -> {"categorie": "technique"}
"Mon associe doit consulter les memes documents."       -> {"categorie": "compte"}
"Je demenage a l'etranger en septembre."                -> {"categorie": "commercial"}"""
