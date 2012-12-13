class CurrentDirectory(object):
    
    def __init__(self,n,p):
        self.path = p           # Path to current directory
        self.name = n           # Name of current directory
        self.curries = []       # Subdirectory structures
        self.dirs = []          # Names of subdirectories
        self.files = []         # Filenames
    
    def addFile(self, f):
        self.files.append(f)
        
    def addDir(self, d):
        self.dirs.append(d.name)    # Just the names of the subdirectories
        print d.name
        self.curries.append(d)      # Recursive subdirectory structures
        
    def toString(self):
        result = self.name + '{\n\t' + str(self.files) 
        for curry in self.curries:
            result += '\n\t' + curry.toString()
        return result + '\n}'
