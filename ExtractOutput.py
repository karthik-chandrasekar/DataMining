#!/usr/bin/python

import re, json, os

class ExtractOutput:

    def __init__(self):
        self.keywords = ['Claim:', 'Status:', 'Origins:', 'Sources:', 'Last updated:']
        self.pattern = re.compile('[\W_]+')

    def run_main(self):

        #files = os.listdir(os.curdir)
        files = ['movies-actors-barrymore.asp']
        for fileName in files:
            data = {}
           
            try:
                if (fileName.endswith(".py")):
                    continue

                key_index  = []
                for line in json.loads(open(fileName).read()):
                    line = self.remLastUpdated(line)
                    for key in self.keywords:
                        key_index.append((key, line.find(key)))
                self.splitData(key_index, data, line) 

                final_string = "\n".join(data.values()) 
                open(fileName+"_new", "w").write(final_string)  
            except:
                print "Exception for fileName - %s" % (fileName)


    def remLastUpdated(self, line):
        lup_index = line.find('Last updated:')
        sources_index = line.find('Sources:')
        source_line = " "
        if lup_index != -1:
            if sources_index != -1:
                source_line = line[sources_index:]
            line = line[:lup_index] + source_line
        return line

    def splitData(self, key_index, data, line):
        
        cur_key = None
        cur_index = None

        for key, index in key_index:
            if index == -1:continue
            if not cur_key:
                cur_key = key
                cur_index = index
                continue

            data[cur_key] = self.dataClean(line[cur_index:index], cur_key)
            cur_key = key
            cur_index = index
        data[cur_key] = self.dataClean(line[cur_index:], cur_key)

    def dataClean(self, line, key):
            
        key = self.pattern.sub("", key)
        line = self.pattern.sub(" ", line).split(" ")
        return "@@@"+"begin"+key+"@@@"+" ".join(line[1:])+"@@@"+"end"+key+"@@@"

if __name__ == "__main__":
    eo_obj = ExtractOutput()
    eo_obj.run_main()
