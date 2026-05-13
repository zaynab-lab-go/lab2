import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}

def extraire_repos(url):
    repos = []

    # Pause aléatoire entre 3 et 6 secondes avant chaque requête
    # Simule un comportement humain pour éviter le blocage
    pause = random.uniform(3, 6)
    print(f"Pause de {pause:.1f} secondes...")
    time.sleep(pause)

    response = requests.get(url, headers=headers)
    print(f"Status code : {response.status_code}")

    # Si on est bloqué, on attend plus longtemps et on réessaie
    if response.status_code == 429:
        print("Bloqué ! On attend 60 secondes...")
        time.sleep(60)
        response = requests.get(url, headers=headers)
        print(f"Status code après attente : {response.status_code}")

    if response.status_code != 200:
        print(f"Erreur : {response.status_code}")
        return repos

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("div.Repositories-module__headerRow__rNWYn")
    print(f"Nombre de repos trouvés : {len(items)}")

    for item in items:
        repo = {}

        try:
            title_tag = item.find("a")
            repo["title"] = title_tag.text.strip()
            repo["url"] = "https://github.com" + title_tag["href"]
        except:
            repo["title"] = "N/A"
            repo["url"] = "N/A"

        try:
            parent = item.find_parent()
            desc_tag = parent.select_one("div.Content-module__Content__mHmep")
            repo["description"] = desc_tag.text.strip() if desc_tag else "N/A"
        except:
            repo["description"] = "N/A"

        try:
            parent = item.find_parent()
            star_tag = parent.select_one("div.Repositories-module__starButtonWrapper__Aa")
            repo["stars"] = star_tag.text.strip() if star_tag else "0"
        except:
            repo["stars"] = "0"

        try:
            parent = item.find_parent()
            footer_tag = parent.select_one("ul.Footer-module__footer__kjBR4")
            repo["last_updated"] = footer_tag.text.strip() if footer_tag else "N/A"
        except:
            repo["last_updated"] = "N/A"

        repos.append(repo)

    return repos


# ============================================================
# EXTRACTION SUR PLUSIEURS PAGES
# ============================================================
all_data = []

for page in [1, 2, 3, 4, 5]:
    print(f"\n📄 Scraping page {page}...")
    url = f"https://github.com/search?q=mental+health+ai&type=repositories&p={page}"
    repos = extraire_repos(url)
    all_data.extend(repos)

df_all = pd.DataFrame(all_data)
df_all.drop_duplicates(subset=["url"], inplace=True)
df_all.reset_index(drop=True, inplace=True)

print(f"\n--- Aperçu ---")
print(df_all.head(10))

df_all.to_csv("github_repos_multipages.csv", index=False, encoding="utf-8")
print(f"\n✅ Total : {len(df_all)} repos sauvegardés !")
