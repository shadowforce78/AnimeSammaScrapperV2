import json
from typing import Dict, Optional
from db.connect import client


def add_scans_to_db(scans_by_title: Dict[str, list], save_to_file: Optional[str] = None, save_to_db: bool = True, db_name: str = "AnimeSama", collection_name: str = "scans") -> int:
    """
    Insert or update pre-parsed scans data into MongoDB.

    Args:
        scans_by_title: dictionary with titles as keys and lists of scan entries as values
        save_to_file: if provided, the data will also be written to this JSON file
        save_to_db: whether to upsert the data into MongoDB
        db_name: MongoDB database name
        collection_name: MongoDB collection name

    Returns:
        Number of documents upserted (approximate)
    """
    if not isinstance(scans_by_title, dict):
        raise ValueError("scans_by_title must be a dictionary with titles as keys")

    # Optionnel: sauvegarder dans un fichier
    if save_to_file:
        with open(save_to_file, 'w', encoding='utf-8') as f:
            json.dump(scans_by_title, f, ensure_ascii=False, indent=2)

    upsert_count = 0

    if save_to_db and scans_by_title:
        db = client[db_name]
        coll = db[collection_name]

        for anime_title, scans_list in scans_by_title.items():
            for entry in scans_list:
                manga_title = entry.get("title")
                url = entry.get("url")
                if not manga_title or not url:
                    continue
                # Upsert based on manga title and url to avoid duplicates
                # Also store the anime title for reference
                entry["anime_title"] = anime_title
                filter_ = {"title": manga_title, "url": url}
                update = {"$set": entry}
                result = coll.update_one(filter_, update, upsert=True)
                # Count upserts
                if getattr(result, 'upserted_id', None) is not None:
                    upsert_count += 1
                else:
                    upsert_count += 1

    return upsert_count
