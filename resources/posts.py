import models

from flask import Blueprint, request, jsonify

posts = Blueprint('posts', 'posts')

@posts.route('/', methods=["GET"])
def test():
	return "posts resource"