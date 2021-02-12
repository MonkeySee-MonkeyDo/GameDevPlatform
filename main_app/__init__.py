from flask import Flask, session
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from main_app.config import Config
from main_app.main.helpers import doc_from_id
import os

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

db = PyMongo(app).db

from main_app.main.routes import main
app.register_blueprint(main)

from main_app.auth.routes import auth
app.register_blueprint(auth)

from main_app.forum.routes import forum
app.register_blueprint(forum)

from main_app.processors import *