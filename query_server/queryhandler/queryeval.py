import re, shelve, math
import os
from operator import itemgetter
from nltk import PorterStemmer
import cPickle as pickle

porter = PorterStemmer()

class QueryEvaluator:
	def __init__ (self, stop_words_file, k, b):
		self.total_number_of_documents = 1500000
		self.average_length = 334
		self.k = k
		self.b = b
		self.length_data = None;

	def load_indices(self, indices_file_list):
		self.indices = []
		for indexFile in indices_file_list:
			self.indices.append(shelve.open(indexFile))

	def load_query_items (self, query_terms, include_stop_words, include_stemming):
		self.index = dict()
		pos = 0
		if include_stemming and (not include_stop_words):
			pos = 0
		elif include_stemming and include_stop_words:
			pos = 1
		elif (not include_stemming) and (not include_stop_words):
			pos = 2
		elif (not include_stemming) and include_stop_words:
			pos = 3
		for term in query_terms:
			if self.indices[pos].has_key(term.encode('utf-8')):
				self.index[term.encode('utf-8')] = self.indices[pos][term.encode('utf-8')]
		return

	def load_length_data(self):	
		self.length_data=pickle.load(open(os.path.join(os.path.dirname(__file__), "length.pickle"), "rb"))
		return

	def get_ranking(self, score):
		rank = sorted(score.items(), key=lambda x:x[1], reverse=True)
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

	def get_tfidf_score_phrase(self, phrase):
		tf={}
		score = {}
		ph = phrase.split()
		if len(ph)==0:
			return score
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

	def get_tf_score_phrase(self, phrase):
		score = {}
		ph = phrase.split()
		if len(ph)==0:
			return score
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
					score[document] = count
		return score

	def get_bm25_score_phrase(self, phrase):
		score = {}
		tf={}
		ph = phrase.split()
		if len(ph)==0:
			return score
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