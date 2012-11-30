import Pyro4
import os
import sys

# Class representing the file system 
class FileSystem(object):
    path = "files/"
    name = "Default"
    
    def __init__(self,n):
        self.name = n
        self.path = n + self.path

    #listFiles::[String]
    def listFiles(self):
        print "Servicing request for file dictionary."
        return _listFiles(self.name,self.path)

    # Read from the specified file and return the contents
    def readFile(self, path):
        try:
            f = open(path,'r')
            temp = f.read()
            f.close()
            print "Read @ " + path + "."
            return temp
        except IOError as e:
            print "Read attempt on nonexistant file @ " + path + "."
            pass

    # Create a new file or overwrite the previous, inserting the supplied text.
    def writeFile(self, path, text):
        f = open(path,'w+')
        f.write(text)
        f.close()
        print "Write @ " + path + "."

    # Append text to the end of the specified file
    def appendFile(self, path, text):
        try:
            f = open(path, 'a')
            f.write(text)
            f.close()
            print "Append @ " + path
        except IOError as e:
            print "Append attempt on nonexistant file @ " + path
            pass

# Recursively builds dictionary of name to (serverID,path) pairs
def _listFiles(name,path):
    files = {}
    for item in os.listdir(path):
        addr = os.path.join(path,item)
        if os.path.isfile(addr):
            # Enter new (key,value) pair
            files[item] = (name,addr)
        else:
            # Recurse and integrate results with existing dictionary
            files = dict(files.items() + _listFiles(name,addr).items())
    return files

#TODO: Build many systems according to configuration file
name = sys.argv[1]
filesystem = FileSystem(name)

daemon = Pyro4.Daemon()             # make Pyro daemon
ns = Pyro4.locateNS()               # find name server
uri = daemon.register(filesystem)   # register filesystem
ns.register("filesystem."+name, uri)      # register with name in name server

print "filesystem." + name
print "Ready."
daemon.requestLoop()                # wait
