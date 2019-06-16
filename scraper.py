from multiprocessing.pool import ThreadPool
import testModule
import threading

#Lock object, Used to update the codes, proxies and the counters
lock = threading.Lock()

class Errors:
    '''
    Errors class
    Like enums
    '''
    codeError = 0
    proxyError = 1

class Worker():
    '''
    Equivalent to one of the threads.
    Takes the work function, codes and proxies as inputs
    '''
    def __init__(self,workerId,work,codes,proxies):
        '''
        Initialization
        codes and proxies are shared betwen workers so remember
        to acquire lock before using it
        '''
        self.workerId = workerId
        self.work = work
        self.codes = codes
        self.proxies = proxies
        self.rotating = False
        self.counters=None

    def setCounters(self,counters):
        '''
        counters is the object that is shared betwen the Checker, Worker
        and the worker function
        Remember to acquire the lock before updating counters 
        '''
        self.counters = counters

    def proxiesRotation(self,rot):
        '''
        Set if the proxies are rotating or not.
        Initial value is False
        '''
        self.rotating = rot

    def getResult(self):
        '''
        Performs the "work" passed during initialization
        till either the codes or proxy run out and return a list
        of all the results by the work function
        '''
        results = []

        code = self.getCode()
        proxy = self.getProxy()
        
        while code != None and proxy != None:
            #While codes or proxies aren't depleted
            resp = self.work(code,proxy,self.counters)    

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
        '''
        Checks if codes are depleted
        '''
        return len(self.codes) > 0

    def proxiesRemaining(self):
        '''
        Checks if the proxies are depleted
        '''
        return len(self.proxies) > 0
    
    def getCode(self):
        '''
        Safely return a code if its available
        or return a None object
        '''
        with lock:
            if self.codesRemaining():
                code = self.codes.pop()
                return code
            return None

    def getProxy(self):
        '''
        Safely return a proxy if its available
        or return a None object
        '''
        with lock:
            if self.proxiesRemaining():
                proxy = self.proxies.pop()
                if self.rotating:
                    self.proxies = [proxy] + self.proxies
                return proxy
            return None
        
        

class Checker():
    '''
    Checker object.
    runs the work function till the codes or the proxy run out,
    on various threads (default = 100 )
    '''
    def __init__(self,work,threadCount=100):
        '''
        Initialization
        '''
        self.work = work
        self.codes = []
        self.proxies = []
        self.threadCount=100
        self.rotating = False
        self.counters = {
                }

    def loadCodes(self,codes):
        '''
        Loads the codes
        '''
        self.codes = codes

    def loadProxies(self,proxies,rot=False):
        '''
        Loads the proxies
        '''
        self.proxies = proxies
        self.rotating=rot

    def check(self):
        '''
        "Checks" the codes against the supplied proxies
        By instantiating worker classes
        '''
        pool = ThreadPool(self.threadCount)
        
        workers = [ 
                Worker(i,self.work,self.codes,self.proxies) 
                for i in range(self.threadCount)]
        
        for worker in workers:
            worker.proxiesRotation(self.rotating)
            worker.setCounters(self.counters)

        results = pool.map( lambda worker: worker.getResult() , workers )
        pool.close()

        return results
        


def main():
    checker = Checker(testModule.work)
    checker.loadCodes( list(range(100000)) )
    checker.loadProxies( list(range(100000)) )
    res = checker.check()
    print(res)

if __name__ == "__main__":
    main()
