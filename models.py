import datetime

from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('wine.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=100)
    # cellar = []

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
            raise Exception("User with that username already exists")

class Post(Model):
    posted_by = CharField()
    name = CharField()
    vintage = CharField(max_length=4)
    review = CharField()
    # created_by = ForeignKeyField(User, related_name='post_set')
    
    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()


