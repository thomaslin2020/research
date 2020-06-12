import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_qrcode import QRcode
from flask_sqlalchemy import SQLAlchemy
from server.config import config
from server.models import *

config_name = os.environ.get('FLASK_ENV') or 'default'

app = Flask(__name__)
app.config.from_object(config[config_name])
config[config_name].init_app(app)
CORS(app, resources={r'/*': {'origins': '*'}})

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)
mongo = SQLAlchemy(app)
qrcode = QRcode(app)


@app.route('/')
def hello():
    return 'Hello world'


if __name__ == '__main__':
    app.run()
