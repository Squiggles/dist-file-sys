import Pyro4

class DirectoryServer(object):
    example = {"lol.txt" : ("FileServer",""), "test.txt" : ("FileServer", "")}
    
    def getFilepath("filename"):
        


directoryserver = DirectoryServer

daemon = Pyro4.Daemon()             # make Pyro daemon
ns = Pyro4.locateNS()               # find name server
uri = daemon.register(filesystem)   # register filesystem
ns.register("FileSystem", uri)      # register with name in name server

print "Ready."
daemon.requestLoop()                # wait
