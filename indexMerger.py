from collections import defaultdict
from itertools import chain
import shelve, os

rootDir = '/home/arihant/Github/Sp.Search/dataset/'

class IndexMerger:
    def merge(self, file1, file2, result):
        mergedIndex = shelve.open(result)
        index1 = shelve.open(file1)
        index2 = shelve.open(file2)

        for key in index1:
            if(index2.has_key(key)):
                postingList = index1[key]
                postingList.update(index2[key].items())
                mergedIndex[key] = postingList
            else:
                mergedIndex[key] = index1[key]

        for key in index2:
            if(not index1.has_key(key)):
                mergedIndex[key] = index2[key]

        mergedIndex.close()
        index1.close()
        index2.close()

    def mergeMultiple(self,folderName):
        currDir = rootDir + folderName+"/"
        print currDir
        dirList=os.listdir(currDir)
        dirList.sort()
        counter = int(len(dirList)/2 ) * 2
        for i in xrange(0,counter,2):
            newIndexname = '%03s' % dirList[i] + '%03s'% dirList[i+1]
            print (currDir + str(dirList[i]), currDir+str(dirList[i+1]),currDir+newIndexname)
            self.merge(currDir + str(dirList[i]), currDir+str(dirList[i+1]),currDir+newIndexname)
            os.remove(currDir + str(dirList[i]))
            os.remove(currDir+str(dirList[i+1]))
            print(newIndexname, '%03d'%(i/2) )
            os.rename(currDir +newIndexname, currDir + '%03d'%(i/2))
            

indexMerger = IndexMerger()
indexMerger.mergeMultiple('merger')