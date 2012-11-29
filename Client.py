# saved as client.py
import Pyro4

def getFilename():
    return raw_input("What is the name of the file? ").strip().lower()
def getText():
    return raw_input("Enter text: ").strip().lower()

def action():
    option = 1

    while not option == "quit":
        filesystem = Pyro4.Proxy("PYRONAME:FileServer")
        option = raw_input("What do you want to do? ").strip().lower()
        
        if option == "read":
            filename = getFilename()
            temp =  filesystem.readFile(filename)
            print "Text read from file."
            print temp
        elif option == "create":
            filename = getFilename()
            text = get_text()
            filesystem.writeFile(filename,text)
            print "File created."
        elif option == "append":
            filename = getFilename()
            text = get_text()
            filesystem.appendFile(filename,text)
            print "Text appended to file."
        elif option == "greet":
            print filesystem.sayHello()
        print " "

print "HELLO, THIS IS CLIENT\n"
action()
