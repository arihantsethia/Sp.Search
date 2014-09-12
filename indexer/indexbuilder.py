from collections import defaultdict
import shelve, gc

class IndexBuilder:
	def __init__ (self):
		self.index = defaultdict(lambda:defaultdict(list))
		gc.disable()
		return

	def buildIndex(self, fileId, wordList):
		print len(self.index)
		for pos in xrange(0,len(wordList)):
			self.index[wordList[pos]][fileId].append(pos)
		return

	def writeIndex(self, fileLocation):
		fileDictionary = shelve.open(fileLocation)
		for key,value in self.index.iteritems():
			fileDictionary[key.encode('utf-8')] = value
		fileDictionary.close()

	def deleteIndex(self):
		del self.index
		gc.collect()

	def getIndex(self):
		return self.index