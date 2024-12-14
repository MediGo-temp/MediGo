import logging
from http_reqs import GetDrugNamesAlphaWise as drugNameScraper
from http_reqs import GetUrlsAndMaxPageNum as drugPageInfoScrapper
import PyMongoOps as pymops

# Set up logging to log messages to a file
logging.basicConfig(
    filename='D:/Medic/MediGo/ProgramLog.log',  # Path to your log file
    level=logging.INFO,  # Log level (INFO and above)
    format='Name Scrapper %(asctime)s - %(levelname)s - %(message)s',  # Log message format
    filemode='a'  # Append mode
)

def main():
    try:
        logging.info("Script started.")
        
        if False:
            logging.info("Fetching drug page info...")
            linkAndPageCountDict = drugPageInfoScrapper.populateDBWithMedicPageInfo()
            logging.info(f"Fetched {len(linkAndPageCountDict)} URLs with page counts.")

            logging.info("Inserting URL and page count data into MongoDB...")
            pymops.insertUrlAndPageCount(linkAndPageCountDict)
            logging.info("Data insertion into MongoDB completed.")
                    
        logging.info("Started fetching data from pages.")
        
        result_dict = pymops.getUrlAndPageCountFromDB()
        
        logging.info(f"Fetched {len(result_dict)} records from MongoDB.")
        
        logging.info(f"Started fetching data for every alphabet.")
        
        drugNameScraper.startScraping(result_dict)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

# Run the main function
if __name__ == "__main__":
    main()
