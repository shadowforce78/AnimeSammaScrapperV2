import json
from parser.episodes_parser import parse_all_anime_episodes


def add_episodes_to_db(all_catalogue_items: list, save_to_file: str = "episodes_data.json"):
    """
    Parse and save all anime episodes from the catalogue
    
    Args:
        all_catalogue_items: List of oeuvre dictionaries from data.json
        save_to_file: Filename to save the episodes data
    """
    all_episodes_data = []
    
    # Filtrer seulement les oeuvres qui ont des animes disponibles
    oeuvres_with_anime = [
        item for item in all_catalogue_items 
        if item.get("details", {}).get("anime_disponible")
    ]
    
    for i, oeuvre in enumerate(oeuvres_with_anime, 1):
        
        episodes_data = parse_all_anime_episodes(oeuvre)
        
        if episodes_data:
            oeuvre_episode_entry = {
                "title": oeuvre.get("title"),
                "link": oeuvre.get("link"),
                "type": oeuvre.get("type"),
                "episodes": episodes_data
            }
            all_episodes_data.append(oeuvre_episode_entry)
    
    # Sauvegarder dans un fichier JSON
    with open(save_to_file, 'w', encoding='utf-8') as f:
        json.dump(all_episodes_data, f, ensure_ascii=False, indent=2)
    
    # Statistiques
    total_episodes = 0
    total_sources = 0
    
    for entry in all_episodes_data:
        for anime_name, sources in entry["episodes"].items():
            total_sources += len(sources)
            # Compter les épisodes du premier source
            if sources:
                first_source = list(sources.keys())[0]
                total_episodes += len(sources[first_source])
    
    return all_episodes_data
