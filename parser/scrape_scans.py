import json
from parser.scans_parser import scrape_all_scans_from_links


def scrape_all_scans_from_manga_data(manga_data_path: str = 'manga_data.json', output_path: str = 'scans_data.json') -> dict:
    """
    Scrape all scans for all manga links in manga_data.json and return the collected scans data.

    This function performs the network scraping and should be run explicitly by the user.
    It returns a dictionary with titles as keys and scan data as values.
    """
    with open(manga_data_path, 'r', encoding='utf-8') as f:
        manga_by_title = json.load(f)

    scans_by_title = {}
    
    # Iterate through each title and its manga links
    for title, manga_links in manga_by_title.items():
        scans_data = scrape_all_scans_from_links(manga_links)
        if scans_data:
            scans_by_title[title] = scans_data

    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scans_by_title, f, ensure_ascii=False, indent=2)

    return scans_by_title
