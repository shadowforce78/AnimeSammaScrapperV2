import json
from typing import List, Dict, Optional
from db.connect import client


def add_scans_to_db(scans_data: List[Dict], save_to_file: Optional[str] = None, save_to_db: bool = True, db_name: str = "AnimeSama", collection_name: str = "scans") -> int:
    """
    Insert or update pre-parsed scans data into MongoDB.
    
    Structure expected:
    [
      {
        "title": "Solo Leveling",
        "link": "https://anime-sama.org/catalogue/solo-leveling/",
        "type": "Scans",
        "scans": {
          "scan": { "url": "...", "title": "...", "chapters": [...] },
          "scan_side_story": { ... },
          ...
        }
      }
    ]

    Args:
        scans_data: list of anime entries with their scans grouped by scan type
        save_to_file: if provided, the data will also be written to this JSON file
        save_to_db: whether to upsert the data into MongoDB
        db_name: MongoDB database name
        collection_name: MongoDB collection name

    Returns:
        Number of documents upserted
    """
    if not isinstance(scans_data, list):
        raise ValueError("scans_data must be a list of anime entries with scans")

    # Optionnel: sauvegarder dans un fichier
    if save_to_file:
        with open(save_to_file, 'w', encoding='utf-8') as f:
            json.dump(scans_data, f, ensure_ascii=False, indent=2)

    upsert_count = 0

    if save_to_db and scans_data:
        db = client[db_name]
        coll = db[collection_name]

        for entry in scans_data:
            title = entry.get("title")
            if not title:
                continue
            
            # Upsert based on title to have one document per anime
            filter_ = {"title": title}
            update = {"$set": entry}
            result = coll.update_one(filter_, update, upsert=True)
            
            # Count upserts
            if getattr(result, 'upserted_id', None) is not None:
                upsert_count += 1
            elif result.modified_count > 0:
                upsert_count += 1

    return upsert_count
