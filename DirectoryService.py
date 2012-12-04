import Pyro4

class DirectoryService(object):

    def __init__(self):
        self.getDir()
    
    # Shows contents of directory given by path
    def show(self,path):
        dirs = path.split('/')
        cd = self.directory
        if path == '': return cd.dirs + cd.files
        
        for d in dirs:
            cd = self.changeDirectory(d)
         
        return  cd.dirs+cd.files
    
    # Checks if a directory exists before changing path in Client
    def exists(self, name):
        for n in self.directory.dirs:
            if n == name:
                return True
        return False
    
    # Changes directory to specified if possible      
    def changeDirectory(self,n):
        for d in self.directory.curries:
            if d.name == n:
                return d
        print 'No folder ' + n
        return self
    
    #return a list of all files
    def getList(self):
        filenames = []
        for f in self.files:
            filenames.append(f)
        print "Served file list"
        return filenames
    """
    #TODO: Look at config file for list of systems, search each one
    # End up with mapping from names to (system,path)
    def buildDirectory(self):
        filesystem = Pyro4.Proxy("PYRONAME:filesystem.robbie")
        self.files = filesystem.listFiles()
        for f in self.files.values(): print f
    """
    #TODO : Handle multiple file systems
    # Retrieve directory from filesystem
    def getDir(self):
        filesystem = Pyro4.Proxy("PYRONAME:filesystem.robbie")
        self.directory = filesystem.buildDir()
        print self.directory.toString()
    
    """
    # Return (system,path) for given filename
    def lookup(self,filename):
        print "Lookup for " + filename
        try:
            return self.files[filename]
        except KeyError as ke:
            return (None,"File does not exist")
    """
directoryservice = DirectoryService()
#directoryservice.buildDirectory()

daemon = Pyro4.Daemon()                     # make Pyro daemon
ns = Pyro4.locateNS()                       # find name server
uri = daemon.register(directoryservice)      # register filesystem
ns.register("directoryservice", uri)         # register with name in name server

print "Ready"
daemon.requestLoop()                        # wait
