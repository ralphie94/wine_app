from flask import Flask

DEBUG = True
PORT = 8000

app = Flask(__name__)

@app.before_request

@app.route('/')
def index():
    return 'hi'

if __name__ == 'main':
    app.run(debug=DEBUG, port=PORT)