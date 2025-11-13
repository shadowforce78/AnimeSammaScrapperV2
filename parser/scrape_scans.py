import json
from parser.scans_parser import scrape_all_scans_from_links, parse_scan_chapters
import re
import os
import dotenv

dotenv.load_dotenv()
BASE_URL=os.getenv("BASE_URL")


def extract_scan_type_from_url(url: str) -> str:
    """
    Extract scan type from URL.
    E.g., "https://anime-sama.fr/catalogue/solo-leveling/scan_ragnarok/vf" -> "scan_ragnarok"
    """
    match = re.search(r'/([^/]+)/vf/?$', url)
    if match:
        return match.group(1)
    return "scan"


def scrape_all_scans_from_manga_data(manga_data_path: str = 'manga_data.json', output_path: str = 'scans_data.json') -> list:
    """
    Scrape all scans for all manga links in manga_data.json and return the collected scans data.
    
    Structure similar to episodes_data.json:
    [
      {
        "title": "Solo Leveling",
        "link": "https://anime-sama.fr/catalogue/solo-leveling/",
        "type": "Scans",
        "scans": {
          "scan": { "chapters": [...] },
          "scan_side_story": { "chapters": [...] },
          ...
        }
      }
    ]
    """
    with open(manga_data_path, 'r', encoding='utf-8') as f:
        manga_by_title = json.load(f)

    all_scans_data = []
    
    # Iterate through each anime title and its manga links
    for anime_title, manga_links in manga_by_title.items():
        if not manga_links:
            continue
            
        scans_dict = {}
        
        # Scrape each manga link (scan, scan_side_story, etc.)
        for url in manga_links:
            scan_data = parse_scan_chapters(url)
            if scan_data:
                # Extract scan type from URL (e.g., "scan", "scan_ragnarok")
                scan_type = extract_scan_type_from_url(url)
                
                # Store chapters data under the scan type
                scans_dict[scan_type] = {
                    "url": url,
                    "title": scan_data.get("title"),
                    "chapters": scan_data.get("chapters", [])
                }
        
        # Only add entry if we have scans
        if scans_dict:
            # Build the catalogue link
            catalogue_link = f"{BASE_URL}/catalogue/{anime_title.lower().replace(' ', '-').replace('#', '')}/"
            
            all_scans_data.append({
                "title": anime_title,
                "link": catalogue_link,
                "type": "Scans",
                "scans": scans_dict
            })

    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_scans_data, f, ensure_ascii=False, indent=2)

    return all_scans_data
