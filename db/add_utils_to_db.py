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
    utils_collection.insert_one(utils_document)