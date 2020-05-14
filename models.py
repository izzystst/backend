import os
from peewee import *
import datetime
from flask_login import UserMixin , current_user
from playhouse.db_url import connect
if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
            
else:
	DATABASE = SqliteDatabase('capstone.sqlite',
		pragmas={'foreign_keys': 1})



class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField(unique=True)
	zipcode=CharField()
	DOB=DateField()
	# lastPost=DateField()
	created=DateField(default=datetime.date.today)

	class Meta:
		database = DATABASE


class Post(Model):
	date=DateTimeField(default=datetime.datetime.now)
	text=TextField()
	Latitude=CharField()
	Longitude=CharField()
	image= TextField()
	user=ForeignKeyField(User, backref='Post', on_delete='CASCADE')

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Post], safe=True)
	print("connected to db and ceated tables")

	DATABASE.close()