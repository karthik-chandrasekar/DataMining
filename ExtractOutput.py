#!/usr/bin/python

import re, json, os

class ExtractOutput:

    def __init__(self):
        self.keywords = ['Claim:', 'Status:', 'Origins:', 'Sources:', 'Last updated:']
        self.pattern = re.compile('[\W_]+')

    def run_main(self):
        files = os.listdir(os.curdir)
        #files = ['movies-actors-barrymore.asp']
        for fileName in files:
            data = {}
            if (fileName.endswith(".py")):
                continue

            key_index  = []
            line = ""
            try:
                line  = json.loads(open(fileName).read())[0]
                     
                line = self.removeLastUpdated(line)
                for key in self.keywords:
                    key_index.append((key, line.find(key)))
                self.getData(key_index, data, line)
                if not 'Status:' in data and 'Claim:' in data: 
                    self.statusCheck(data)
                data = self.formatData(data) 
                final_string = "\n".join(data.values()) 
                open(fileName+"_new", "w").write(final_string)  

            except:
                print "Exception for %s" % (fileName)

    def removeLastUpdated(self, line):
        lup_index = line.find('Last updated:')
        sources_index = line.find('Sources:')
        source_line = " "
        if lup_index != -1:
            if sources_index != -1:
                source_line = line[sources_index:]
            line = line[:lup_index] + source_line
        return line

    def getData(self, key_index, data, line):
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
        
        if not cur_key or cur_index == -1:data= {};return
        data[cur_key] = self.dataClean(line[cur_index:])

    def dataClean(self, line):
        line = self.pattern.sub(" ", line).split(" ")
        return " ".join(line[1:])

    def statusCheck(self, data):
        claim = data.get('Claim:')    
        claim = claim and claim.strip()
        if not claim:return
        claim = claim.split(" ")
        status = claim[-1]
        if status.lower() in ('true', 'false'):
            data['Claim:'] = " ".join(claim[:-1])
        else:
            status = "Mixture"
        data['Status:'] = status.strip()

    def formatData(self, data):
        new_data = {}
        if not data:return
        for key, value in data.iteritems():
            if not value:continue
            if key == "Status:":
                value = self.cleanStatus(value)
                print value
            key = key.strip(":")
            final_string = "@@@begin"+key+"@@@"+value+"@@@end"+key+"@@@"
            new_data[key] = final_string
        return new_data

    def cleanStatus(self, value):
        if not value:return
        ex_index = value.find("Example") 
        if not ex_index == -1: 
            value =  value[:ex_index]
        if value.lower().strip() not in ('true', 'false', 'mixture'):
            value = 'Mixture'
        return value    


if __name__ == "__main__":
    eo_obj = ExtractOutput()
    eo_obj.run_main()
