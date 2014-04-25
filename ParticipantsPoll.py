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
      
        for aFile in allFiles:
            if aFile.endswith("py") or aFile.startswith("voting"):
                continue
            aFileOpList = []
            with open(aFile) as aFilefd:
                for line in aFilefd.readlines():
                    line = line and line.strip()
                    aFileOpList.append(int(line))
            self.allFilesResultsMap[aFile] = aFileOpList
            aFilefd.close()
 
    def doVoting(self):
        self.cumVotingList = [0] * self.test_instances_count        

        for aFileList in self.allFilesResultsMap.values():
            self.cumVotingList = [x+y for x,y in zip(self.cumVotingList, aFileList)]
 
    def announceResults(self):
        votingCountFd = open('votingCount', 'w')
        with open(self.resultsFile, 'w') as resultsFd:
            for line in self.cumVotingList:
                if line > 0:
                    verdict = 1
                elif line <=0:
                    verdict = -1
                resultsFd.write("%s\n" % verdict)
                votingCountFd.write("%s\n" % line)
        votingCountFd.close()

if __name__ == "__main__":
    pp = ParticipantsPoll()
    pp.main()
