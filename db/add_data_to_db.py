from db.connect import client

def add_data_to_db(data):
    db = client["AnimeSama"]
    oeuvres_collection = db["oeuvres"]
    for item in data:
        # I want : title, alt_title, link, image, genres, type, language, details (remove already existing fields), also separate manga et anime from details
        # Remove existing fields from details
        if "details" in item:
            details = item["details"]
            keys_to_remove = ["titre_principal", "titre_alternatif", "genres_details"]
            for key in keys_to_remove:
                details.pop(key, None)
            # Separate manga and anime into their own fields
            if "anime_disponible" in details:
                item["anime_disponible"] = details.pop("anime_disponible")
            else:
                item["anime_disponible"] = []
            if "manga_disponible" in details:
                item["manga_disponible"] = details.pop("manga_disponible")
            else:
                item["manga_disponible"] = []
            item["details"] = details
        else:
            item["details"] = {}
            item["anime_disponible"] = []
            item["manga_disponible"] = []
        # Insert into DB
        oeuvres_collection.insert_one(item)
