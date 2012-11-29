import Pyro4

class FileSystem(object):
    def sayHello(self):
        return "Hello!\n"
    
    def readFile(self, filename):
        f = open(filename,'r+')
        return f.read()
        f.close()

filesystem = FileSystem()

daemon = Pyro4.Daemon()                   # make a Pyro daemon
ns = Pyro4.locateNS()                     # find the name server
uri = daemon.register(filesystem)              # register the greeting object as a Pyro object
ns.register("FileSystem", uri)       # register the object with a name in the name server

print "Ready."
daemon.requestLoop()                  # start the event loop of the server to wait for calls

