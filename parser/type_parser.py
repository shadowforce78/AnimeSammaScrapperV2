def parse_types(soup):
    """Return a list of types from the catalogue page soup.

    If the section is absent, return an empty list.
    """
    types = []
    type_section = soup.find(id="filtres_types")
    if not type_section:
        return types

    checkboxes = type_section.find_all("input", {"type": "checkbox"})
    for checkbox in checkboxes:
        value = checkbox.get("value")
        if value:
            types.append(value.strip())

    # Remove duplicates while preserving order
    seen = set()
    cleaned = []
    for t in types:
        if t not in seen:
            seen.add(t)
            cleaned.append(t)

    return cleaned
