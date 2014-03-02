#!/usr/bin/python

import re, json

class ExtractOutput:

    def __init__(self):
        self.file_name = "movies-films-keylargo.asp"
        self.keywords = ['Claim:', 'Status:', 'Origins:', 'Sources:']

    def run_main(self):
        data = {}
        pattern = re.compile('[\W_]+')

        for line in json.loads(open(self.file_name).read()):

            for key in self.keywords:
                line = line.split(key)
                if len(line) >1:
                    temp = line[0]
                    temp = pattern.sub(" ", temp)
                    data.setdefault(key, []).append(temp)
                    line = " ".join(line[1:])
                else:
                    line = " ".join(line) 

        open("output-file", "w").write(json.dumps(data))    


if __name__ == "__main__":
    eo_obj = ExtractOutput()
    eo_obj.run_main()
