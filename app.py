from flask import Flask, g
import models
from resources.users import users_api

from flask_cors import CORS
from flask_login import LoginManager
login_manager - LoginManager()

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
app.register_blueprint(users_api, url_prefix='/users')

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

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)