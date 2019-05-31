# import json

# from flask import jsonify, Blueprint, abort, make_response
# from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)

# wine_fields = {
#     "wine": fields.String,
#     "color": fields.String,
# }

# class WineList(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument(
#             'wine',
#             required=False,
#             help='wine name not available',
#             location=['form', 'json']
#         )
#         self.reqparse.add_argument(
#             'color',
#             required=False,
#             help="no color available",
#             location=['form', 'json']
#         )
#         super().__init__()

#     def get(self):
#         wines = [marshal(wine, wine_fields)
#         return wines


# wine_api = Blueprint('resources.wine', __name__)
# api = Api(wine_api)
# api.add_resource(
#     WineList,
#     '/winelist',
#     endpoint='winelist'
# )