import os

from flask import Flask, current_app
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)

CORS(app)

auth = HTTPTokenAuth('Token')

@auth.verify_token
def verify_token(token):
    return token == os.getenv('SECRET_KEY')


@app.route("/")
@auth.login_required
def main_route():
    return 'Version v3.0.0'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8001)
