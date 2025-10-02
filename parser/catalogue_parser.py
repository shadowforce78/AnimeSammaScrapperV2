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
    
    items = title_section.find_all("div", class_="shrink-0 m-3 rounded border-2 border-gray-400 border-opacity-50 shadow-2xl shadow-black hover:shadow-zinc-900 hover:opacity-80 bg-black bg-opacity-40 transition-all duration-200 cursor-pointer")
    parsed_items = []
    
    for item in items:
        link_tag = item.find("a", href=True)
        img_tag = item.find("img", src=True)
        title_tag = item.find("h1", class_="text-white font-bold uppercase text-md line-clamp-2")
        alt_title_tag = item.find("p", class_="text-white text-xs opacity-40 truncate italic")
        
        info_tags = item.find_all("p", class_="mt-0.5 text-gray-300 font-medium text-xs truncate")
        genres_tag = info_tags[0] if len(info_tags) > 0 else None
        type_tag = info_tags[1] if len(info_tags) > 1 else None
        language_tag = info_tags[2] if len(info_tags) > 2 else None

        parsed_item = {
            "link": link_tag['href'] if link_tag else None,
            "image": img_tag['src'] if img_tag else None,
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