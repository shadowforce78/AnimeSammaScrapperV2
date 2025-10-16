import requests
import bs4
from urllib.parse import quote
from typing import Dict, List, Optional


def parse_scan_chapters(url: str) -> Optional[Dict]:
    """
    Parse all chapters and images for a given manga scan URL
    
    Args:
        url: Full URL to the manga scan page (e.g., "https://anime-sama.fr/catalogue/solo-leveling/scan/vf/")
        
    Returns:
        Dictionary with 'title' and 'chapters' (list of chapter dicts with 'chapter' and 'images')
        Returns None if parsing fails
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        
        # Get the oeuvre title
        titre_oeuvre_tag = soup.find(id="titreOeuvre")
        if not titre_oeuvre_tag:
            return None
        
        nom_oeuvre = titre_oeuvre_tag.text.strip()
        
        # Get metadata (chapters and number of images per chapter)
        url_metadata = f"https://anime-sama.fr/s2/scans/get_nb_chap_et_img.php?oeuvre={quote(nom_oeuvre)}"
        response = requests.get(url_metadata, timeout=10)
        
        if not response.ok:
            return None
        
        data = response.json()
        all_chapters = [
            {"chapter": int(chap), "num_images": int(num)} 
            for chap, num in data.items()
        ]
        
        # Build image URLs for each chapter
        all_images = []
        for chapter_info in all_chapters:
            chapter_num = chapter_info["chapter"]
            num_images = chapter_info["num_images"]
            images = [
                f"https://anime-sama.fr/s2/scans/{quote(nom_oeuvre)}/{chapter_num}/{i}.jpg" 
                for i in range(1, num_images + 1)
            ]
            all_images.append({
                "chapter": chapter_num, 
                "images": images
            })
        
        return {
            "url": url,
            "title": nom_oeuvre,
            "chapters": all_images
        }
        
    except Exception as e:
        return None


def scrape_all_scans_from_links(manga_links: List[str]) -> List[Dict]:
    """
    Scrape all manga scans from a list of URLs
    
    Args:
        manga_links: List of manga scan URLs
        
    Returns:
        List of dictionaries with scan data (title, url, chapters)
    """
    all_scans_data = []
    
    for url in manga_links:
        scan_data = parse_scan_chapters(url)
        if scan_data:
            all_scans_data.append(scan_data)
    
    return all_scans_data
