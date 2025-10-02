import requests
import dotenv
import os
import bs4
from parser.gernres_parser import parse_genres
from parser.language_parser import parse_languages
from parser.type_parser import parse_types

dotenv.load_dotenv()

URL_BASE = os.getenv("URL_BASE")
CATALOGUE = os.getenv("CATALOGUE")
CATALOGUE_PAGE = os.getenv("CATALOGUE_PAGE")


def fetch_catalogue_page(page=1):
    """Fetch a specific catalogue page"""
    url = f"{URL_BASE}{CATALOGUE}{CATALOGUE_PAGE}{page}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response


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


# Fetch first page to get utils and determine page count
first_page_response = fetch_catalogue_page(1)
first_page_soup = bs4.BeautifulSoup(first_page_response.text, "html.parser")

# Parse utils from first page only
genres = parse_genres(first_page_soup)
languages = parse_languages(first_page_soup)
types = parse_types(first_page_soup)

# Determine total number of pages
max_pages = get_max_page_number(first_page_soup)

# Store first page soup for compatibility
soup = first_page_soup


def return_data():
    return {"genres": genres, "languages": languages, "types": types}


def fetch_all_catalogue_pages():
    """Fetch all catalogue pages and return all soups"""
    all_soups = [first_page_soup]  # Include first page

    for page in range(2, max_pages + 1):
        try:
            response = fetch_catalogue_page(page)
            page_soup = bs4.BeautifulSoup(response.text, "html.parser")
            all_soups.append(page_soup)
        except Exception as e:
            print(f"Erreur lors de la récupération de la page {page}: {e}")
            break
    return all_soups
