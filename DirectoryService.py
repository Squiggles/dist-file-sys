import Pyro4
import time
import CurrentDirectory as CD

class DirectoryService(object):

    def __init__(self):
        coo = Pyro4.Proxy('PYRONAME:coordinator')
        curry = CD.CurrentDirectory('home','')
        for system in coo.getSystems():
            fs = Pyro4.Proxy('PYRONAME:filesystem.' + system)
            curry.addDir(fs.buildDir())
        curry.toplevel = True
        self.directory = curry
        print self.directory.toString()
        
        self.timemap = {}   #map from paths to time accessed
        for p in self.getPaths():
            self.timemap[p] = time.time()
        
        print 'Timestamps:'
        for i in self.timemap.items():
            print i
        
    def navigate(self,path):
        if path == []: return self.directory
        cd = self.directory
        for d in path:
            cd = self.changeDirectory(d, cd)
        return cd
    
    # Shows contents of directory given by path
    def show(self,path):
        cd = self.navigate(path)
        return  cd.dirs+cd.files
    
    # Checks if a directory exists before changing path in Client
    def exists(self, name, path):
        cd = self.navigate(path)
        for n in cd.dirs:
            if n == name:
                return True
        return False
    
    # Changes directory to specified if possible      
    def changeDirectory(self,n, cd):
        for d in cd.curries:
            if d.name == n:
                return d
        print 'No folder ' + n
        return  cd
    
    #return a list of all files
    def getPaths(self):
        print '\nBuilding list of all filepaths for locking service:'
        return getPaths_(self.directory,[])
        
    def timeAccessed(self,path):
        return timemap[path]
            
def getPaths_(cd,paths):
    for f in cd.files:
        print cd.path+f
        paths.append(cd.path+f)
    for c in cd.curries:
        paths = getPaths_(c, paths)
    return paths
    """
        filenames = []
        for f in self.files:
            filenames.append(f)
        print "Served file list"
        return filenames
    """
    
    """
    #TODO: Look at config file for list of systems, search each one
    # End up with mapping from names to (system,path)
    def buildDirectory(self):
        filesystem = Pyro4.Proxy("PYRONAME:filesystem.robbie")
        self.files = filesystem.listFiles()
        for f in self.files.values(): print f
    """
        
    
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
