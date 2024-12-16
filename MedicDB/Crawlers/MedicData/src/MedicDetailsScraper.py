import urllib.parse
import PyMongoOps as pymoops
import http_reqs.GetDrugDetails as getDrugDetails
import logging

logging.basicConfig(
    filename='D:/Medic/MediGo/ProgramLog.log',
    level=logging.INFO,
    format='Details Scraper %(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

def encodeUrl(url):
    parsed_url = urllib.parse.urlparse(url)
    
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    encoded_query = {}
    for key, values in query_params.items():
        encoded_values = [urllib.parse.quote_plus(value) for value in values]
        encoded_query[key] = encoded_values

    encoded_query_string = urllib.parse.urlencode(encoded_query, doseq=True)
    encoded_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{encoded_query_string}"
    
    urlList = []
    urlList.append(encoded_url)
    urlList.append(url.split(" ")[0])
    return urlList

def startScraping():
    logging.info("Scraping process started.")
    for drugName in pymoops.getMedicNames():
        try:
            url = f'https://www.1mg.com/search/all?name={drugName}'
            logging.info(f"Processing drug: {drugName}")
            drugDetails = getDrugDetails.getDrugDetailsFrom1Mg(encodeUrl(url), drugName)
            if drugDetails:
                pymoops.insertDrugDetails1Mg(drugDetails)
                logging.info(f"Successfully inserted details for drug: {drugName}")
            else:
                logging.info(f"No details found for drug: {drugName}")
        except Exception as e:
            logging.error(f"Error occurred while processing drug: {drugName}, Error: {e}")
    logging.info("Scraping process completed.")
