from flask import Flask, jsonify
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
@app.route('/')
def hello():
	return "hell world"

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)


