import requests
import bs4
from typing import Dict, Any, Optional


def parse_oeuvre_details(url: str) -> Optional[Dict[str, Any]]:
    """
    Parse detailed information from an oeuvre's individual page
    
    Args:
        url: The URL of the oeuvre page
        
    Returns:
        Dictionary with detailed information or None if failed
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        
        details = {}
        
        # Titre principal et alternatif (déjà dans le catalogue mais on les récupère aussi pour vérification)
        titre_oeuvre = soup.find("h4", id="titreOeuvre")
        titre_alter = soup.find("h2", id="titreAlter")
        
        details["titre_principal"] = titre_oeuvre.text.strip() if titre_oeuvre else None
        details["titre_alternatif"] = titre_alter.text.strip() if titre_alter else None
        
        # Avancement et Correspondance
        avancement_p = None
        correspondance_p = None
        
        for p in soup.find_all("p", class_="text-white font-semibold text-sm"):
            text = p.text.strip()
            if text.startswith("Avancement"):
                a_tag = p.find("a", class_="font-normal text-gray-400")
                avancement_p = a_tag.text.strip() if a_tag else None
            elif text.startswith("Correspondance"):
                a_tag = p.find("a", class_="font-normal text-gray-400")
                correspondance_p = a_tag.text.strip() if a_tag else None
        
        details["avancement"] = avancement_p
        details["correspondance"] = correspondance_p
        
        # Synopsis
        synopsis_h2 = soup.find("h2", string=lambda text: text and "Synopsis" in text)
        if synopsis_h2:
            synopsis_p = synopsis_h2.find_next_sibling("p")
            details["synopsis"] = synopsis_p.text.strip() if synopsis_p else None
        else:
            details["synopsis"] = None
        
        # Genres (depuis la page détails)
        genres_h2 = soup.find("h2", string=lambda text: text and "Genres" in text)
        if genres_h2:
            genres_a = genres_h2.find_next_sibling("a")
            if genres_a:
                details["genres_details"] = [g.strip() for g in genres_a.text.split(',')]
            else:
                details["genres_details"] = []
        else:
            details["genres_details"] = []
        
        # Anime sections (extraction des saisons/versions disponibles)
        anime_sections = []
        anime_h2 = soup.find("h2", string=lambda text: text and "Anime" in text)
        if anime_h2:
            anime_div = anime_h2.find_next_sibling("div")
            if anime_div:
                script_tag = anime_div.find("script")
                if script_tag:
                    script_content = script_tag.string
                    if script_content:
                        # Parse panneauAnime calls
                        import re
                        pattern = r'panneauAnime\("([^"]+)",\s*"([^"]+)"\)'
                        matches = re.findall(pattern, script_content)
                        for match in matches:
                            # Skip template/comment entries
                            if match[0] != "nom" and match[1] != "url":
                                anime_sections.append({
                                    "nom": match[0],
                                    "url": match[1]
                                })
        
        details["anime_disponible"] = anime_sections
        
        # Manga sections (extraction des scans disponibles)
        manga_sections = []
        manga_h2 = soup.find("h2", string=lambda text: text and "Manga" in text)
        if manga_h2:
            manga_div = manga_h2.find_next_sibling("div")
            if manga_div:
                script_tag = manga_div.find("script")
                if script_tag:
                    script_content = script_tag.string
                    if script_content:
                        # Parse panneauScan calls
                        import re
                        pattern = r'panneauScan\("([^"]+)",\s*"([^"]+)"\)'
                        matches = re.findall(pattern, script_content)
                        for match in matches:
                            # Skip template/comment entries
                            if match[0] != "nom" and match[1] != "url":
                                manga_sections.append({
                                    "nom": match[0],
                                    "url": match[1]
                                })
        
        details["manga_disponible"] = manga_sections
        
        return details
        
    except Exception as e:
        print(f"   ❌ Erreur lors du parsing de {url}: {e}")
        return None
