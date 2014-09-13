#!/usr/bin/python
import os, chardet, urllib, string
from indexer import indexbuilder, htmlparser, indexmerger
from queryhandler import queryparser

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
	#print indices
	query_parser = queryparser.QueryParser(indices,stop_words_file, k, b)
	
def get_query_parser():
	global query_parser
	return query_parser;


if __name__ == '__main__':
	set_query_parser()
	s = raw_input("enter query: ")
	m = int(raw_input("enter mode: "))
	rank = query_parser.get_rank(s, m, False, True)
	for i in xrange(0, min(10, len(rank))):
		print rank[i]