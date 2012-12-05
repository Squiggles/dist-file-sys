# saved as client.py
import Pyro4

def getFilename(): return raw_input('Filename: ').strip()
def getText(): return raw_input('Text: ')

def attemptAction(filename):
    #lockservice = Pyro4.Proxy("PYRONAME:directoryservice")
    return True
    
        
print 'HELLO, THIS IS CLIENT\n'

option = ''        # User command
path = []
system = ''

# Prefix of every filesystem registry address
pname = 'PYRONAME:filesystem.'
directoryservice = Pyro4.Proxy('PYRONAME:directoryservice')     # Connect to directory service
#lockservice = Pyro4.Proxy('PYRONAME:lockservice')               # Connect to lock service

def quit(option):
    return option == 'quit' or option == 'q'

#TODO: Read line by line in a loop, insert into different parts, handle failure
while not quit(option):
    command = raw_input('/'.join(['home']+path)+': ').lower().split()
    option = command[0]
    
    if option == 'ls':
        print '\t'.join(directoryservice.show(path))
        
    elif option == 'cd' and len(command) > 1:
        if command[1] == '..':
            del path[len(path)-1]
        elif directoryservice.exists(command[1],path):
            path += [command[1]]
            if len(path) == 1:
                system = directoryservice.navigate(path).system
                print system
  
    elif option == 'help' or option == 'h':
        print "I HAVE NO IDEA WHAT I'M DOING"
        
    elif option == 'read' or option == 'r' and len(command) > 1:
        filesystem = Pyro4.Proxy(pname+system)              # Access file system
        print filesystem.readFile('/'.join(path +[command[1]]))                  # Read file from server
    elif not quit(option):
        print 'Command not recognised, type h or help for assistance'
    
    # TODO: Redo most of this to fit in with new system 
    """
    elif command[0] == 'r':
        filename = getFilename()        # Get name of file from user
        # Get system name and path on that system from
        # the directory service
        (system,path) = directoryservice.lookup(filename)
        
        if system == None: print path  #contains error message
        elif not lockservice.requestLock(filename): print 
        else:
            
            filesystem = Pyro4.Proxy(pname+system)              # Access file system
            result = filesystem.readFile(path)                  # Read file from server
            print 'Read successful'
            print result
    elif command[0] == 'w':
        filename = getFilename()
        text = getText()
        
        (system,path) = directoryservice.lookup(filename)
        
        if not system == None:
            filesystem = Pyro4.Proxy(pname+system)
            filesystem.writeFile(path,text)
            print 'Write successful'
        else:
            print path
    elif command[0] == 'a':
        filename = getFilename()
        text = getText()
        
        (system,path) = directoryservice.lookup(filename)
        
        if not system == None:
            filesystem = Pyro4.Proxy(pname+system)
            filesystem.appendFile(path,text)
            print 'Text appended to file'
        else: print path
    """
