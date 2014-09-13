#!/usr/bin/python
import os, chardet, urllib, string
from indexer import indexbuilder, htmlparser, indexmerger
from queryhandler import queryparser
import cProfile
import pstats

query_parser = None 
def set_query_parser():

	global query_parser
	root_dir = '/home/simrat/Documents/IRProject/Sp.Search/'

	index_dir = root_dir + 'indices/'
	indices = []
	indices.append(index_dir+'finalIndexWithoutStopWordsWithStemming')
	indices.append(index_dir+'indexWithStopWordsAndWithStemming')
	indices.append(index_dir+'indexWithoutStopWordsAndWithoutStemming')
	indices.append(index_dir+'indexWithStopWordsAndWithoutStemming')
	error_dir = root_dir + 'errors/'
	errorLogFile =error_dir + 'error.log'
	stop_words_file = root_dir+"indexer/stopWords.txt"
	k = 2.00
	b = 0.75

	query_parser = queryparser.QueryParser(indices,stop_words_file, k, b)
	
def get_query_parser():
	global query_parser
	return query_parser;


if __name__ == '__main__':
	set_query_parser()
	queries = ["woman", "computer science", "boring job", "\"prime minister\"", 
					"sex", "novel", "final - result", "apple + banana", "man", "error"]
	#s = raw_input("enter query: ")
	#m = int(raw_input("enter mode: "))
	for q in queries:
		print q
		cProfile.run('r=query_parser.get_rank(q, 1, False, True)', 'restats')
		p = pstats.Stats('restats')
		p.sort_stats('cumulative').print_stats(20)
		print q
		cProfile.run('r=query_parser.get_rank(q, 2, False, True)', 'restats')
		p = pstats.Stats('restats')
		p.sort_stats('cumulative').print_stats(20)
		print q
		cProfile.run('r=query_parser.get_rank(q, 3, False, True)', 'restats')
		p = pstats.Stats('restats')
		p.sort_stats('cumulative').print_stats(20)

	
	#for i in xrange(0, min(10, len(rank))):
		#print rank[i]
