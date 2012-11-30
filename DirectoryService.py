import Pyro4

class DirectoryService(object):
    files = {}
    
    def getList(self):
        filenames = []
        for f in self.files:
            filenames.append(f)
        return filenames
    
    #TODO: Look at configfile for list of systems, search each one
    def buildDirectory(self):
        filesystem = Pyro4.Proxy("PYRONAME:filesystem.robbie")
        self.files = filesystem.listFiles()
        print self.files
    
    def lookup(self,filename):
        print "Lookup for " + filename
        try:
            return self.files[filename]
        except KeyError as ke:
            return (None,"File does not exist")

directoryservice = DirectoryService()
directoryservice.buildDirectory()

daemon = Pyro4.Daemon()                     # make Pyro daemon
ns = Pyro4.locateNS()                       # find name server
uri = daemon.register(directoryservice)      # register filesystem
ns.register("directoryservice", uri)         # register with name in name server

print "Ready"
daemon.requestLoop()                        # wait
