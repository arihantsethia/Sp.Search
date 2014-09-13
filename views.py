# Views.py : Handles the views of general modules
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
import smtplib
#Defining the Blueprint for views.py
views = Blueprint('views',__name__)

@views.route('/')
def index():
	return render_template("index.html")

@views.route('/search', methods=['GET'])
def search():
	query_string = request.args.get('query', '')
	stemming = True if request.args.get('stemming','Y') == 'Y' else False
	stopWords = True if request.args.get('stopWords','N') == 'Y' else False
	
	#log query,stemming, stopwords
	return render_template("search_results.html")

@views.route('/search_results',)
def search_results():

	query_string = request.args.get('query', '')
	stemming = True if request.args.get('stemming','Y') == 'Y' else False
	stopWords = True if request.args.get('stopWords','N') == 'Y' else False
	
	scoring_method = request.args.get('scoringMethod','tf')
	start_rank = request.args.get('start_rank',0)
	num_results = request.args.get('num_results',10)
	query_id = request.args.get('query_id',None)

	if query_id is None:
		#generete new id and do whole search
		query_id = 1
		return 

	# #log query,stemming, stopwords
	# return render_template("search_results.html", result)

@views.route('/about')
def about():
	return render_template("about.html")
