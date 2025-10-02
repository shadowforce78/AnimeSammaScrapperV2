from db.connect import client


# exemple of oeuvre :
# {
#     "link": "https://anime-sama.fr/catalogue/solo-leveling/",
#     "image": "https://cdn.statically.io/gh/Anime-Sama/IMG/img/contenu/solo-leveling0.jpg",
#     "title": "Solo Leveling",
#     "alt_title": "Only I level up",
#     "genres": [
#       "Action",
#       "Fantasy"
#     ],
#     "type": "Anime, Scans",
#     "language": "VOSTFR, VF, VASTFR",
#     "details": {
#       "titre_principal": "Solo Leveling",
#       "titre_alternatif": "Only I level up",
#       "avancement": "Aucune donnée.",
#       "correspondance": "Saison 2 Episode 13 -> Chapitre 108",
#       "synopsis": "Dix ans auparavant, des portails ont commencé à apparaître un peu partout dans le monde. Ces portails ont la particularité de connecter le monde à d'autres dimensions, donjons ou mondes parallèles. En même temps, certaines personnes ont développé des capacités afin de pouvoir chasser ces portails. On appelle ceux qui reçoivent un Éveil, des Chasseurs.\r\n\r\nSung Jin Woo est considéré comme le plus faible des Chasseurs de rang E... Autrement dit le plus faible parmi les faibles. Il est tellement faible qu'il est surnommé par ses confrères, le « Faible ». Avec une équipe de Chasseurs, il se rend dans un donjon de rang D. Malheureusement, l'équipe se retrouve piégée dans une salle avec des monstres qui ne sont pas du tout du niveau du donjon... S'en suit un massacre... Et Sung Jin Woo, aux portes de la mort arrive à acquérir une capacité pour le moins étrange...\r\n\r\nSung Jin Woo va-t-il réussir à devenir le plus puissant des Chasseurs tout en surmontant les épreuves et conspirations ?",
#       "genres_details": [
#         "Action",
#         "Fantasy"
#       ],
#       "anime_disponible": [
#         {
#           "nom": "Saison 1",
#           "url": "saison1/vostfr"
#         },
#         {
#           "nom": "Saison 2",
#           "url": "saison2/vostfr"
#         }
#       ],
#       "manga_disponible": [
#         {
#           "nom": "Scans",
#           "url": "scan/vf"
#         },
#         {
#           "nom": "Side Story",
#           "url": "scan_side_story/vf"
#         },
#         {
#           "nom": "Ragnarok",
#           "url": "scan_ragnarok/vf"
#         },
#         {
#           "nom": "Arise",
#           "url": "scan_arise/vf"
#         }
#       ]
#     }
#   },


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
