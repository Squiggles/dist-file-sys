class CurrentDirectory(object):
    
    def __init__(self,p):
        self.path = p
        self.curries = []
        self.files = []
    
    def addFile(self, f):
        self.files.append(f)
        
    def addDir(self, d):
        self.curries.append(d)
        
    def toString(self):
        print self.path
        print self.files
        for curry in self.curries:
            curry.toString()
