import PyMongoOps as pymoops
import http_reqs.GetEachAlphaPageCount1MG as getEachAlphaPageCount1MG
import http_reqs.GetDrugListFrom1MgPages as getDrugListFrom1MgPages
import logging
from bs4 import BeautifulSoup
import requests

logging.basicConfig(
    filename='D:/Medic/MediGo/ProgramLog.log',
    level=logging.INFO,
    format='1MG DRUG LIST %(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

headersList = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36/Thunder Client (https://www.thunderclient.com)" 
}
payload = ""

def getEachAlphabetPageCount():
    logging.info("Started fetching page counts for all alphabets.")
    baseUrl = 'https://www.1mg.com/drugs-all-medicines'
    for alpha in range(97, 123):
        alphabet = chr(alpha)
        try:
            if alpha == 97:
                page_count = getEachAlphaPageCount1MG.getPageCount(baseUrl)
                logging.info(f"Fetched page count for '{alphabet}' with URL: {baseUrl}.")
            else:
                page_count = getEachAlphaPageCount1MG.getPageCount(f'{baseUrl}?label={alphabet}')
                logging.info(f"Fetched page count for '{alphabet}' with URL: {baseUrl}?label={alphabet}.")
            pymoops.insertUrlAndPageCountFor1MG(page_count)
            logging.info(f"Inserted page count for '{alphabet}' into the database.")
        except Exception as e:
            logging.error(f"Error fetching or inserting page count for '{alphabet}': {e}")

def startInsertingRecordsFrom1Mg():
    logging.info("Started inserting records from 1Mg into the database.")
    urlIndex = 0
    pageCountIndex = 1
    alphaChar = 97
    try:
        page_links = pymoops.get1MgPageLinks()
        for pageInfoArr in page_links:
            alphabet = chr(alphaChar)
            logging.info(f"Processing records for alphabet '{alphabet}' with URL: {pageInfoArr[urlIndex]} and page count: {pageInfoArr[pageCountIndex]}")
            startScraping1MgMedicList(pageInfoArr[urlIndex], pageInfoArr[pageCountIndex], alphabet)
            alphaChar += 1
        logging.info("Finished inserting all records from 1Mg.")
    except Exception as e:
        logging.error(f"Error inserting records: {e}")

def startScraping1MgMedicList(url, pagecount, alphabet):
    logging.info(f"Started scraping for alphabet '{alphabet}' from URL: {url} with {pagecount} pages.")
    try:
        for pageNum in range(1, pagecount + 1):
            logging.info(f"Scraping page {pageNum} for alphabet '{alphabet}'.")
            records = insertAllMedicUrlFromPage(url, pageNum)
            pymoops.insertAllPageMedicFrom1MG(records)
            logging.info(f"Inserted records from page {pageNum} for alphabet '{alphabet}' into the database.")
    except Exception as e:
        logging.error(f"Error scraping or inserting records for alphabet '{alphabet}': {e}")

def insertAllMedicUrlFromPage(url, pageNum):
    try:
        if pageNum == 1:
            logging.info(f"Fetching records from URL: {url}")
            return getAllMedicOnPage(url)
        else:
            page_url = f'{url}&page={pageNum}'
            logging.info(f"Fetching records from URL: {page_url}")
            return getAllMedicOnPage(page_url)
    except Exception as e:
        logging.error(f"Error fetching records from page {pageNum} with URL: {url}: {e}")
        return []

def getAllMedicOnPage(url):
    MedicDataDictList = []
    response = requests.request("GET", url, data=payload, headers=headersList)
    pageSoup = BeautifulSoup(response.text, 'html.parser')
    
    allMedicsOfPage = pageSoup.find(class_='style__inner-container___3BZU9 style__product-grid___3noQW style__padding-top-bottom-12px___1-DPF').find_all('a')
    
    for medicData in allMedicsOfPage:
        try:
            medicName = medicData.find(class_='style__font-bold___1k9Dl style__font-14px___YZZrf style__flex-row___2AKyf style__space-between___2mbvn style__padding-bottom-5px___2NrDR').find('div').string
            medicUrl = medicData['href']
            medicImageUrl = medicData.find('img')['src']
            dataDict = {
                "name" : medicName,
                "url" : f'https://www.1mg.com{medicUrl}',
                "imageurl" : medicImageUrl
            }
            MedicDataDictList.append(dataDict)

        except Exception as e:
                logging.error(f"Error fetching records from h URL: {url}: {e}")
                return []
    return MedicDataDictList