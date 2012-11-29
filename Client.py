# saved as client.py
import Pyro4

def getFilename(): return raw_input("Filename: ").strip()
def getText(): return raw_input("Text: ")

def action():
    option = 1
    pname = "PYRONAME:filesystem."
    directoryservice = Pyro4.Proxy("PYRONAME:directoryservice")

    while not option == "q":
        option = raw_input("> ").strip().lower()
        
        if option == "r":
            filename = getFilename()        # Get name of file from user
            
            # Get system name and path on that system from
            # the directory service
            (system,path) = directoryservice.lookup(filename)
            filesystem = Pyro4.Proxy(pname+system)              # Access file system
            result = filesystem.readFile(path)                  # Read file from server
            print "Read successful"
            print result
        elif option == "n":
            filename = getFilename()
            text = getText()
            
            (system,path) = directoryservice.lookup(filename)
            filesystem = Pyro4.Proxy(pname+system)
            filesystem.writeFile(path,text)
            print "Creation successful"
        elif option == "a":
            filename = getFilename()
            text = getText()
            
            (system,path) = directoryservice.lookup(filename)
            filesystem = Pyro4.Proxy(pname+system)
            filesystem.appendFile(path,text)
            print "Text appended to file"
        print " "

print "HELLO, THIS IS CLIENT\n"
action()
