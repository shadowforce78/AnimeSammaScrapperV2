import json
from typing import List, Dict, Optional
from db.connect import client


def add_episodes_to_db(
    episodes_data: List[Dict],
    save_to_db: bool = True,
    db_name: str = "AnimeSama",
    collection_name: str = "episodes",
) -> int:
    """
    Insert or update pre-parsed episodes data into MongoDB.

    Args:
        episodes_data: list of episode entries (each entry should contain at least 'title' and 'episodes')
        save_to_db: whether to upsert the data into MongoDB
        db_name: MongoDB database name
        collection_name: MongoDB collection name

    Returns:
        Number of documents upserted (approximate)
    """
    if not isinstance(episodes_data, list):
        raise ValueError("episodes_data must be a list of episode entries")

    # Optionnel: sauvegarder dans un fichier

    upsert_count = 0

    if save_to_db and episodes_data:
        db = client[db_name]
        coll = db[collection_name]

        for entry in episodes_data:
            title = entry.get("title")
            if not title:
                continue
            filter_ = {"title": title}
            update = {"$set": entry}
            result = coll.update_one(filter_, update, upsert=True)
            # result.upserted_id is set when a new doc was inserted
            if getattr(result, "upserted_id", None) is not None:
                upsert_count += 1
            else:
                # If no upserted_id, it's an update; count it as well
                upsert_count += 1

    return upsert_count
