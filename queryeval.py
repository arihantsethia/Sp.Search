from operator import itemgetter
import re, shelve, math
from sets import Set
#from nltk import PorterStemmer
#from nltk.corpus import stopwords

index = shelve.open("Data/indices/107")
totalNumberOfDocuments = 1500000 #Change it once we get the actual value 
averageLength = 334
k=2.0
b=0.75

# def ranktfidf (query):
# 	rval = []
# 	words = query;
# 	tfScore = []
# 	tfIdfScore = []
# 	for word in words:
# 		if index.has_key(word):
# 			postlist = index[word]
# 			numberOfDocuments = len(postlist)
# 			for document in postlist:
# 				length = len(postlist[document])
# 				tfScore.append( (length , document) )
# 				tfIdfScore.append( ( (length * (math.log(totalNumberOfDocuments/numberOfDocuments))), document))

# 	tfScore.sort(reverse=True)
# 	tfIdfScore.sort(reverse=True)
# 	return (tfScore, tfIdfScore)

def get_tfidfscore(term):
	score={}
	if index.has_key(term):
		postlist = index[term]
		numberOfDocuments = len(postlist)
		idf = math.log(totalNumberOfDocuments/numberOfDocuments)
		for document in postlist:
			freq = len(postlist[document])
			score[document] = freq*idf
	return score

def get_tfidfscore_phrase(phrase):
	tf={}
	score = {}
	ph = phrase.split()
	if index.has_key(ph[0]):
		postlist = index[ph[0]]
		for document in postlist:
			count = 0
			
			#print type(document)
			for pos in index[ph[0]][document]:
				flag = True
				last = pos
				for x in xrange(1, len(ph)):
					
					if index.has_key(ph[x]):
						
						if  (last+1) in index[ph[x]][document]:
							last = last + 1
							#print "sda"
							
						else:
							flag = False
							break
					else:
						flag = False
						break		
				if flag:
					count += 1
			if count>0:
				tf[document] = count
				
	numberOfDocuments = len(tf)
	idf = math.log(totalNumberOfDocuments/numberOfDocuments)
	for document in tf:
		score[document] = tf[document]*idf
	
	return score







def get_tfscore_phrase(phrase):
	score = {}
	ph = phrase.split()
	if index.has_key(ph[0]):
		postlist = index[ph[0]]
		for document in postlist:
			count = 0
			
			#print type(document)
			for pos in index[ph[0]][document]:
				flag = True
				last = pos
				for x in xrange(1, len(ph)):
					
					if index.has_key(ph[x]):
						
						if  (last+1) in index[ph[x]][document]:
							last = last + 1
							#print "sda"
							
						else:
							flag = False
							break
					else:
						flag = False
						break		
				if flag:
					count += 1
			if count>0:
				score[document] = count
	return score

def get_bm25score_phrase(phrase):
	lendata = shelve.open('Data/length')
	score = {}
	tf={}
	ph = phrase.split()
	if index.has_key(ph[0]):
		postlist = index[ph[0]]
		
		for document in postlist:
			count = 0
			
			
			
			#print type(document)
			for pos in index[ph[0]][document]:
				flag = True
				last = pos
				for x in xrange(1, len(ph)):
					
					if index.has_key(ph[x]):
						
						if  (last+1) in index[ph[x]][document]:
							last = last + 1
							#print "sda"
							
						else:
							flag = False
							break
					else:
						flag = False
						break		
				if flag:
					count += 1
			if count>0:
				tf[document] = count
		
	numberOfDocuments = len(tf)
	idf = math.log((totalNumberOfDocuments - numberOfDocuments + 0.5)/(numberOfDocuments+0.5), 2)
	for document in tf:
		if lendata.has_key(str(document)):
			doclen = lendata[str(document)]
		else:
			doclen = averageLength
		bm25score = idf*(tf[document]*(k+1)/(tf[document] + k*(1-b+ b*(doclen/averageLength))))
		if bm25score<0:
			bm25score=0
		score[document] = bm25score
	return score
		




def get_tfscore(term):
	score={}
	if index.has_key(term):
		postlist = index[term]
		for document in postlist:
			score[document] = len(postlist[document])
	return score

def get_bm25score(term):
	lendata = shelve.open('Data/length')
	score ={}
	if index.has_key(term):
		postlist=index[term]
		numberOfDocuments = len(postlist)
		idf = math.log((totalNumberOfDocuments - numberOfDocuments + 0.5)/(numberOfDocuments+0.5), 2)
		for document in postlist:
			if lendata.has_key(str(document)):
				doclen = lendata[str(document)]
			else:
				doclen = averageLength
			tf = len(postlist[document])
			bm25score = idf*(tf*(k+1)/(tf + k*(1-b+ b*(doclen/averageLength))))
			if bm25score<0:
				bm25score = 0
			score[document] = bm25score
			
	return score
			
		


def getRanking(score):
	rank = sorted(score.items(), key=lambda x:x[1], reverse=True)
	#score.sort(reverse=True)
	print rank
	return rank



# def rankBM25(query, docs): #query is the query which is a list of terms, docs is the list of documents
# 	scoreBM25=[]
# 	for d in documents:
# 		score = getBM25score(q, d)
# 		scoreBM25.append((d, score))
# 	return sorted(scoreBM25, key=itemgetter(1))

# def getBM25score(query, d):
# 	totscore = 0
# 	for term in query:
# 		k = 2.0
# 		b = 0.75
# 		plist = getPostingList(term)
# 		#df = getDocFreq(term)
# 		df = len(plist)
# 		idf = math.log((TotalDocs - df + 0.5)/(df+0.5) , 2)
# 		#tf = getTermFreq(term, d)
# 		tf = len(plist[d])
# 		dlen = getDocLen(d)

# 		score = idf*(tf*(k+1)/(tf + k(1-b+ b*(dlen/AvgDLen))))
# 		if(score<0):
# 			score = 0
# 		totscore += score

# 	return totscore

# def search(s):
# 	phrases = re.findall('"(.*?)"',s)
# 	s=re.sub('("(.*?)")*','',s)
# 	notwords = re.findall ('(?:[-])(\S+)',s)
# 	pluswords = re.findall('(?:[+])(\S+)',s)
# 	othwords = re.findall ('(?:^|\s)(?![-|+])(\S+)',s)

# 	print notwords, pluswords, othwords,phrases
	
# 	#make set of docs to be excluded to facilitate O(1) lookup
# 	notdocs = Set([])
# 	for word in notwords:
# 		if index.has_key(word):
# 			for item in index[word]:
# 				notdocs.add(item)
	
	

	
# query = 'air +line -look +pool +prop -lop cool "ok gu what"'
if __name__ == "__main__":
	query = raw_input("enter query ")
	print get_tfscore_phrase(query)
