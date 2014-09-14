# Main File : This has to be run to start the server
from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint, current_app
import smtplib, uuid, json
from queryhandler import queryparser
import cache, json_utils
import logging

# Defining the application by creating an instance of Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

query_parser = None

def init_query_parser():
	global query_parser
	print "i am shot"
	root_dir = '/home/arihant/Github/Sp.Search/'
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

@app.route('/search', methods=['GET'])
def search():
	callback = request.args.get('callback', '')
	query_string = request.args.get('query', '')
	stemming = True if request.args.get('stemming','Y') == 'Y' else False
	stop_words = True if request.args.get('stop_words','N') == 'Y' else False
	scoring_method = request.args.get('scoring_method','tf')
	start_rank = request.args.get('start_rank',0)
	num_results = request.args.get('num_results',10)
	query_id = request.args.get('query_id',None)
	if (query_id is None) or (not cache.is_cached(query_id)):
		query_id = str(uuid.uuid4())
		rank_list = query_parser.get_rank(query_string, scoring_method, stemming, stop_words)
		results_length = len(rank_list)
		cache.cache_result(query_id, rank_list)
		processing_time = 0.06
		cache.cache_result_stats(query_id, results_length, processing_time)
		rank_list = rank_list[start_rank: start_rank+num_results]
	else :
		rank_list = cache.get_cached(query_id, start_rank, num_results)
		stats = cached.get_cached_stats(query_id)
		results_length = stats['results_length']
		processing_time = stats['processing_time']
	results = json_utils.generate_json(query_id, rank_list, query_string, scoring_method, processing_time, results_length, start_rank)
	print results
	if(callback ==  ''):
		return results
	else:
		return callback+'(' + results +')'

@app.route('/log', methods=['GET'])
def log():
	query_id = request.args.get('query_id', '')
	redirect_url = request.args.get('redirect_url', '')
	rank = request.args.get('rank', '')
	return redirect(redirect_url);

if __name__ == '__main__':
	init_query_parser()
	handler = logging.FileHandler('query_results.log')
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	app.logger.addHandler(handler)
	app.run(host='0.0.0.0', port=1234, debug=True)