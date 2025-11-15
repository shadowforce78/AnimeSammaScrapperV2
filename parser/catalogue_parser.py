import json
from parser.details_parser import parse_oeuvre_details


def parse_catalogue_from_soup(soup, fetch_details=False):
    """Parse catalogue items from a single soup object
    
    Args:
        soup: BeautifulSoup object of the catalogue page
        fetch_details: If True, fetch additional details from each oeuvre's page
    """
    title_section = soup.find(id="list_catalog")
    if not title_section:
        return []
    
    # The site uses a number of tailwind classes which can change; match by
    # the stable 'shrink-0' class and filter for cards with a link/image.
    all_cards = title_section.find_all("div", class_="shrink-0")
    items = [card for card in all_cards if card.find("a", href=True) and card.find("img", src=True)]
    parsed_items = []
    
    for item in items:
        link_tag = item.find("a", href=True)
        img_tag = item.find("img", src=True)
        # Some links on the site contain trailing spaces; normalize them
        href = link_tag['href'].strip() if link_tag and link_tag.get('href') else None
        img_src = img_tag['src'].strip() if img_tag and img_tag.get('src') else None

        # Title is often in an h1/h2; class attribute can vary so fall back
        title_tag = item.find(["h1", "h2", "h3"])  # site uses h2.card-title
        alt_title_tag = (
            item.find("p", class_="alternate-titles")
            or item.find("p", class_="text-white text-xs opacity-40 truncate italic")
            or item.find("p", class_="italic")
        )

        info_tags = item.find_all("p", class_="info-value") or item.find_all("p")
        genres_tag = info_tags[0] if len(info_tags) > 0 else None
        type_tag = info_tags[1] if len(info_tags) > 1 else None
        language_tag = info_tags[2] if len(info_tags) > 2 else None

        parsed_item = {
            "link": href,
            "image": img_src,
            "title": title_tag.text.strip() if title_tag else None,
            "alt_title": alt_title_tag.text.strip() if alt_title_tag else None,
            "genres": [genre.strip() for genre in genres_tag.text.split(',')] if genres_tag and genres_tag.text else [],
            "type": type_tag.text.strip() if type_tag and type_tag.text else None,
            "language": language_tag.text.strip() if language_tag and language_tag.text else None
        }
        
        # Fetch detailed information if requested
        if fetch_details and parsed_item["link"]:
            print(f"      🔗 Récupération des détails de: {parsed_item['title']}")
            details = parse_oeuvre_details(parsed_item["link"])
            if details:
                parsed_item["details"] = details
        
        parsed_items.append(parsed_item)
    
    return parsed_items


def parser_catalogue(soup):
    """Parse catalogue from a single soup (backward compatibility)"""
    parsed_items = parse_catalogue_from_soup(soup)
    return json.dumps(parsed_items, ensure_ascii=False, indent=2)


def parser_all_catalogue_pages(soups, fetch_details=False):
    """Parse catalogue items from multiple soup objects (all pages)
    
    Args:
        soups: List of BeautifulSoup objects
        fetch_details: If True, fetch additional details from each oeuvre's page
    """
    all_items = []
    
    for i, soup in enumerate(soups, 1):
        print(f"🔍 Parsing de la page {i}/{len(soups)}...")
        items = parse_catalogue_from_soup(soup, fetch_details=fetch_details)
        all_items.extend(items)
        print(f"   ✓ {len(items)} ouvrages trouvés sur cette page")
    
    print(f"\n🎉 Total : {len(all_items)} ouvrages récupérés")
    return all_items