from flask import Flask, jsonify
from resources.users import users
from flask_login import LoginManager, current_user
import models
DEBUG=True
PORT=8000

app= Flask(__name__)

app.secret_key="a secret"
login_manager= LoginManager()
login_manager.init_app(app) 

app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/')
def hello():
	return "hell world"

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)


