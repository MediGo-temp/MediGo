import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    filename='D:/Medic/MediGo/ProgramLog.log',
    level=logging.INFO,  
    format='GETURL %(asctime)s - %(levelname)s - %(message)s',  
    filemode='a'
)

def getPageCount(link):    
    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }
    payload = ""
    
    logging.info(f"Fetching page count for link: {link}")
    
    try:
        response = requests.request("GET", link, data=payload, headers=headersList)
        response.raise_for_status()  
        pageSoup = BeautifulSoup(response.text, 'html.parser')
        
        pageNumList = pageSoup.find(class_="pagination").find_all("a")
        maxNumOfPages = pageNumList[len(pageNumList)-1].string
        
        logging.info(f"Found max page number: {maxNumOfPages}")
        return maxNumOfPages
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching page count for {link}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error while processing {link}: {e}")
        return None

def populateDBWithMedicPageInfo():
    reqUrl = "https://www.medindia.net/drug-price/brand/index.htm?alpha=a"
    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }
    payload = ""
    
    logging.info(f"Fetching links and page count from: {reqUrl}")
    
    try:
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        response.raise_for_status()  
        pageSoup = BeautifulSoup(response.text, 'html.parser')
        
        listOfLinkInHtml = pageSoup.find(class_='az-list').find_all("a")
        
        linksList = []
        for link in listOfLinkInHtml:
            linksList.append(link.get("href"))
        
        linkAndPageCountDict = {}
        logging.info(f"Processing {len(linksList)} links")
        
        for link in linksList:
            logging.info(f"Fetching page count for {link}")
            pageCount = getPageCount(link)
            if pageCount:
                linkAndPageCountDict[link] = pageCount
        
        logging.info("Completed fetching page counts for all links.")
        return linkAndPageCountDict
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {reqUrl}: {e}")
        return {}
    except Exception as e:
        logging.error(f"Unexpected error during processing: {e}")
        return {}
