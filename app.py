from flask import Flask, g
import models
from resources.users import users_api
from resources.posts import posts_api

# import requests

from flask_cors import CORS
from flask_login import LoginManager
login_manager = LoginManager()

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(posts_api, origins=["http://localhost:3000"], supports_credentials=True)
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(posts_api, url_prefix='/wine')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def hello():
    return 'hi'

# @app.route('/wines')
# def wines():
#     r = requests.get('https://api.globalwinescore.com/globalwinescores/latest/?wine_id=')
#     r.headers{
#         'content-type': 'application/json',
#         'Authorization':'Token 911c4473076f96f384b74008df0dff9596bc829c'
#     }
#     return r.json()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)