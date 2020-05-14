import models
import nltk
import pprint
import datetime
pp = pprint.PrettyPrinter(indent=4)

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
	print("this is the current_user")
	print(current_user)
	print("this is todays datetime.datetime.today")
	print(datetime.date.today())
	today = datetime.date.today()
	# print(date.today())
	# (models.Post.date == today)
	# models.Post.user == current_user
	posts = models.Post.select().where(models.Post.user == current_user.id).where(models.Post.date == today)
	print(posts)


	finddict = [model_to_dict(post) for post in posts]
	print("this is the finddcit")
	print(finddict)
	# print(finddict)
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
	users_posts= models.Post.select().where(models.Post.user == id).order_by(models.Post.date.desc())
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
	# creating a string of all the text
	listToStr = ' '.join([str(elem) for elem in all_text]) 
	print("this is th list now string")
	print(listToStr)
	# this will tokenize and remove punctuation
	tokenizer = nltk.RegexpTokenizer(r"\w+")
	nopunc = tokenizer.tokenize(listToStr)
	# setting the stop words
	stop_words = set(stopwords.words('english'))
	ps = PorterStemmer()
	stemwords = []
	# this is stemming all the words
	for w in nopunc:
		stemwords.append(ps.stem(w))
	# removing the stopwords from the list of total words
	stemwords = [stemword for stemword in stemwords if stemword not in stop_words]
	# print(stemwords)
	# freqnescy of words 
	fdist = FreqDist(stemwords)

	most_common_words = []
	for word, frequency in fdist.most_common(5):
		most_common_words.append(word)
		print(u'{};{}'.format(word, frequency))

	print("these are the common wordds")
	print(most_common_words)
	text_posts = []

	for word in most_common_words:
		# print(word)
		texts = models.Post.select().where(models.Post.text.contains(word))
		text_dict = [model_to_dict(text) for text in texts]
		# print('this is the word')
		# print(word)
		# pp.pprint(text_dict)
		text_posts.append(text_dict)
	pp.pprint(text_posts)

	return jsonify(
		data={"posts": text_posts, 'words': most_common_words},
		message="common words queries",
		status=200), 200

@posts.route("/today", methods=["GET"])
def todays_posts():
	today = datetime.date.today()
	# print(date.today())
	print(current_user)
	# (models.Post.date == today)
# models.Post.date == today
# models.Post.user ==current_user
	todays = models.Post.select().where(models.Post.date == today) 
	todays_dict = [model_to_dict(today) for today in todays]
	print(todays_dict)

	return jsonify(
		data=todays_dict,
		message="these are the posts from today",
		status=200),200
		


