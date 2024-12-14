import requests
from bs4 import BeautifulSoup

def getPageCount(link):    
    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }
    payload = ""

    response = requests.request("GET", link, data=payload,  headers=headersList)
    pageSoup = BeautifulSoup(response.text, 'html.parser')
    
    pageNumList = pageSoup.find(class_ = "pagination").find_all("a")
    maxNumOfPages = pageNumList[len(pageNumList)-1].string
    
    return maxNumOfPages

def populateDBWithMedicPageInfo():
    reqUrl = f"https://www.medindia.net/drug-price/brand/index.htm?alpha=a"
    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }
    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    pageSoup = BeautifulSoup(response.text, 'html.parser')
    
    listOfLinkInHtml = pageSoup.find(class_='az-list').find_all("a")
    
    linksList = []
    for link in listOfLinkInHtml:
        linksList.append( link.get("href") )
    
    linkAndPageCountDict = {}
    for link in linksList:
        pageCount = getPageCount(link)
        linkAndPageCountDict[link] = pageCount
        
    return linkAndPageCountDict


    