from db.connect import client

def add_utils_to_db(data):
    db = client["AnimeSama"]
    utils_collection = db["utils"]
    genres = data.get("genres", [])
    languages = data.get("languages", [])
    types = data.get("types", [])
    
    utils_document = {
        "genres": genres,
        "languages": languages,
        "types": types
    }
    
    # Add a static identifier for the utils document
    utils_document["id"] = "global_utils"
    
    utils_collection.update_one(
        {"id": "global_utils"},
        {"$set": utils_document},
        upsert=True
    )