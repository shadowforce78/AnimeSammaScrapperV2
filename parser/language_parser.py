def parse_languages(soup):
    """Return a list of languages from the catalogue page soup.

    If the section is absent, return an empty list.
    """
    languages = []
    language_section = soup.find(id="filtres_langues")
    if not language_section:
        return languages

    checkboxes = language_section.find_all("input", {"type": "checkbox"})
    for checkbox in checkboxes:
        value = checkbox.get("value")
        if value:
            languages.append(value.strip())

    # Remove duplicates while preserving order
    seen = set()
    cleaned = []
    for l in languages:
        if l not in seen:
            seen.add(l)
            cleaned.append(l)

    return cleaned
