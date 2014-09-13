#!/usr/bin/python
import os, chardet, urllib, string
from indexer import indexbuilder, htmlparser, indexmerger
from queryhandler import queryparser

query_parser = None 
def set_query_parser():
	root_dir = '/home/rh/git/Sp.Search/'
	index_dir = root_dir + 'indices/'
	indices = []
	indices.append(index_dir+'indexWithoutStopWordsAndWithStemming')
	indices.append(index_dir+'indexWithStopWordsAndWithStemming')
	indices.append(index_dir+'indexWithoutStopWordsAndWithoutStemming')
	indices.append(index_dir+'indexWithStopWordsAndWithoutStemming')
	error_dir = root_dir + 'errors/'
	errorLogFile =error_dir + 'error.log'
	stop_words_file = root_dir+"indexer/stopWords.txt"
	k = 2.00
	b = 0.75
	query_parser = queryparser.QueryParser(indices,stop_words_file, k, b)
