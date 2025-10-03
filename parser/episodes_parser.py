import requests
import bs4
import re
from urllib.parse import quote
from typing import Dict, List, Optional


def parse_episodes_from_url(base_title: str, anime_url: str) -> Optional[Dict[str, List[str]]]:
    """
    Parse episode links from an anime URL
    
    Args:
        base_title: The title of the anime (will be kebab-cased)
        anime_url: The relative URL (e.g., "saison1/vostfr")
        
    Returns:
        Dictionary with episode sources (eps1, eps2, etc.) containing lists of episode URLs
        Returns None if parsing fails
    """
    try:
        # Préparer le titre pour l'URL
        kebabed_title = base_title.lower().replace(" ", "-")
        encoded_title = quote(kebabed_title)
        
        # Construire l'URL complète de la page
        page_url = f"https://anime-sama.fr/catalogue/{encoded_title}/{anime_url}"
        
        # Récupérer la page
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        
        # Trouver l'ID du fichier episodes.js
        episode_id = None
        for script in soup.find_all("script", src=True):
            if "episodes.js?filever=" in script["src"]:
                episode_id = script["src"].split("episodes.js?filever=")[1]
                break
        
        if not episode_id:
            return None
        
        # Construire l'URL du fichier episodes.js
        episodes_js_url = f"https://anime-sama.fr/catalogue/{encoded_title}/{anime_url}/episodes.js?filever={episode_id}"
        
        # Récupérer le contenu JavaScript
        js_response = requests.get(episodes_js_url, timeout=10)
        js_response.raise_for_status()
        js_content = js_response.text
        
        # Parser le contenu JavaScript
        all_links = {}
        js_content = js_content.replace("var ", "").strip()
        
        # Découpe par blocs "epsX = [ ... ];"
        blocks = re.split(r'(\w+\s*=\s*\[)', js_content)
        
        current_key = None
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            
            # Si c'est un header genre "eps3 = ["
            if "=" in block and block.endswith("["):
                current_key = block.split("=")[0].strip()
                all_links[current_key] = []
                continue
            
            # Sinon c'est le contenu du tableau
            if current_key:
                lines = [l.strip("', ") for l in block.split("\n") if l.strip()]
                for line in lines:
                    # Ignorer les crochets et fins de tableau
                    if line in ["]", "];"]:
                        continue
                    # Garder que les URLs valides
                    if line.startswith("http"):
                        # Remplacer vidmoly.to par vidmoly.net
                        line = line.replace("https://vidmoly.to", "https://vidmoly.net")
                        all_links[current_key].append(line)
        
        # Compter le nombre total d'épisodes (basé sur le premier source)
        nb_episodes = len(all_links[list(all_links.keys())[0]]) if all_links else 0
        
        return all_links
        
    except Exception as e:
        return None


def parse_all_anime_episodes(oeuvre_data: dict) -> Dict[str, Dict[str, List[str]]]:
    """
    Parse all anime episodes for a given oeuvre
    
    Args:
        oeuvre_data: Dictionary containing the oeuvre information from data.json
        
    Returns:
        Dictionary with anime names as keys and episode links as values
    """
    title = oeuvre_data.get("title")
    details = oeuvre_data.get("details", {})
    anime_disponible = details.get("anime_disponible", [])
    
    if not title or not anime_disponible:
        return {}
    
    all_anime_episodes = {}
    
    for anime in anime_disponible:
        anime_name = anime.get("nom")
        anime_url = anime.get("url")
        
        if not anime_name or not anime_url:
            continue
        
        episodes = parse_episodes_from_url(title, anime_url)
        
        if episodes:
            all_anime_episodes[anime_name] = episodes
    
    return all_anime_episodes
