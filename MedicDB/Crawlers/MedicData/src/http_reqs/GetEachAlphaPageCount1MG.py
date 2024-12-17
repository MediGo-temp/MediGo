import requests
from bs4 import BeautifulSoup
import PyMongoOps as pymongoops
import logging

logging.basicConfig(
    filename='D:/Medic/MediGo/ProgramLog.log',
    level=logging.INFO,
    format='1Mg Page Count %(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)


headersList = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36/Thunder Client (https://www.thunderclient.com)" 
}

payload = ""

def getPageCount(url):
    try:
        response = requests.request("GET", url, data=payload, headers=headersList)
        pageSoup = BeautifulSoup(response.text, 'html.parser')
        
        listofPointers = pageSoup.find_all(class_='list-pagination')
        lastSecondBecauseTheNumberIsThere = -2
        
        pageCount = int(listofPointers[0].find_all('a')[lastSecondBecauseTheNumberIsThere].string)
        
        response = {
            "url" : url,
            "pageCount" : pageCount
        }
        
        return response
                        
    except Exception as e:
        logging.error(f"Error occurred while scraping {url}: {e}")

