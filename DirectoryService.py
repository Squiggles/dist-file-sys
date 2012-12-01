import Pyro4

class DirectoryService(object):
    
    def show(self,path):
        dirs = path.split('/')
        for d in tokens:
            self.directory
    
    def getList(self):
        filenames = []
        for f in self.files:
            filenames.append(f)
        print "Served file list"
        return filenames
    
    #TODO: Look at config file for list of systems, search each one
    def buildDirectory(self):
        filesystem = Pyro4.Proxy("PYRONAME:filesystem.robbie")
        self.files = filesystem.listFiles()
        for f in self.files.values(): print f
        
    def getDir(self):
        filesystem = Pyro4.Proxy("PYRONAME:filesystem.robbie")
        self.directory = filesystem.buildDir()
        self.directory.toString()
    
    def lookup(self,filename):
        print "Lookup for " + filename
        try:
            return self.files[filename]
        except KeyError as ke:
            return (None,"File does not exist")

directoryservice = DirectoryService()
directoryservice.buildDirectory()
directoryservice.getDir()

daemon = Pyro4.Daemon()                     # make Pyro daemon
ns = Pyro4.locateNS()                       # find name server
uri = daemon.register(directoryservice)      # register filesystem
ns.register("directoryservice", uri)         # register with name in name server

print "Ready"
daemon.requestLoop()                        # wait
