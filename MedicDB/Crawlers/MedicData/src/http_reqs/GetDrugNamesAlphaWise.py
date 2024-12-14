import requests
from bs4 import BeautifulSoup

#pageNum => page=2&
def getDrugNamesAlphaWise(alphabet,pageNum):
    reqUrl = f"https://www.medindia.net/drug-price/brand/index.htm?{pageNum}alpha={alphabet}"
    
    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }
    
    payload = ""
    
    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    
    return response