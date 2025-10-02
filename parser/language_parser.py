def parse_languages(soup):
    language_section = soup.find(id="filtres_langues")
    if language_section:
        checkboxes = language_section.find_all("input", {"type": "checkbox"})
        languages = [checkbox["value"] for checkbox in checkboxes]
        # Languages = All languages available on the site
    return languages
