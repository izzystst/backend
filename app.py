from flask import Flask, jsonify
from resources.users import users

DEBUG=True
PORT=8000

app= Flask(__name__)

@app.route('/')
def hello():
	return "hell world"
app.register_blueprint(users, url_prefix='/api/v1/users')

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)


