from os import listdir

class ParticipantsPoll:

    def __init__(self):
        self.allFilesResultsMap = {}
        self.test_instances_count = 952
        self.resultsFile = "votingResult"

    def main(self):
        self.loadAllInput()
        self.doVoting()
        self.announceResults()        

    def loadAllInput(self):
        allFiles = listdir('.')
      
        try: 
            for aFile in allFiles:
                if aFile.endswith("py"):continue
                aFileOpList = []
                with open(aFile) as aFilefd:
                    for line in aFilefd:
                        line = line and line.strip()
                        aFileOpList.append(int(line))
                self.allFilesResultsMap[aFile] = aFileOpList
        except:
            print "Exception during loading votes"
 
    def doVoting(self):
        self.cumVotingList = [0] * self.test_instances_count        

        for aFileList in self.allFilesResultsMap.values():
            self.cumVotingList = [x+y for x,y in zip(self.cumVotingList, aFileList)]
        
    def announceResults(self):
        with open(self.resultsFile, 'w') as resultsFd:
            for line in self.cumVotingList:
                if line > 0:
                    verdict = 1
                elif line <=0:
                    verdict = -1
                resultsFd.write("%s\n" % verdict)

if __name__ == "__main__":
    pp = ParticipantsPoll()
    pp.main()
