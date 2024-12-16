import requests
from bs4 import BeautifulSoup
import PyMongoOps as pymongoops
import logging
import time

logging.basicConfig(
    filename='D:/Medic/MediGo/ProgramLog.log',
    level=logging.INFO,  
    format='GETDRUGDETAILS %(asctime)s - %(levelname)s - %(message)s',  
    filemode='a'
)

headersList = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36/Thunder Client (https://www.thunderclient.com)" 
}

def getDrugDetailsFrom1Mg(urlList, drugName):
    logging.info(f"Starting to scrape data from link: {urlList}")
    
    payload = ""
    OneMgUrls = {}
    for url in urlList:
        try:
            logging.info(f"Sending GET request to {url}")
            response = requests.request("GET", url, data=payload, headers=headersList)
            
            # Log response status
            if response.status_code == 200:
                logging.info(f"Successfully fetched data for {drugName} from {url}")
            else:
                logging.warning(f"Received unexpected status code {response.status_code} for {drugName} from {url}")

            pageSoup = BeautifulSoup(response.text, 'html.parser')
            
            logging.info("Parsing the page content.")
            
            listofDrugOnPage = pageSoup.find_all(class_='row style__grid-container___3OfcL')
            
            if not listofDrugOnPage:
                logging.warning(f"No drug data found on page for {drugName}. URL: {url}")
            else:
                logging.info(f"Drug data found on page for {drugName}. URL: {url}")
                
            
            for drugs in listofDrugOnPage:
                try:
                    drug_link = drugs.find('a')['href']
                    full_url = f"https://www.1mg.com{drug_link}"
                    OneMgUrls[full_url] = drugName
                    logging.info(f"Found drug URL: {full_url} for drug: {drugName}")
                except Exception as e:
                    logging.error(f"Error processing drug data for {drugName}: {e}")

            if OneMgUrls:
                logging.info(f"Successfully scraped {len(OneMgUrls)} URLs for {drugName}")
            else:
                logging.warning(f"No valid URLs found for {drugName}.")                        

        except Exception as e:
            logging.error(f"Error occurred while scraping {url} for {drugName}: {e}")
    return OneMgUrls
