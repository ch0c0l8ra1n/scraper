from multiprocessing.pool import ThreadPool
import testModule


class Errors:
    codeError = 0
    proxyError = 1

class Worker():
    def __init__(self,workerId,work,codes,proxies):
        self.workerId = workerId
        self.work = work
        self.codes = codes
        self.proxies = proxies
        self.rotating = False

    def proxiesRotation(self,rot):
        self.rotating = rot

    def getResult(self):
        results = []

        code = self.getCode()
        proxy = self.getProxy()
        
        while code != None and proxy != None:
            resp = self.work(code,proxy)    

            if "success" not in resp:
                print("Module not configured properly")
                return results

            if resp["success"]:
                results += resp["result"]

            else:
                if resp["error"] == Errors.codeError:
                    code = self.getCode()
                
                elif resp["error"] == Errors.proxyError:
                    proxy = self.getProxy()
        
        return results
            
            
    def codesRemaining(self):
        return len(self.codes) > 0

    def proxiesRemaining(self):
        return len(self.codes) > 0
    
    def getCode(self):
        if self.codesRemaining():
            code = self.codes.pop()
            return code
        return None

    def getProxy(self):
        if self.proxiesRemaining():
            proxy = self.proxies.pop()
            if self.rotating:
                self.proxies = [proxy] + self.proxies
            return proxy
        return None
        
        

class Checker():
    def __init__(self,module,threadCount=100):
        self.module = module
        self.codes = []
        self.proxies = []
        self.threadCount=100
        self.rotating = False

    def loadCodes(self,codes):
        self.codes = codes

    def loadProxies(self,proxies,rot=False):
        self.proxies = proxies
        self.rotating=rot

    def check(self):
        pool = ThreadPool(self.threadCount)
        
        workers = [ 
                Worker(i,self.module,self.codes,self.proxies) 
                for i in range(self.threadCount)]
        
        for worker in workers:
            worker.proxiesRotation(self.rotating)

        results = pool.map( lambda worker: worker.getResult() , workers )
        pool.close()

        return results
        


def main():
    checker = Checker(testModule.work)
    res = checker.check()
    print(res)

if __name__ == "__main__":
    main()

