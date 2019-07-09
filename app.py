import os
import json
from flask import Flask, g, flash, request, redirect, url_for, session, make_response
import models
from werkzeug.utils import secure_filename
from resources.users import users_api
from resources.posts import posts_api



from flask_cors import CORS, cross_origin
from flask_login import LoginManager
login_manager = LoginManager()

import config

MYDIR = os.path.dirname(__file__)
UPLOAD_FOLDER = "static/imgs"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

CORS(users_api, origins=["http://localhost:3000", "https://winepost.herokuapp.com"], supports_credentials=True)
CORS(posts_api, origins=["http://localhost:3000", "https://winepost.herokuapp.com"], supports_credentials=True)
CORS(app, origins=["http://localhost:3000", "https://winepost.herokuapp.com"], supports_credentials=True)

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

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(MYDIR + '/' + app.config['UPLOAD_FOLDER'])
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination = '/'.join([target, filename])
    file.save(destination)
    session['uploadFilePath'] = destination
    return make_response(
    json.dumps({
        'destination': os.path.join('/' + app.config['UPLOAD_FOLDER'] + '/' + filename),
        'message': 'successfully saved image'
    }), 200)


if 'ON_HEROKU' in os.environ:
    models.initialize()


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)