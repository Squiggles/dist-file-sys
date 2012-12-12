import Pyro4

#TODO:  Timeout? Tell FileSystem to reject client, wait for confirmation before unlocking again.
#       Store system time with lock when taken. If lock requested by another client and difference
#       with current time big enough, kick original lock guy. Need identity of locker?

#TODO:  Should the file system check with the file server before allowing access?

#TODO:  This might all need to be drastically overhauled to fit in with the new system

class LockService(object):
    locks = {}
    
    def getList(self):
        directoryservice = Pyro4.Proxy("PYRONAME:directoryservice")
        paths = directoryservice.getPaths()
        print 'Received list of filepaths from directory service'
        for p in paths: 
            print p
            self.locks[p] = False
    
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
        
    #TODO: Need identity to prevent foul play?
    def releaseLock(self,f):
        self.locks[f] = False
        for l in self.locks.items(): print l
        
lockservice = LockService()
lockservice.getList()

daemon = Pyro4.Daemon()                     # make Pyro daemon
ns = Pyro4.locateNS()                       # find name server
uri = daemon.register(lockservice)          # register filesystem
ns.register("lockservice", uri)             # register with name in name server

print "Ready"
daemon.requestLoop()                        # wait
