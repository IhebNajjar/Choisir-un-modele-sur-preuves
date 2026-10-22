from evaluer import evaluer, charger
from classifieur import CONSIGNE_EXEMPLES

evaluer(
    "openai/gpt-oss-120b",
    charger(),
    consigne=CONSIGNE_EXEMPLES,
    etiquette="gpt-oss-120b + 4 exemples",
    nom_fichier="openai_gpt-oss-120b_variante.json"
)
