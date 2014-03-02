#!/usr/bin/python

import re, json, os

class ExtractOutput:

    def __init__(self):
        self.keywords = ['Claim:', 'Status:', 'Origins:', 'Sources:']

    def run_main(self):
        data = {}
        pattern = re.compile('[\W_]+')

        for fileName in os.listdir(os.curdir):
  
            try:
                if (fileName.endswith(".py")):
                    continue
                for line in json.loads(open(fileName).read()):

                    for key in self.keywords:
                        line = line.split(key)
                        if len(line) >1:
                            temp = line[0]
                            temp = pattern.sub(" ", temp)
                            data.setdefault(key, []).append(temp)
                            line = " ".join(line[1:])
                        else:
                            line = " ".join(line) 

                open(fileName+"_new", "w").write(json.dumps(data))  
  
            except:
                print "Exception for fileName - %s" % (fileName)



if __name__ == "__main__":
    eo_obj = ExtractOutput()
    eo_obj.run_main()
