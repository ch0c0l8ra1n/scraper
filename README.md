# scraper
A generic multithreaded scraper

Usage:

```python3
# Note this is a psuedocode (parts of it) and not an actual code that you can copy and paste
from scraper import Scraper
import requests

proxies = loadProxiesFromSomewhere()
codes = loadCodesFromSomewhere()

proxyError = {
  "success": False,
  "error" : Scraper.Errors.proxyError
}

codeError = {
  "success": False,
  "error" : Scraper.Errors.codeError
}

success = {
  "success": True,
  "results" : []
}

def work(code,proxy,counters):
  '''
  This is the function you use to actually scrape the website.
  You have to pass this function to the scraper when initializing it.
  This is an example (psuedocode) to scrape ebay listings for a query
  from the code argument
  '''
  
  website = requests.get("https://ebay.com/search?{}".format(code) , proxies=proxy)
 
  if "Too many requests in website":
    return proxyError
  
  if "Invalid query" in website:
    return codeError
  
  result = []
  for searchResults in website:
    result += [ { "name": searchResults.name , "price": searchResults.price , "link": searchResults.link } ]
  
  success["results"] = result
  
  return success
  
def main():
  scraper = Scraper.Scraper()
  scraper.loadProxies(proxies)
  scraper.loadCodes(codes)
  
  results = scraper.scrape()
  
  print(results)
  
if __name__ == "__main__":
  main()
```
