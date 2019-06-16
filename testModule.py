import random

class Errors:
    codeError = 0
    proxyError = 1

succ = {
        "success": True,
        "result" : [random.randint(0,100) for i in range(random.randint(0,100))]
        }

codeE = {
        "success": False,
        "error" : Errors.codeError
        }

proxyE = {
        "success": False,
        "error" : Errors.proxyError
        }

def work(code,proxy,counters):
    res = random.choice([ succ] * 1 + [codeE] + [proxyE])
    return res

def workProxyLess(code,counters):
    return work(code,None,counters)
