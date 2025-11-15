import os
from typing import Optional

import bs4
import dotenv

from parser.gernres_parser import parse_genres
from parser.language_parser import parse_languages
from parser.type_parser import parse_types
from utils.scraper import fetch

dotenv.load_dotenv()

URL_BASE = os.getenv("URL_BASE")
CATALOGUE = os.getenv("CATALOGUE")
CATALOGUE_PAGE = os.getenv("CATALOGUE_PAGE")

first_page_soup, genres, languages, types, max_pages, soup = None, None, None, None, None, None

def fetch_catalogue_page(page=1):
    """Fetch a specific catalogue page using the hardened scraper session."""
    if not URL_BASE or not CATALOGUE or not CATALOGUE_PAGE:
        raise RuntimeError("Les variables d'environnement du catalogue sont manquantes")
    url = f"{URL_BASE}{CATALOGUE}{CATALOGUE_PAGE}{page}"
    return fetch(url)


def get_max_page_number(soup):
    """Determine the maximum number of pages from pagination"""
    # Look for pagination elements - typically buttons or links with page numbers
    pagination = soup.find("div", class_="pagination") or soup.find("ul", class_="pagination")
    
    if pagination:
        page_links = pagination.find_all("a")
        max_page = 1
        for link in page_links:
            text = link.text.strip()
            if text.isdigit():
                max_page = max(max_page, int(text))
        return max_page
    
    # If no pagination found, check if there are items on page 2
    # This is a fallback method
    try:
        response = fetch_catalogue_page(2)
        soup_page_2 = bs4.BeautifulSoup(response.text, "html.parser")
        items = soup_page_2.find(id="list_catalog")
        if items and items.find_all("div", class_="shrink-0"):
            # If page 2 exists, we need to find the last page by trial
            page = 2
            while True:
                try:
                    response = fetch_catalogue_page(page + 1)
                    soup_test = bs4.BeautifulSoup(response.text, "html.parser")
                    items = soup_test.find(id="list_catalog")
                    if not items or not items.find_all("div", class_="shrink-0"):
                        return page
                    page += 1
                except:
                    return page
    except:
        pass
    
    return 1


def bootstrap_catalogue(force_refresh: bool = False):
    global first_page_soup, genres, languages, types, max_pages, soup

    if first_page_soup is not None and not force_refresh:
        return

    response = fetch_catalogue_page(1)
    first_page_soup = bs4.BeautifulSoup(response.text, "html.parser")
    first_page_soup = first_page_soup
    soup = first_page_soup
    genres = parse_genres(first_page_soup)
    languages = parse_languages(first_page_soup)
    types = parse_types(first_page_soup)
    max_pages = get_max_page_number(first_page_soup)


def return_data():
    bootstrap_catalogue()
    return {"genres": genres, "languages": languages, "types": types}


def fetch_all_catalogue_pages():
    """Fetch all catalogue pages and return all soups"""
    bootstrap_catalogue()

    all_soups = [first_page_soup] if first_page_soup else []
    total_pages = max_pages or 1

    for page in range(2, total_pages + 1):
        try:
            response = fetch_catalogue_page(page)
            page_soup = bs4.BeautifulSoup(response.text, "html.parser")
            all_soups.append(page_soup)
        except Exception as e:
            print(f"Erreur lors de la récupération de la page {page}: {e}")
            break
    return all_soups
