import Pyro4

class LockService(object):
    locks = {}
    
    def getList(self):
        directoryservice = Pyro4.Proxy("PYRONAME:directoryservice")
        files = directoryservice.getList()
        for f in files:
            self.locks[f] = False
    
    def requestLock(self,f):
        if self.locks[f] == False:
            self.locks[f] = True
            return True
        else: return False
        
lockservice = LockService()
lockservice.getList()

daemon = Pyro4.Daemon()                     # make Pyro daemon
ns = Pyro4.locateNS()                       # find name server
uri = daemon.register(lockservice)      # register filesystem
ns.register("lockservice", uri)         # register with name in name server

print "Ready"
daemon.requestLoop()                        # wait
