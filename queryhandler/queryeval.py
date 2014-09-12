import re, shelve, math
from operator import itemgetter
from sets import Set
from nltk import PorterStemmer

porter = PorterStemmer()

class QueryEvaluator:
	def __init__ (self, stop_words_file, total_number_of_documents, average_length, k, b):
		self.get_stopwords(stop_words_file)
		self.total_number_of_documents = total_number_of_documents
		self.average_length = average_length
		self.k = k
		self.b = b
		self.length_data = None;

	def load_indices(self, indicesFileList):
		for indexFile in indicesFileList:
			self.indices.append(shelve.open(indexFile))

	def get_terms(self, query_terms, include_stop_words, include_stemming):
		html_string = query_terms.lower()
		html_string = re.sub(r'[^a-z0-9 ]',' ',html_string)
		html_string = html_string.split()
		if(not self.contains_stop_words) :
			html_string = [x for x in html_string if x not in self.stop_words]
		html_string = [ self.porter.stem(word) for word in html_string]
		return html_string

	def load_query_items (self, query_terms, include_stop_words, include_stemming):
		query_terms = [porter.stem(word) for word in terms]
		full_index = shelve.open("Data/indices/107")
		for term in terms:
			if full_index.has_key(term):
				self.index[term] = full_index[term]
		return

	def get_stopwords(self, stop_words_file):
		'''get stopwords from the stopwords file'''
		f=open(stop_words_file, 'r')
		stopWords=[line.rstrip() for line in f]
		self.stopWords=dict.fromkeys(stopWords)
		f.close()

	def get_ranking(self, score):
		rank = sorted(score.items(), key=lambda x:x[1], reverse=True)
		print rank
		return rank


	def get_tfidf_score(self, term):
		score={}
		if self.index.has_key(term):
			postlist = self.index[term]
			numberOfDocuments = len(postlist)
			if numberOfDocuments==0:
				idf=0
			else:
				idf = math.log(self.total_number_of_documents/numberOfDocuments)
			for document in postlist:
				freq = len(postlist[document])
				score[document] = freq*idf
		return score


	def get_tf_score(self, term):
		score={}
		if self.index.has_key(term):
			postlist = self.index[term]
			for document in postlist:
				score[document] = len(postlist[document])
		return score

	def get_bm25_score(self, term):
		score ={}
		if self.index.has_key(term):
			postlist=self.index[term]
			numberOfDocuments = len(postlist)
			if numberOfDocuments==0:
				idf = 0
			else:
				idf = math.log((self.total_number_of_documents - numberOfDocuments + 0.5)/(numberOfDocuments+0.5), 2)
			for document in postlist:
				if self.length_data.has_key(str(document)):
					doclen = self.length_data[str(document)]
				else:
					doclen = self.average_length
				tf = len(postlist[document])
				bm25score = idf*(tf*(self.k+1)/(tf + self.k*(1-self.b+ self.b*(doclen/self.average_length))))
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
				for pos in self.index[ph[0]][document]:
					flag = True
					last = pos
					for x in xrange(1, len(ph)):
						if self.index.has_key(ph[x]):
							if  (last+1) in self.index[ph[x]][document]:
								last = last + 1
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
		if numberOfDocuments==0:
			idf=0
		else:
			idf = math.log(self.total_number_of_documents/numberOfDocuments)
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
							break
					if flag:
						count += 1
				if count>0:
					score[document] = count
		return score

	def get_bm25score_phrase(self, phrase):
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
		if numberOfDocuments==0:
			idf = 0
		else:
			idf = math.log((self.total_number_of_documents - numberOfDocuments + 0.5)/(numberOfDocuments+0.5), 2)
		for document in tf:
			if self.length_data.has_key(str(document)):
				doclen = self.length_data[str(document)]
			else:
				doclen = self.average_length
			bm25score = idf*(tf[document]*(self.k+1)/(tf[document] + self.k*(1-self.b+ self.b*(doclen/self.average_length))))
			if bm25score<0:
				bm25score=0
			score[document] = bm25score
		return score

# query = 'air +line -look +pool +prop -lop cool "ok gu what"'
if __name__ == "__main__":
	query = raw_input("enter query ")
	print get_tfscore_phrase(query)