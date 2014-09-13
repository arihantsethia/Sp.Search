# Main File : This has to be run to start the server
from __future__ import with_statement
from flask import Flask, _app_ctx_stack
from views import views
from queryhandler import queryparser
import uuid

# Defining the application by creating an instance of Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
query_parser = None 

# Blueprints : Setting the blueprints for handling various routes 
app.register_blueprint(views)
#Initaialzes the database from the database schema give in 'schema.sql'
def init_query_parser():
	with app.app_context():
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

def get_query_parser():
	return query_parser;

if __name__ == '__main__':
	init_query_parser()
	app.run(host='0.0.0.0',debug=True)
	

