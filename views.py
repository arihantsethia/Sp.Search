# Views.py : Handles the views of general modules
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
import smtplib
import uuid
import json

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
	 	query_id = uuid.uuid4()
		 	
	data = {}
	data['scoringMethod']=scoring_method
	data['results']=[{},{}]
	
	data['results'][0]['url']='sadsad'
	data['results'][0]['title']=123
	data['results'][0]['rank']=1
	data['results'][0]['content']="sadsda"
	# data['results'][1]={}
	data['results'][1]['url']='sadad'
	data['results'][1]['title']=2313
	data['results'][1]['rank']=2
	data['results'][1]['content']="eqwe"
	data['query_id']=str(query_id)
	return json.dumps(data)

@views.route('/about')
def about():
	return render_template("about.html")
