import models
import nltk

from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from nltk.probability import FreqDist

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from peewee import *

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

from flask_login import LoginManager, current_user

posts = Blueprint('posts', 'posts')

# @posts.route('/', methods=["GET"])
# def test():
# 	return "posts resource"

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

@posts.route('/', methods=["GET"])
def posts_index():
	posts = models.Post.select()
	print(posts)
	posts_dict = [model_to_dict(post) for post in posts]

	return jsonify(
		data=posts_dict,
		message="found all of the posts",
		status=200), 200

# post show route 
@posts.route('/<id>', methods=["GET"])
def posts_show(id):
	post = models.Post.get_by_id(id)
	post_dict = model_to_dict(post)

	return jsonify(
		data=post_dict,
		message=f"found session with id {id}",
		status=200
		), 200

@posts.route('/random', methods=["GET"])
def random_post():
	randoms = models.Post.select().order_by(fn.Random()).limit(1)
	print(randoms)
	random_dict = [model_to_dict(random) for random in randoms]
	print(random_dict)

	return jsonify(
		data=random_dict,
		message=f"found a random post",
		status=200
		), 200
@posts.route('/user/<id>', methods=["GET"])
def users_posts(id):
	users_posts= models.Post.select().where(models.Post.user == id)
	users_posts_dict = [model_to_dict(users_post) for users_post in users_posts]
	print(users_posts_dict)
	return jsonify(
		data=users_posts_dict,
		message=f"found all posts by user {id}",
		status=200), 200
	# need  / map / texts / image 
# this is just for testing purposes
@posts.route('/<id>', methods=["DELETE"])
def delete_post(id):
	delete_query = models.Post.select().where(models.Post.id == id)

@posts.route("/common", methods=["GET"])
def common_words():
	all_text = []
	for post in models.Post.select():
		all_text.append(post.text)
	print("these are all posts")
	print(all_text)
	listToStr = ' '.join([str(elem) for elem in all_text]) 
	print("this is th list now string")
	print(listToStr)
	# sample_text = state_union.raw("2006-GWBush.txt")
	tokenizer = nltk.RegexpTokenizer(r"\w+")
	nopunc = tokenizer.tokenize(listToStr)
	print("this is without punct")
	print(nopunc)
	# print(nopunc)
	# fdist = FreqDist()
	# for word in word_tokenize(sentance):
	stop_words = set(stopwords.words('english'))
	ps = PorterStemmer()

	# words = word_tokenize(nopunc)
	# print(words)
	stemwords = []
	for w in nopunc:
		stemwords.append(ps.stem(w))

	# print(stemwords)
	stemwords = [stemword for stemword in stemwords if stemword not in stop_words]
	print(stemwords)
	fdist = FreqDist(stemwords)

	most_common_words = []
	for word, frequency in fdist.most_common(5):
		most_common_words.append(word)
		print(u'{};{}'.format(word, frequency))

	print("these are the common wordds")
	print(most_common_words)
	# posts_dict = [model_to_dict(post) for post in posts]
	# print(posts_dict)
	# # print('this is the posts dict')
	# # print(posts_dict)
	# tokenizer = nltk.RegexpTokenizer(r"\w+")
	# nopunc = tokenizer.tokenize(posts_dict)
	# print(nopunc)

	return jsonify(
		data={"all text": all_text, "common_words": most_common_words},
		message="found all the text in posts",
		status=200), 200
