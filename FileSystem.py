import Pyro4
import os
import sys

import CurrentDirectory as CD

# Class representing the file system 
class FileSystem(object):
    
    # Each system has a name and a private directory
    def __init__(self,n):
        self.system = n
        self.name = n + 'files'
        self.path = self.name + '/'
        
    
        
    # Build a representative directory structure for the directory service
    def buildDir(self):
        top = _buildDir(self.name,self.path)
        top.system = self.system
        return top

    # Build a mapping between filename and (system,path)
    def listFiles(self):
        print 'Servicing request for file dictionary'
        return _listFiles(self.path,self.path)
        
    #TODO : Reimplement reading, writing etc

    # Read from the specified file and return the contents
    def readFile(self, path):
        try:
            f = open(path,'r')
            print "Read @ " + path
            return f.read()
        except IOError as e:
            print 'Read attempt on nonexistant file @ ' + path
            return 'ERROR: file doesn\'t exist'
            
    def readLine(self, path, i):
        try:
            f = open(path,'r')
            contents = f.read().split('\n')
            print "Read @ " + path
            if i < len(contents):
                return contents[i]
            else:
                return -1
        except IOError as e:
            print 'Read attempt on nonexistant file @ ' + path
            return 'ERROR: file doesn\'t exist'

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

# Build a representative directory structure for the directory service
def _buildDir(name,path):
    curry = CD.CurrentDirectory(name,path)
        
    for item in os.listdir(path):
        addr = os.path.join(path,item)

        if os.path.isfile(addr):
            curry.addFile(item)
        elif os.path.isdir(addr):
            curry.addDir(_buildDir(item, path + item + "/"))
                
    return curry

coo = Pyro4.Proxy('PYRONAME:coordinator')
systems = coo.getSystems()

# Start servers
daemon = Pyro4.Daemon()             # make Pyro daemon
ns = Pyro4.locateNS()               # find name server
for fs in systems:
    filesystem = FileSystem(fs)
    uri = daemon.register(filesystem)       # register filesystem
    ns.register('filesystem.'+fs, uri)      # register with name in name server
    print 'filesystem.' + fs + ' ready'

daemon.requestLoop()                # wait
