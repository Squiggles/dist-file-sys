# saved as client.py
import Pyro4

def action():
    option = raw_input("What do you want to do? ").strip().lower()
    
    if option == "read":
        filename = raw_input("What is the name of the file? ").strip()
        filesystem = Pyro4.Proxy("PYRONAME:FileSystem")
        print '\n' + filesystem.readFile(filename)
        
action()
