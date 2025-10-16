import json
from parser.scans_parser import scrape_all_scans_from_links


def scrape_all_scans_from_manga_data(manga_data_path: str = 'manga_data.json', output_path: str = 'scans_data.json') -> list:
    """
    Scrape all scans for all manga links in manga_data.json and return the collected scans data.

    This function performs the network scraping and should be run explicitly by the user.
    It returns a list of entries; each entry contains: title, url, chapters
    """
    with open(manga_data_path, 'r', encoding='utf-8') as f:
        manga_data = json.load(f)

    manga_links = manga_data.get('manga_links', [])

    all_scans_data = scrape_all_scans_from_links(manga_links)

    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_scans_data, f, ensure_ascii=False, indent=2)

    return all_scans_data
