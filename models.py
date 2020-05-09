from peewee import *
import datetime
from flask_login import UserMixin , current_user
from playhouse.db_url import connect

DATABASE = SqliteDatabase('capstone.sqlite',
	pragmas={'foreign_keys': 1})



class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField(unique=True)
	zipcode=CharField()
	DOB=DateField()
	created=DateField(default=datetime.date.today)

	class Meta:
		database = DATABASE


class Post(Model):
	date=DateTimeField(default=datetime.datetime.now)
	text=TextField()
	Latitude=CharField()
	Longitude=CharField()
	image= CharField()
	user=ForeignKeyField(User, backref='Post', on_delete='CASCADE')

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Post], safe=True)
	print("connected to db and ceated tables")

	DATABASE.close()