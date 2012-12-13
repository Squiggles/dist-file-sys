import Pyro4

# Checks configuration file for servers and reports this to directory service
# and file system manager
class Coordinator(object):
    def __init__(self):
        handle = open('config.txt', 'r')
        contents = handle.read()
        handle.close()
        self.systems = filter(removeEmpty,contents.split('\n'))
        
    def getSystems(self):
        print 'System list request'
        return self.systems

#function to asist filtering out empty values from a list
def removeEmpty(x):
    return not x == ''
        
# Register coordinator
coo = Coordinator()
daemon = Pyro4.Daemon()                     # make Pyro daemon
ns = Pyro4.locateNS()                       # find name server
uri = daemon.register(coo)                  # register coordinator
ns.register('coordinator', uri)             # register with name in name server

message = 'Available systems: '
for s in coo.systems:
    message += s + ' '
print message
print 'Ready'
daemon.requestLoop()                        # wait

