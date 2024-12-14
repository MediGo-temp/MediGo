from pymongo import MongoClient
import logging

connection_string = "mongodb://localhost:27017/medigo"
client = MongoClient(connection_string)
db = client['MediGo']

logging.basicConfig(
    filename='D:\Medic\MediGo\ProgramLog.log',  
    level=logging.INFO,  
    format='MONGO-DB %(asctime)s - %(levelname)s - %(message)s',  
    filemode='a'
)

def insertUrlAndPageCount(linkAndPageCountDict):
    collection = db['DrugsPageInfoAlpha']  # MongoDB collection
    
    logging.info("Starting to insert URL and page count data into MongoDB.")
    
    for key, value in linkAndPageCountDict.items():
        try:
            record = {
                "url": key,
                "page_count": value
            }
            # Insert the record into the collection
            insert_result = collection.insert_one(record)
            
            logging.info(f"Inserted record with URL: {key}, Page Count: {value} into MongoDB.")
        
        except Exception as e:
            logging.error(f"Error inserting record for URL {key}: {e}")

    logging.info("Completed inserting all records into MongoDB.")
    
def getUrlAndPageCountFromDB():
    collection = db['DrugsPageInfoAlpha']  # MongoDB collection
    
    logging.info("Fetching URL and page count data from MongoDB.")
    
    try:
        cursor = collection.find()
        
        result_dict = {record['url']: record['page_count'] for record in cursor}        
        
        return result_dict
    
    except Exception as e:
        logging.error(f"Error fetching data from MongoDB: {e}")
        return {}

def insertDrugName(drugName):
    collection = db['DrugsName']  # MongoDB collection
    
    try:
        record = {
            "drugname" : drugName
        }
        # Insert the record into the collection
        insert_result = collection.insert_one(record)
        
        logging.info(f"Inserted record  {drugName}")
    
    except Exception as e:
        logging.error(f"Error inserting record for  {drugName}: {e}")

    logging.info("Completed inserting all records into MongoDB.")
