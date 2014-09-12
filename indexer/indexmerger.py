from collections import defaultdict
from itertools import chain
import shelve, os

class IndexMerger:
	def __init__ (self, merge_dir):
		self.merge_dir = merge_dir
		return

	def merge(self, file1, file2, result):
		merged_index = shelve.open(result)
		index1 = shelve.open(file1)
		index2 = shelve.open(file2)

		for key in index1:
			if(index2.has_key(key)):
				posting_list = index1[key]
				posting_list.update(index2[key].items())
				merged_index[key] = posting_list
			else:
				merged_index[key] = index1[key]

		for key in index2:
			if(not index1.has_key(key)):
				merged_index[key] = index2[key]

		merged_index.close()
		index1.close()
		index2.close()

	def merge_all(self):
		currDir = self.merge_dir+"/"
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
