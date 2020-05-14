from flask import Flask, jsonify, g
import os

from resources.users import users
from resources.posts import posts
from flask_login import LoginManager, current_user
import models
import commonwords
from flask_cors import CORS
DEBUG=True
PORT=8000

app= Flask(__name__)

app.secret_key="a secret"
login_manager= LoginManager()
login_manager.init_app(app) 

@login_manager.user_loader
def load_user(user_id):
	try:
		user = models.User.get_by_id(user_id)
		return user
	except models.DoesNotExist:
		return None
@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
		data={'error':'user is not logged in'},
		message="you must be logged in to do this",
		status=401), 401

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(posts, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(posts, url_prefix='/api/v1/posts')

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():
  """Connect to the db before each request"""
  # store the database as a global var in g
  print("you should see this before each request") # optional -- to illustrate that this code rus before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
  g.db = models.DATABASE
  g.db.connect()


@app.after_request # use this decorator to cause a function to run after reqs
def after_request(response):
  """Close the db connetion after each request"""
  print("you should see this after each request") # optional -- to illustrate that this code runs after each request
  g.db.close()
  return response # go ahead and send response back to client 

@app.route('/')
def hello():
	return "hell world"

if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

# you should already have these lines at the bottom of your app
# this is how the app is run when you type "python app.py" on your terminal
# running a .py file from the terminal causes __name__ to be set to __main__
# inside that application
if __name__ == '__main__': 
  models.initialize() 
  app.run(debug=DEBUG, port=PORT)


