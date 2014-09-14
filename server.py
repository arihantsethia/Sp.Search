# Main File : This has to be run to start the server
from __future__ import with_statement
from flask import Flask, _app_ctx_stack, g
from views import views

# Defining the application by creating an instance of Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Blueprints : Setting the blueprints for handling various routes 
app.register_blueprint(views)

if __name__ == '__main__':
	#init_query_parser()
	app.run(host='0.0.0.0',debug=True)
