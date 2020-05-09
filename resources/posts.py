import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

from flask_login import LoginManager, current_user
posts = Blueprint('posts', 'posts')

@posts.route('/', methods=["GET"])
def test():
	return "posts resource"

@posts.route('/', methods=["POST"])
def create_post():
	payload = request.get_json()
	print('this is the payload')
	print(payload)
	new_post = models.Post.create(text=payload['text'], image=payload['image'],Latitude=payload['Latitude'], Longitude=payload["Longitude"], user=current_user.id)
	print(new_post)
	post_dict = model_to_dict(new_post)

	return jsonify(
		data=post_dict,
		message="succesfully created a post",
		status=200), 200

