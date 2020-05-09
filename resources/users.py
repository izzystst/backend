import models

from flask import Blueprint, request, jsonify
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
				message="registerd user",
				status=201), 201





