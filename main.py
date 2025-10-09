from utils.catalogue import return_data, fetch_all_catalogue_pages
from db.add_utils_to_db import add_utils_to_db
from db.add_data_to_db import add_data_to_db
from db.add_episodes_to_db import add_episodes_to_db
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
# add_data_to_db(all_catalogue_items) # Scraped ✅

# Scrap every episodes 
with open("episodes_data.json", "r", encoding="utf-8") as f:
    all_episodes_data = json.load(f)
episodes_data = add_episodes_to_db(all_episodes_data) # Scraped ✅

