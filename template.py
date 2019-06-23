import requests
from scrapers import Errors, Scraper , safeWrite
import threading
from template_helpers import *

# Use lock when updating counters
lock = threading.Lock()

def work(code,proxy,counters):
    pass

def workProxyLess(code,counters):
    pass

def main():
    scraper = Scraper(work,threadCount)
    scraper.loadCodes(codes)
    scraper.loadProxies(proxies)
    res = scraper.scrape()
    print(res)

if __name__ == "__main__":
    main()
