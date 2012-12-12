# saved as client.py
import Pyro4

def fileInteract(path, fs):
    cmd = ['']
    index = 0
    print 'interact mode'
    while not quit(cmd[0]): 
        cmd = raw_input().lower().split()
        if len(cmd) == 0: cmd = '\n'

        if cmd[0] == 'r':
            print fs.readFile(path),
        elif cmd[0] == '\n':
            line = fs.readLine(path, index)
            if line == -1:
                print 'EOF'
                index = 0;
            else:
                print line
                index+=1

def quit(opt):
    return opt == 'quit' or opt == 'q'
    
    
# BEGIN PROGRAM #    
    
tokens = []         # Tokens representing filepath
sys = ''            # Which system to connect to
cmd = ['']          # User command

pname = 'PYRONAME:filesystem.'                          # Prefix of every filesystem registry address
dirserv = Pyro4.Proxy('PYRONAME:directoryservice')      # Connect to directory service
lockserv = Pyro4.Proxy('PYRONAME:lockservice')          # Connect to lock service

print 'HELLO, THIS IS CLIENT\n'

#TODO: Read line by line in a loop, insert into different parts, handle failure
while not quit(cmd[0]):
    #path = '/'.join(tokens)
    cmd = raw_input('/'.join(['home']+tokens)+': ').lower().split()
    
    # View contents of current directory
    if cmd[0] == 'ls':
        print '\t'.join(dirserv.show(tokens))
        
    # Change directory
    elif cmd[0] == 'cd' and len(cmd) > 1:
        if cmd[1] == '..':
            del tokens[len(tokens)-1]
            if len(tokens) == 0:
                sys = ''
        elif dirserv.exists(cmd[1],tokens):
            tokens += [cmd[1]]
            if len(tokens) == 1:
                sys = dirserv.navigate(tokens).system
                filesystem = Pyro4.Proxy(pname+sys)
        else:
            print "Directory doesn't exist"
    
    # Open file in interactive mode        
    elif cmd[0] == 'open' or cmd[0] == 'o' and len(cmd) > 1:
        path = '/'.join(tokens +[cmd[1]])
        if sys == '':
            print 'Must first choose a filesystem'
        elif lockserv.requestLock(path):
            print path
            fileInteract(path, filesystem)
            lockserv.releaseLock(path)
        else:
            print 'File locked by another user'
    
    # Read contents of file
    elif cmd[0] == 'read' or cmd[0] == 'r' and len(cmd) > 1:
        if sys == '':
            print 'Must first choose a filesystem'
        else:
            print filesystem.readFile('/'.join(tokens +[cmd[1]])) 
  
    # View help
    elif cmd[0] == 'help' or cmd[0] == 'h':
        print 'I HAVE NO IDEA WHAT I\'M DOING'
    
    # Command not recognised    
    elif not quit(cmd[0]):
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
