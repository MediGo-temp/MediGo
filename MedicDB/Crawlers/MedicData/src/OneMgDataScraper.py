import urllib.parse
import PyMongoOps as pymoops
import http_reqs.GetEachAlphaPageCount1MG as getEachAlphaPageCount1MG
import http_reqs.GetDrugListFrom1MgPages as getDrugListFrom1MgPages
import logging

logging.basicConfig(
    filename='1MG SCRAPER D:/Medic/MediGo/ProgramLog.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

def getEachAlphabetPageCount():
    """Fetch page count for each alphabet from 1mg and insert into the database."""
    logging.info("Starting to fetch page counts for all alphabets.")
    baseUrl = 'https://www.1mg.com/drugs-all-medicines'
    for alpha in range(97, 123):  # Iterate over 'a' to 'z'
        alphabet = chr(alpha)
        try:
            if alpha == 97:
                page_count = getEachAlphaPageCount1MG.getPageCount(baseUrl)
                logging.info(f"Fetched page count for '{alphabet}' using URL: {baseUrl}")
            else:
                page_count = getEachAlphaPageCount1MG.getPageCount(f'{baseUrl}?label={alphabet}')
                logging.info(f"Fetched page count for '{alphabet}' using URL: {baseUrl}?label={alphabet}")
            
            pymoops.insertUrlAndPageCountFor1MG(page_count)
            logging.info(f"Inserted page count for '{alphabet}' into the database.")
        except Exception as e:
            logging.error(f"Error fetching or inserting page count for '{alphabet}': {e}")

def startInsertingRecordsFrom1Mg():
    """Insert drug records from 1mg into the database for all alphabets."""
    logging.info("Starting to insert records from 1mg into the database.")
    try:
        page_links = pymoops.get1MgPageLinks()
        alphaChar = 97  # Start with 'a'
        for pageInfoArr in page_links:
            alphabet = chr(alphaChar)
            url = pageInfoArr[0]
            page_count = pageInfoArr[1]
            logging.info(f"Processing records for alphabet '{alphabet}' with URL: {url} and page count: {page_count}")
            
            startScraping1MgMedicList(url, page_count, alphabet)
            alphaChar += 1
        logging.info("Finished inserting all records from 1mg.")
    except Exception as e:
        logging.error(f"Error during the insertion process: {e}")

def startScraping1MgMedicList(url, page_count, alphabet):
    """Scrape and insert records for a specific alphabet and URL."""
    logging.info(f"Starting scraping for alphabet '{alphabet}' from URL: {url} with {page_count} pages.")
    try:
        for pageNum in range(1, page_count + 1):
            logging.info(f"Scraping page {pageNum} for alphabet '{alphabet}'.")
            records = insertAllMedicUrlFromPage(url, pageNum,alphabet)
            pymoops.insertAllPageMedicFrom1MG(records)
            logging.info(f"Inserted records from page {pageNum} for alphabet '{alphabet}' into the database.")
    except Exception as e:
        logging.error(f"Error scraping or inserting records for alphabet '{alphabet}': {e}")

def insertAllMedicUrlFromPage(url, pageNum,alphabet):
    """Fetch drug records from a specific page."""
    try:
        if pageNum == 1:
            logging.info(f"Fetching records from URL: {url}")
            return getDrugListFrom1MgPages.getAllMedicOnPage(url)
        elif alphabet == 'a':
            page_url = f"{url}?page={pageNum}"
            logging.info(f"Fetching records from URL: {page_url}")
            return getDrugListFrom1MgPages.getAllMedicOnPage(page_url)
        else:
            page_url = f"{url}&page={pageNum}"
            logging.info(f"Fetching records from URL: {page_url}")
            return getDrugListFrom1MgPages.getAllMedicOnPage(page_url)
    except Exception as e:
        logging.error(f"Error fetching records from page {pageNum} with URL: {url}: {e}")
        return []

pymoops.insertAllPageMedicFrom1MG(getDrugListFrom1MgPages.getAllMedicOnPage('https://www.1mg.com/drugs-all-medicines?label=z&page=321'))
