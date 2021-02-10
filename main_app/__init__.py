from flask import Flask
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from main_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

db = PyMongo(app).db

from main_app.routes import main

app.register_blueprint(main)