import json
from db.add_episodes_to_db import add_episodes_to_db

# Charger les données du catalogue
with open("data.json", "r", encoding="utf-8") as f:
    all_catalogue_items = json.load(f)

# Scraper tous les épisodes
episodes_data = add_episodes_to_db(all_catalogue_items)
