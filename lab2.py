import requests

# URL cible
url = "https://github.com/search?q=mental+health+ai&type=repositories"

# On définit des headers pour se faire passer pour un vrai navigateur
# Sans ça, GitHub peut bloquer notre requête (code 403)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Connection": "keep-alive",
}

# Envoi de la requête
response = requests.get(url, headers=headers)

# Vérification du statut (bonne pratique !)
# 200 = OK, 403 = Interdit, 404 = Pas trouvé, 429 = Trop de requêtes
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    # Sauvegarde du HTML brut dans un fichier texte
    with open("github_raw.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Fichier sauvegardé avec succès")
else:
    print(f"Erreur : {response.status_code}")