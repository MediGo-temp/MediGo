from http_reqs import GetDrugNamesAlphaWise as drugNameScraper
from http_reqs import GetUrlsAndMaxPageNum as drugPageInfoScrapper
import PyMongoOps as pymops

linkAndPageCountDict = drugPageInfoScrapper.populateDBWithMedicPageInfo()
pymops.insertUrlAndPageCount(linkAndPageCountDict)
print("Completed")
