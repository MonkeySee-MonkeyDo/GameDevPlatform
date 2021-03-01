from flask import session
from datetime import timedelta
from main_app import app

@app.before_first_request
def before_first_request():
    app.permanent_session_lifetime = timedelta(minutes=30)
    if not "logged_in" in session:
        session["logged_in"] = False