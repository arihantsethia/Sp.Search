# Views.py : Handles the views of general modules
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash, _app_ctx_stack,Blueprint, current_app
import smtplib, uuid, json

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
	return render_template("search_results.html")

@views.route('/about')
def about():
	return render_template("about.html")
