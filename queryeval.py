from operator import itemgetter
import re, shelve, math
from sets import Set
from nltk import PorterStemmer

index = shelve.open("dataset/finalIndex")

def get_tfscore_phrase(phrase):
	score = {}
	ph = phrase.split()
	if index.has_key(ph[0]):
		postlist = index[ph[0]]
		for document in postlist:
			count = 0
			for pos in index[ph[0]][document]:
				flag = True
				last = pos
				for x in xrange(1, len(ph)):
					if index.has_key(ph[x]):
						if  (last+1) in index[ph[x]][document]:
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

def get_tfscore(term):
	score={}
	if index.has_key(term):
		postlist = index[term]
		for document in postlist:
			score[document] = len(postlist[document])
	return score

def getRanking(score):
	rank = sorted(score.items(), key=lambda x:x[1], reverse=True)
	return rank

# query = 'air +line -look +pool +prop -lop cool "ok gu what"'
if __name__ == "__main__":
	query = raw_input("enter query ")
	print len(get_tfscore(query))
