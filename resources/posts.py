import json
from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)
import models

post_fields = {
    'id': fields.Integer,
    'posted_by': fields.Integer,
    'img': fields.String,
    'wine': fields.String,
    'vintage': fields.Integer,
    'comment': fields.String,
    'user': fields.String,
    'created_at': fields.DateTime
}

user_fields = {
    'username': fields.String,
    'id': fields.Integer
}

class PostList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'posted_by',
            required=False,
            help='username is required to post',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'img',
            required=False,
            help="No image provided",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'wine',
            required=False,
            help='Name of wine is required',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'vintage',
            required=False,
            help='No vintage year was provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'comment',
            required=False,
            help='No review/comment',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'user',
            required=False,
            help='No user provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        posts = [marshal(post, post_fields) for post in models.Post.select()]
        return posts

    def post(self):
        args = self.reqparse.parse_args()
        post = models.Post.create(**args)
        
        return make_response(
            json.dumps({
                'post': marshal(post, post_fields),
                'message': 'successfully posted'
            }), 200)


class Post(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'wine',
            required=False,
            help='Name of wine is required',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'vintage',
            required=False,
            help='No vintage year was provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'comment',
            required=False,
            help='No review/comment',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(post_fields)
    def get(self, id):
        try:
            post = (models.Post.get(models.Post.id==id), 200)
        except models.Post.DoesNotExist:
            abort(404)
        else:
            return post

    @marshal_with(post_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Post.update(**args).where(models.Post.id==id)
        query.execute()
        return (models.Post.get(models.Post.id==id), 200)

    def delete(self, id):
        query = models.Post.delete().where(models.Post.id==id)
        query.execute()
        return 'Post has been deleted'

class UserPostList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'posted_by',
            required=False,
            help='username is required to post',
            location=['form', 'json']
        )
        super().__init__()
    # @marshal_with(post_fields)
    def get(self, id):
        posts = [marshal(post, post_fields) for post in models.Post.select().where(models.Post.posted_by==id)]
        return posts

        # try:
        #     user = (models.User.get(models.User.id==id), 200)
        #     posts = [marshal(post, post_fields) for post in models.Post.select().where(models.Post.posted_by==user.username)]
        # except models.Post.DoesNotExist:
        #     abort(404)
        # else:
        #     return posts


posts_api = Blueprint('resources.posts', __name__)
api = Api(posts_api)
api.add_resource(
    PostList,
    '/posts',
    endpoint='posts'
)
api.add_resource(
    Post,
    '/posts/<int:id>',
    endpoint='post'
)
api.add_resource(
    UserPostList,
    '/userposts/<int:id>',
    endpoint='userposts'
)