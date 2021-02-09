from flask import Flask
from flask_pymongo import PyMongo
from main_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = PyMongo(app).db

from main_app.routes import main

app.register_blueprint(main)