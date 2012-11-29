import Pyro4
import os

# Class representing the file server. 
class FileServer(object):
    default = "files/"
    
    def listFiles(self):
        path = self.default
        print path
        return [f for f in os.listdir('.')]

    # Read from the specified file and return the contents
    def readFile(self, filename):
        try:
            path = self.default + filename
            f = open(path,'r')
            temp = f.read()
            f.close()
            print "Read @ " + filename + "."
            return temp
        except IOError as e:
            print "Read attempt on nonexistant file @ " + filename + "."
            pass

    # Create a new file or overwrite the previous, inserting the supplied text.
    def writeFile(self, filename,text):
        path = self.default + filename
        f = open(path,'w+')
        f.write(text)
        f.close()
        print "Write @ " + filename + "."

    # Append text to the end of the specified file
    def appendFile(self,filename,text):
        try:
            path = self.default + filename
            f = open(path, 'a')
            f.write(text)
            f.close()
            print "Append @ " + filename + "."
        except IOError as e:
            print "Append attempt on nonexistant file @ " + filename + "."
            pass
        

fileserver = FileServer()
print fileserver.listFiles()

daemon = Pyro4.Daemon()             # make Pyro daemon
ns = Pyro4.locateNS()               # find name server
uri = daemon.register(fileserver)   # register filesystem
ns.register("FileServer", uri)      # register with name in name server

print "Ready."
daemon.requestLoop()                # wait

