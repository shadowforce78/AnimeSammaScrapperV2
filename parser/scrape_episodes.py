import json
from parser.episodes_parser import parse_all_anime_episodes


def scrape_all_episodes_from_catalogue(catalogue_path: str = 'data.json', output_path: str = 'episodes_data.json') -> list:
    """
    Scrape all episodes for all oeuvres in data.json and return the collected episodes data.

    This function performs the network scraping and should be run explicitly by the user.
    It returns a list of entries; each entry contains: title, link, type, episodes
    """
    with open(catalogue_path, 'r', encoding='utf-8') as f:
        all_catalogue_items = json.load(f)

    all_episodes_data = []

    oeuvres_with_anime = [
        item for item in all_catalogue_items
        if item.get('details', {}).get('anime_disponible')
    ]

    for oeuvre in oeuvres_with_anime:
        episodes_data = parse_all_anime_episodes(oeuvre)
        if episodes_data:
            oeuvre_episode_entry = {
                'title': oeuvre.get('title'),
                'link': oeuvre.get('link'),
                'type': oeuvre.get('type'),
                'episodes': episodes_data
            }
            all_episodes_data.append(oeuvre_episode_entry)

    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_episodes_data, f, ensure_ascii=False, indent=2)

    return all_episodes_data
