from flask import Flask, g
import models
from resources.users import users_api

DEBUG = True
PORT = 8000

app = Flask(__name__)
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