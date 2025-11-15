def parse_genres(soup):
    """Return a list of available genres from the catalogue page soup.

    If the section is not found, return an empty list instead of raising.
    """
    genres = []
    genres_section = soup.find(id="filtres_genres")
    if not genres_section:
        return genres

    checkboxes = genres_section.find_all("input", {"type": "checkbox"})
    for checkbox in checkboxes:
        value = checkbox.get("value")
        if value:
            genres.append(value.strip())

    # Remove duplicates while preserving order
    seen = set()
    cleaned = []
    for g in genres:
        if g not in seen:
            seen.add(g)
            cleaned.append(g)

    return cleaned