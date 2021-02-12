from flask import session
from main_app import app

@app.before_first_request
def before_first_request():
    if not "logged_in" in session:
        session["logged_in"] = False