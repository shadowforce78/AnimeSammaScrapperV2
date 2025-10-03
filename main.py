from utils.catalogue import return_data, fetch_all_catalogue_pages
from db.add_utils_to_db import add_utils_to_db
from db.add_data_to_db import add_data_to_db
from parser.catalogue_parser import parser_all_catalogue_pages
import json
import requests
import bs4
import re
from urllib.parse import quote
# Scrap utils first (genres, languages, types from first page only)
# add_utils_to_db(return_data()) # Scraped ✅

# Scrap catalogue title next
# all_soups = fetch_all_catalogue_pages()
# all_catalogue_items = parser_all_catalogue_pages(all_soups, fetch_details=True)

# with open("data.json", "r", encoding="utf-8") as f:
#     all_catalogue_items = json.load(f)
# add_data_to_db(all_catalogue_items) # Scrapead ✅

title = "Demon Slayer"
url = "saison1/vostfr"
kebabed_title = title.lower().replace(" ", "-")
encoded_title = quote(kebabed_title)
totallink = f"https://anime-sama.fr/catalogue/{encoded_title}/{url}"
response = requests.get(totallink)
soup = bs4.BeautifulSoup(response.text, "html.parser")
# <!-- liste יpisodes -->
# <script defer="" src="episodes.js?filever=6077" type="text/javascript">
# I need the ID from here "6077" from the soup
id = None
for script in soup.find_all("script", src=True):
    if "episodes.js?filever=" in script["src"]:
        id = script["src"].split("episodes.js?filever=")[1]
        break

# This ID corresponds to the episodes.js file that contains the episode links of the first season
# Each var epsX corresponds to a different link source (Sibnet, Oneupload, etc.)
# Each links in the array corresponds to an episode in order (Episode 1, Episode 2, etc.)

linkurl = f"https://anime-sama.fr/catalogue/{encoded_title}/{url}/episodes.js?filever={id}"
response = requests.get(linkurl)
js_content = response.text

all_links = {}
js_content = js_content.replace("var ", "").strip()

# Découpe par blocs "epsX = [ ... ];"
blocks = re.split(r'(\w+\s*=\s*\[)', js_content)

current_key = None
for block in blocks:
    block = block.strip()
    if not block:
        continue

    # Si c'est un header genre "eps3 = ["
    if "=" in block and block.endswith("["):
        current_key = block.split("=")[0].strip()
        all_links[current_key] = []
        continue

    # Sinon c’est le contenu du tableau
    if current_key:
        lines = [l.strip("', ") for l in block.split("\n") if l.strip()]
        for line in lines:
            # ignorer les crochets et fins de tableau
            if line in ["]", "];"]:
                continue
            # garder que les URLs valides
            if line.startswith("http"):
                all_links[current_key].append(line)

# Export JSON propre
print(json.dumps(all_links, indent=2, ensure_ascii=False))