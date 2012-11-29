import Pyro4

class DirectoryService(object):
    files = {}
    
    def buildDirectory(self):
        filesystem = Pyro4.Proxy("PYRONAME:filesystem.luke")
        self.files = filesystem.listFiles()
        print self.files
    
    def lookup(self,filename):
        print "Lookup for " + filename
        return self.files[filename]

directoryservice = DirectoryService()
directoryservice.buildDirectory()

daemon = Pyro4.Daemon()                     # make Pyro daemon
ns = Pyro4.locateNS()                       # find name server
uri = daemon.register(directoryservice)      # register filesystem
ns.register("directoryservice", uri)         # register with name in name server

print "Ready"
daemon.requestLoop()                        # wait
