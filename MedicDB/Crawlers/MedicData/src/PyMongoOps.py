from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/medigo"
client = MongoClient(connection_string)
db = client['MediGo']

def insertUrlAndPageCount(linkAndPageCountDict):
    collection = db['DrugsPageInfoAlpha']
    for key, value in linkAndPageCountDict.items():
        record  = {
            "url": key,
            "page_count": value
        }
        collection.insert_one(record)
