from utils.catalogue import return_data, fetch_all_catalogue_pages
from db.add_utils_to_db import add_utils_to_db
from db.add_data_to_db import add_data_to_db
from db.add_episodes_to_db import add_episodes_to_db
from db.add_scans_to_db import add_scans_to_db
from parser.catalogue_parser import parser_all_catalogue_pages
from parser.scrape_episodes import scrape_all_episodes_from_catalogue
from parser.scrape_scans import scrape_all_scans_from_manga_data
import json

# Scrap utils first (genres, languages, types from first page only)
# add_utils_to_db(return_data()) # Scraped ✅

# Scrap catalogue title next
# all_soups = fetch_all_catalogue_pages()
# all_catalogue_items = parser_all_catalogue_pages(all_soups, fetch_details=True)

# with open("data.json", "r", encoding="utf-8") as f:
#     all_catalogue_items = json.load(f)
# add_data_to_db(all_catalogue_items) # Scraped ✅

# Scrap episodes next
# scrape_all_episodes_from_catalogue()  # This will create episodes_data.json
# with open("episodes_data.json", "r", encoding="utf-8") as f:
#     all_episodes_data = json.load(f)
# episodes_data = add_episodes_to_db(all_episodes_data) # Scraped ✅

# Scrap scan next
# with open("data.json", "r", encoding="utf-8") as f:
#     all_catalogue_items = json.load(f)

# manga_by_title = {}
# # Get manga disponible for each item with manga
# for item in all_catalogue_items:
#     if item.get("details", {}).get("manga_disponible"):
#         manga_disponible = item["details"]["manga_disponible"]
#         title = item['title']
#         manga_by_title[title] = []

#         for manga in manga_disponible:
#             full_url = f"https://anime-sama.fr/catalogue/{title.lower().replace(' ', '-').replace('#', '')}/{manga['url']}"
#             manga_by_title[title].append(full_url)

# with open("manga_data.json", "w", encoding="utf-8") as f:
#     # Put links grouped by title in manga_data.json
#     json.dump(manga_by_title, f, ensure_ascii=False, indent=2)

# Scrap all manga scans from manga_data.json
# scrape_all_scans_from_manga_data()  # This will create scans_data.json
# with open("scans_data.json", "r", encoding="utf-8") as f:
#     all_scans_data = json.load(f)
# add_scans_to_db(all_scans_data)  # Scraped ✅
