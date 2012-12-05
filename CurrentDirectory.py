class CurrentDirectory(object):
    
    def __init__(self,n,p):
        self.path = p
        self.name = n
        self.curries = []
        self.dirs = []
        self.files = []
        self.toplevel = False
    
    def addFile(self, f):
        self.files.append(f)
        
    def addDir(self, d):
        self.dirs.append(d.name)
        print d.name
        self.curries.append(d)
        
    def toString(self):
        result = self.name + '{\n\t' + str(self.files) 
        for curry in self.curries:
            result += '\n\t' + curry.toString()
        return result + '\n}'
