from operator import itemgetter
import re, shelve, math
from sets import Set
from nltk import PorterStemmer
from nltk.corpus import stopwords

porter = PorterStemmer()

class Query:
	def __init__ (self, stopWordsFile, totalNumberOfDocuments, averageLength, k, b):
		self.getStopwords(stopWordsFile)
		self.totalNumberOfDocuments = totalNumberOfDocuments
		self.averageLength = averageLength
		self.k = k
		self.b = 0.75

	def loadIndices(self, indicesFileList):
		for indexFile in indicesFileList:
			self.indices.append(shelve.open(indexFile))

	def loadQueryItems (self, terms):
		self.index={}
		terms = [porter.stem(word) for word in terms]
		full_index = shelve.open("Data/indices/107")
		for term in terms:
			if full_index.has_key(term):
				self.index[term] = full_index[term]
		return

    def getStopwords(self, stopWordsFile):
        '''get stopwords from the stopwords file'''
        f=open(stopWordsFile, 'r')
        stopWords=[line.rstrip() for line in f]
        self.stopWords=dict.fromkeys(stopWords)
        f.close()

	def getRanking(self, score):
		rank = sorted(score.items(), key=lambda x:x[1], reverse=True)
		#score.sort(reverse=True)
		print rank
		return rank


	def get_tfidfscore(self, term):
		score={}
		if self.index.has_key(term):
			postlist = self.index[term]
			numberOfDocuments = len(postlist)
			if numberOfDocuments==0:
				idf=0
			else:
				idf = math.log(self.totalNumberOfDocuments/numberOfDocuments)
			for document in postlist:
				freq = len(postlist[document])
				score[document] = freq*idf
		return score


	def get_tfscore(self, term):
		score={}
		if self.index.has_key(term):
			postlist = self.index[term]
			for document in postlist:
				score[document] = len(postlist[document])
		return score

	def get_bm25score(self, term):
		lendata = shelve.open('Data/length')
		score ={}
		if self.index.has_key(term):
			postlist=self.index[term]
			numberOfDocuments = len(postlist)
			if numberOfDocuments==0:
				idf = 0
			else:
				idf = math.log((self.totalNumberOfDocuments - numberOfDocuments + 0.5)/(numberOfDocuments+0.5), 2)
			for document in postlist:
				if lendata.has_key(str(document)):
					doclen = lendata[str(document)]
				else:
					doclen = self.averageLength
				tf = len(postlist[document])
				bm25score = idf*(tf*(self.k+1)/(tf + self.k*(1-self.b+ self.b*(doclen/self.averageLength))))
				if bm25score<0:
					bm25score = 0
				score[document] = bm25score
		return score

	def get_tfidfscore_phrase(self, phrase):
		tf={}
		score = {}
		ph = phrase.split()
		if self.index.has_key(ph[0]):
			postlist = self.index[ph[0]]
			for document in postlist:
				count = 0
				#print type(document)
				for pos in self.index[ph[0]][document]:
					flag = True
					last = pos
					for x in xrange(1, len(ph)):
						if self.index.has_key(ph[x]):
							if  (last+1) in self.index[ph[x]][document]:
								last = last + 1
								#print "sda"
							else:
								flag = False
								break
						else:
							flag = False
							break					if flag:
						count += 1
				if count>0:
					tf[document] = count
		numberOfDocuments = len(tf)
		if numberOfDocuments==0:
			idf=0
		else:
			idf = math.log(self.totalNumberOfDocuments/numberOfDocuments)
		for document in tf:
			score[document] = tf[document]*idf
		return score

	def get_tfscore_phrase(self, phrase):
		score = {}
		ph = phrase.split()
		if self.index.has_key(ph[0]):
			postlist = self.index[ph[0]]
			for document in postlist:
				count = 0
				#print type(document)
				for pos in self.index[ph[0]][document]:
					flag = True
					last = pos
					for x in xrange(1, len(ph)):
						if self.index.has_key(ph[x]):
							if  (last+1) in self.index[ph[x]][document]:
								last = last + 1
								#print "sda"
							else:
								flag = False
								break
						else:
							flag = False
							break					if flag:
						count += 1
				if count>0:
					score[document] = count
		return score

	def get_bm25score_phrase(self, phrase):
		lendata = shelve.open('Data/length')
		score = {}
		tf={}
		ph = phrase.split()
		if self.index.has_key(ph[0]):
			postlist = self.index[ph[0]]
			for document in postlist:
				count = 0
				#print type(document)
				for pos in self.index[ph[0]][document]:
					flag = True
					last = pos
					for x in xrange(1, len(ph)):
						if self.index.has_key(ph[x]):
							if  (last+1) in self.index[ph[x]][document]:
								last = last + 1
								#print "sda"
							else:
								flag = False
								break
						else:
							flag = False
							break					if flag:
						count += 1
				if count>0:
					tf[document] = count
		numberOfDocuments = len(tf)
		if numberOfDocuments==0:
			idf = 0
		else:
			idf = math.log((self.totalNumberOfDocuments - numberOfDocuments + 0.5)/(numberOfDocuments+0.5), 2)
		for document in tf:
			if lendata.has_key(str(document)):
				doclen = lendata[str(document)]
			else:
				doclen = self.averageLength
			bm25score = idf*(tf[document]*(self.k+1)/(tf[document] + self.k*(1-self.b+ self.b*(doclen/self.averageLength))))
			if bm25score<0:
				bm25score=0
			score[document] = bm25score
		return score

# query = 'air +line -look +pool +prop -lop cool "ok gu what"'
if __name__ == "__main__":
	query = raw_input("enter query ")
	print get_tfscore_phrase(query)
