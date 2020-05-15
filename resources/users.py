import models

from flask import Blueprint, request, jsonify, flash
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

users = Blueprint('users', 'users')

@users.route('/', methods=["GET"])
def test():
	return "user resourse hello"

@users.route('/register', methods=['POST'])
def register():
	payload=request.get_json()
	print(payload)

	payload['email']=payload['email'].lower()
	payload['username'] = payload['email'].lower()

	try:
		models.User.get(models.User.email == payload['email'])
		return jsonify(
			data={},
			message="That email is already in our system",
			status=401
			), 401
	except models.DoesNotExist:

		try:
			models.User.get(models.User.username == payload['username'])
			return jsonify(
				data={},
				message="That username isn't available",
				status=401), 401
		except models.DoesNotExist:

			pw_hash = generate_password_hash(payload['password'])
			created_user = models.User.create(
				username=payload['username'],
				email=payload['email'],
				password=pw_hash,
				zipcode=payload['zipcode'],
				DOB=payload['DOB']
			)
			login_user(created_user)
			created_user_dict = model_to_dict(created_user)
			created_user_dict.pop('password')

			return jsonify(
				data=created_user_dict,
				message="congrats, you are now registered! Let's make your first post!",
				status=201), 201

@users.route('/login', methods=["POST"])
def login():
	payload= request.get_json()
	payload['email']=payload['email'].lower()
	payload['username']=payload['email'].lower()

	try:
		user = models.User.get(models.User.email==payload['email'])
		user_dict = model_to_dict(user)

		checked_password = check_password_hash(user_dict['password'], payload['password'])
		if(checked_password):
			login_user(user)
			print(f'{current_user.username} is current_user.username in POST login')
			user_dict.pop('password')

			return jsonify(
				data=user_dict,
				message=f"Congrats, you are now logged in as {user_dict['email']}",
				status=200
				),200
		else:
			# bad password
			return jsonify(
				data={},
				message="email or password is wrong",
				status=401), 401

	except models.DoesNotExist:
		# wrong username 
		return jsonify(
			data={},
			message="email or password is wrong",
			status=401), 401
@users.route("/logout", methods=['GET'])
def logout():
	logout_user()
	return jsonify(
		data={},
		message="logged out! See you tommorrow!",
		status=200), 200

@users.route('<id>', methods=["DELETE"])
def delete_user(id):
	delete_query = models.User.delete().where(models.User.id == id)
	num_rows_deleted = delete_query.execute()
	return jsonify(
		data={},
		message="Sorry to see you go! We have deleted your account.",
		status=200), 200

