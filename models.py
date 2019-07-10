import os
from playhouse.db_url import connect

import datetime
from flask import jsonify, make_response
import json
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = connect(os.environ.get('DATABASE_URL'))
# DATABASE = SqliteDatabase('wine.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password, **kwargs):
        username = username.lower()
        try:
           cls.select().where(
                (cls.username==username)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception("Username already exists")
             

class Post(Model):
    posted_by = CharField()
    user = CharField()
    img = CharField()
    wine = CharField()
    vintage = CharField()
    comment = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    # created_by = ForeignKeyField(User, related_name='post_set')
    
    class Meta:
        database = DATABASE
    
 

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()


