# Main File : This has to be run to start the server
from __future__ import with_statement
from flask import Flask, _app_ctx_stack
from views import views

# Defining the application by creating an instance of Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Blueprints : Setting the blueprints for handling various routes 
app.register_blueprint(views)
#Initaialzes the database from the database schema give in 'schema.sql'
def init_db():
	with app.app_context():
		print "asd"

if __name__ == '__main__':
	#init_db()
	app.run(host='0.0.0.0')
	

