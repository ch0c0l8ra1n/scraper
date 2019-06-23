from scraper import Errors
from template_config import threadCount, codesFile, proxiesFile

proxyError = {
        "success": False,
        "error" : Errors.proxyError
        }

codeError = {
        "success": False,
        "error" : Errors.codeError
        }

with open(codesFile) as lines:
    for line in lines:
        line = line.strip("\n")
        code = # Extract the code from the line
        codes.append( code )

with open(proxiesFile) as lines:
    for line in lines:
        line = line.strip("\n")
        proxy = # Extract the code from the line
        proxies.append( proxy )
