def parse_types(soup):
    type_section = soup.find(id="filtres_types")
    if type_section:
        checkboxes = type_section.find_all("input", {"type": "checkbox"})
        types = [checkbox["value"] for checkbox in checkboxes]
        # Types = All types available on the site
    return types
