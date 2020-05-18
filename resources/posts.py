import models
import nltk
import pprint
import datetime
pp = pprint.PrettyPrinter(indent=4)

from nltk.tokenize import word_tokenize, PunktSentenceTokenizer, sent_tokenize
from nltk.probability import FreqDist

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from peewee import *

from flask import Blueprint, request, jsonify, flash
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
		message="Congrats, you did your post for today!",
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
	delete_query = models.Post.get_by_id(id)
	delete_query.delete_instance()
	return jsonify(
		data={},
		message="deleted",
		status=200),200

@posts.route("/common", methods=["GET"])
def common_words():
	all_text = []
	for post in models.Post.select():
		all_text.append(post.text)
	print("these are all posts")
	# print(all_text)
	# creating a string of all the text
	listToStr = ' '.join([str(elem) for elem in all_text]) 
	# print("this is th list now string")
	# print(listToStr)

	# adding some more words to the to stop words
	stop_words = stopwords.words('english')
	# all_stopwords = stopwords.words('english')
	stop_words.extend(['today', 'tommorrow', 'was', 'wa'])
	print("these are the stop words")
	pp.pprint(stopwords)
	# this will tokenize and remove punctuation
	tokenizer = nltk.RegexpTokenizer(r"\w+")
	nopunc = tokenizer.tokenize(listToStr)
	# setting the stop words
	ps = PorterStemmer()
	stemwords = []
	# this is stemming all the words
	for w in nopunc:
		stemwords.append(ps.stem(w))
	# removing the stopwords from the list of total words
	stemwords = [stemword for stemword in stemwords if stemword not in stop_words]
	print("this is after stopwords")
	print(stemwords)
	# freqnescy of words 
	fdist = FreqDist(stemwords)

	most_common_words = []
	for word, frequency in fdist.most_common(5):
		most_common_words.append(word)
		print(u'{};{}'.format(word, frequency))

	# print("these are the common wordds")
	# print(most_common_words)
	text_posts = []

	for word in most_common_words:
		# print(word)
		texts = models.Post.select().where(models.Post.text.contains(word))
		text_dict = [model_to_dict(text) for text in texts]
		# print('this is the word')
		# print(word)
		# pp.pprint(text_dict)
		text_posts.append(text_dict)
	# pp.pprint(text_posts)

	return jsonify(
		data={"posts": text_posts, 'words': most_common_words},
		message="common words queries",
		status=200), 200

@posts.route("/today", methods=["GET"])
def todays_posts():
	# today = datetime.date.today()
	today = datetime.date.today() 
	# print(date.today())
	# tomoorow =datetime.date.today() + datetime.timedelta(days=1)
	print(current_user)
	# (models.Post.date == today)
# models.Post.date == today
# models.Post.user ==current_user
	todays = models.Post.select().where(models.Post.user == current_user.id).where(models.Post.date == today).exists()
	print(todays)
	# todayss = models.Post.select().where(models.Post.user == current_user.id & models.Post.date == today)
	# todays_dict = [model_to_dict(today) for today in todayss]
	# print(todays_dict)
	# print(todays_dict)
	return jsonify(
		data=todays,
		message="posts from today exist",
		status=200),200
		
@posts.route('/search/<query>', methods=["GET"])
def search(query):
	print(query)
	print("you are calling the search")
	all_text = []
	for post in models.Post.select().where(models.Post.text.contains(query)):
		all_text.append(post.text)
	# .where(models.Post.text).contains(query)
	# stringy the posts
	listToStr = ' '.join([str(elem) for elem in all_text]) 

	# posts_dict = [model_to_dict(post) for post in posts]
	print(all_text)
	print(";ength of all all_text")
	print(len(all_text))
	print("len of string")
	print(listToStr)
	print("this is the list to string, sent tokenize")
	list_final_query= []
	sentences = sent_tokenize(listToStr)
	print("this is the sentance")
	print(sentences)
	# if query in sentances:
	# 	print(sentances)
	# 	list_final_query.append(sent)
	# if any(query in s for s in sentances)
	list_final_querys = [sentence for sentence in sentences if query in sentence]
	print("this is the lst with the qury ")
	print(list_final_querys)
	# list_final_query_dict = [model_to_dict(list_final_query) for list_final_query in list_final_querys]
	# print("this is the dict")
	# print(list_final_query_dict)
	# list_dict = model_to_dict(list_final_querys)
	# print("\n \n \n \n this is the list dict")
	# print(list_dict)
	query_list={}
	query_list[query]=list_final_querys
	print(query_list)

	return jsonify(
		data=query_list,
		message=f"these are the sentance that contain the query {query}",
		status=200
		), 200

@posts.route("/<id>", methods=['PUT'])
def update_date(id):
	payload = request.get_json()
	post_to_update = models.Post.get_by_id(id)
	if 'date' in payload:
		post_to_update.date= payload['date']
	post_to_update.save()
	updated_post_dict= model_to_dict(post_to_update)
	return jsonify(
		data=updated_post_dict,
		message="updated dog",
		status=200

		), 200


