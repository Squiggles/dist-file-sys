# saved as client.py
import Pyro4
import time

#TODO:  Caching?
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
            if line == None:
                print 'EOF'
                index = 0;
            else:
                print line
                index+=1

def cacheInsert(path,cache,fs):
    f = fs.readFile(path)
    if f == None:
        print "File doesn't exist"
    else:
        if len(cache) > 2:
            lru = ('',('',time.time()))
            for pair in cache.items():
                if pair[1][1] < lru[1][1]:
                    lru = pair
            del cache[lru[0]]
        cache[path] = fs.readFile(path),time.time()

def quit(opt):
    return opt == 'quit' or opt == 'q'
    
    
# BEGIN PROGRAM #    
    
tokens = []         # Tokens representing filepath
sys = ''            # Which system to connect to
cmd = ['']          # User command
cache = {}          # Mapping from path to a tuple of contents and timestamp

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
            if len(tokens) == 0:
                print 'Can\'t go higher than root directory'
            else:
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
    elif (cmd[0] == 'open' or cmd[0] == 'o') and len(cmd) > 1:
        path = '/'.join(tokens +[cmd[1]])
        if sys == '':
            print 'Must first choose a filesystem'
        elif lockserv.requestLock(path):
            fileInteract(path, filesystem)
            lockserv.releaseLock(path)
        else:
            print 'File locked by another user'
    
    # Read contents of file
    elif (cmd[0] == 'read' or cmd[0] == 'r') and len(cmd) > 1:
        path = '/'.join(tokens +[cmd[1]])
        if sys == '':
            print 'Must first choose a filesystem'
        elif path not in cache or cache[path][1] < dirserv.timeAccessed(path):
            cacheInsert(path, cache, filesystem)
        if path in cache:
            print cache[path][0]
    
    elif (cmd[0] == 'w' or cmd[0] == 'write') and len(cmd) > 1:
        path = '/'.join(tokens +[cmd[1]])
        if sys == '':
            print 'Must first choose a filesystem'
        elif lockserv.requestLock(path):
            text = raw_input()
            filesystem.writeFile(path,text)
            if path in cache:
                del cache[path]
            dirserv.timeUpdate(path)
            dirserv.refresh()
            print 'Write successful'
            lockserv.releaseLock(path)
        else:
            print 'File locked by another user'
    
    elif (cmd[0] == 'a' or cmd[0] == 'append') and len(cmd) > 1:
        path = '/'.join(tokens +[cmd[1]])
        if sys == '':
            print 'Must first choose a filesystem'
        elif lockserv.requestLock(path):
            text = raw_input()
            filesystem.appendFile(path,text)
            if path in cache:
                del cache[path]
            dirserv.timeUpdate(path)
            print 'Append successful'
            lockserv.releaseLock(path)
        else:
            print 'File locked by another user'
    
    # View help
    elif cmd[0] == 'help' or cmd[0] == 'h':
        print 'I HAVE NO IDEA WHAT I\'M DOING'
    
    # Debug info
    elif cmd[0] == 'd':
        for c in cache.items():
            print c
    
    # Command not recognised    
    elif not quit(cmd[0]):
        print 'Command not recognised, type h or help for assistance'
