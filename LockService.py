import Pyro4

class LockService(object):
    locks = {}
    
    def getList(self):
        directoryservice = Pyro4.Proxy("PYRONAME:directoryservice")
        files = directoryservice.getList()
        for f in files: self.locks[f] = False
        for l in self.locks.items(): print l
    
    def requestLock(self,f):
        if self.locks[f] == False:
            self.locks[f] = True
            print f + " locked"
            result = True
        else:
            print f + " already locked"
            result = False
        for l in self.locks.items(): print l
        return result
        
lockservice = LockService()
lockservice.getList()

daemon = Pyro4.Daemon()                     # make Pyro daemon
ns = Pyro4.locateNS()                       # find name server
uri = daemon.register(lockservice)      # register filesystem
ns.register("lockservice", uri)         # register with name in name server

print "Ready"
daemon.requestLoop()                        # wait
