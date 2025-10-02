from utils.catalogue import return_data, fetch_all_catalogue_pages
from db.add_utils_to_db import add_utils_to_db
from db.add_data_to_db import add_data_to_db
from parser.catalogue_parser import parser_all_catalogue_pages
import json
import requests
import bs4

# Scrap utils first (genres, languages, types from first page only)
# add_utils_to_db(return_data()) # Scraped ✅

# Scrap catalogue title next
# all_soups = fetch_all_catalogue_pages()
# all_catalogue_items = parser_all_catalogue_pages(all_soups, fetch_details=True)

# with open("data.json", "r", encoding="utf-8") as f:
#     all_catalogue_items = json.load(f)
# add_data_to_db(all_catalogue_items) # Scrapead ✅

# Scrap video link next
# {
#     "link": "https://anime-sama.fr/catalogue/demon-slayer/",
#     "image": "https://cdn.statically.io/gh/Anime-Sama/IMG/img/contenu/demon-slayer.jpg",
#     "title": "Demon Slayer",
#     "alt_title": "Kimetsu no Yaiba, KNY",
#     "genres": [
#       "Action",
#       "Aventure",
#       "Drame",
#       "Fantastique",
#       "Historique",
#       "Surnaturel"
#     ],
#     "type": "Anime, Scans",
#     "language": "VOSTFR, VF",
#     "details": {
#       "titre_principal": "Demon Slayer",
#       "titre_alternatif": "Kimetsu no Yaiba, KNY",
#       "avancement": "Le film \"La Forteresse Infinie\" est prévu pour 2026",
#       "correspondance": "Saison 4 Épisode 8 -> Chapitre 139",
#       "synopsis": "Depuis les temps anciens, il existe des rumeurs concernant des démons mangeurs d'hommes qui se cachent dans les bois. Pour cette raison, les citadins locaux ne s'y aventurent jamais la nuit. La légende raconte aussi qu'un tueur de démons déambule la nuit, chassant ces démons assoiffés de sang. Pour le jeune Tanjirô, ces rumeurs vont bientôt devenir sa dure réalité ...\r\n\r\nDepuis la mort de son père, Tanjirô a pris sur lui pour subvenir aux besoins de sa famille. Malgré cette tragédie, ils réussissent à trouver un peu de bonheur au quotidien.\r\n\r\nCependant, ce peu de bonheur se retrouve détruit le jour où Tanjirô découvre que sa famille s'est fait massacrer et que la seule survivante, sa sœur Nezuko, est devenue un démon. À sa grande surprise, Nezuko montre encore des signes d'émotion et de pensées humaines. Ainsi, commence la dure tâche de Tanjirô, celle de combattre les démons et de faire redevenir sa sœur humaine.",
#       "genres_details": [
#         "Action",
#         "Aventure",
#         "Drame",
#         "Fantastique",
#         "Historique",
#         "Surnaturel"
#       ],
#       "anime_disponible": [
#         {
#           "nom": "Saison 1",
#           "url": "saison1/vostfr"
#         },
#         {
#           "nom": "Film",
#           "url": "film/vostfr"
#         },
#         {
#           "nom": "Épisode - Train de l'infini",
#           "url": "saison1hs/vostfr"
#         },
#         {
#           "nom": "Saison 2",
#           "url": "saison2/vostfr"
#         },
#         {
#           "nom": "Saison 3",
#           "url": "saison3/vostfr"
#         },
#         {
#           "nom": "Saison 4",
#           "url": "saison4/vostfr"
#         }
#       ],
#       "manga_disponible": [
#         {
#           "nom": "Scans",
#           "url": "scan/vf"
#         },
#         {
#           "nom": "Spin-off Rengoku",
#           "url": "scan-rengoku/vf"
#         },
#         {
#           "nom": "Spin-off Tomioka",
#           "url": "scan-tomioka/vf"
#         }
#       ]
#     }
#   }

totallink = "https://anime-sama.fr/catalogue/demon-slayer/saison1/vostfr"
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

linkurl = "https://anime-sama.fr/catalogue/demon-slayer/saison1/vostfr/episodes.js?filever=" + id
response = requests.get(linkurl)
js_content = response.text
print(js_content)