import requests
from bs4 import BeautifulSoup
import PyMongoOps as pymongoops
import logging

logging.basicConfig(
    filename='D:/Medic/MediGo/ProgramLog.log',
    level=logging.INFO,  
    format='GETDRUGNAME %(asctime)s - %(levelname)s - %(message)s',  
    filemode='a'
)

def insertDrugNamesFromPageToMongo(link):
    logging.info(f"Starting to scrape data from link: {link}")
    
    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }
    
    payload = ""
    
    try:
        response = requests.request("GET", link, data=payload, headers=headersList)
        pageSoup = BeautifulSoup(response.text, 'html.parser')
        
        listofDrugNamesOnPage = pageSoup.find_all(class_='index-list-grid')

        for druglist in listofDrugNamesOnPage:    
            for drugname in druglist.find_all('li'):
                drugnameA = drugname.find('a')  
                if drugnameA and drugnameA.string:
                    pymongoops.insertDrugName(drugnameA.string)
                    logging.info(f"Inserted drug name: {drugnameA.string}")
                    
    except Exception as e:
        logging.error(f"Error occurred while scraping {link}: {e}")

def startScraping(result_dict):
    logging.info("Starting the scraping process.")
    
    for link, pageCount in result_dict.items():
        logging.info(f"Scraping data from link: {link} with {pageCount} pages.")
        
        for pageNum in range(1, int(pageCount) + 1):
            full_link = f"{link}&page={pageNum}" if pageNum > 1 else link
            logging.info(f"Processing page {pageNum} of {pageCount} for link: {full_link}")
            
            insertDrugNamesFromPageToMongo(full_link)
            
    logging.info("Scraping process completed.")

