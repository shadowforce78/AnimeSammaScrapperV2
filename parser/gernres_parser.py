def parse_genres(soup):
    genres_section = soup.find(id="filtres_genres")
    if genres_section:
        checkboxes = genres_section.find_all("input", {"type": "checkbox"})
        genres = [checkbox['value'] for checkbox in checkboxes]
        # Genres = All genres available on the site
    return genres