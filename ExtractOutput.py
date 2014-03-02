#!/usr/bin/python

import re, json, os

class ExtractOutput:

    def __init__(self):
        self.keywords = ['Claim:', 'Status:', 'Origins:', 'Sources:']
        self.pattern = re.compile('[\W_]+')

    def run_main(self):

        #files = os.listdir(os.curdir)
        files = ['movies-films-goldfinger.asp']
        for fileName in files:
            data = {}
           
            try:

                if (fileName.endswith(".py")):
                    continue

                key_index  = []
                for line in json.loads(open(fileName).read()):
                    for key in self.keywords:
                        key_index.append((key, line.find(key)))
                self.splitData(key_index, data, line)  
                open(fileName+"_new", "w").write(json.dumps(data))  
  
            except:
                print "Exception for fileName - %s" % (fileName)

    def splitData(self, key_index, data, line):
        
        cur_key = None
        cur_index = None

        for key, index in key_index:
            if index == -1:continue
            if not cur_key:
                cur_key = key
                cur_index = index
                continue

            data[cur_key] = self.dataClean(line[cur_index:index])
            cur_key = key
            cur_index = index
        data[cur_key] = self.dataClean(line[cur_index:])


    def dataClean(self, line):
            
        line = self.pattern.sub(" ", line).split(" ")
        return " ".join(line[1:])

if __name__ == "__main__":
    eo_obj = ExtractOutput()
    eo_obj.run_main()
