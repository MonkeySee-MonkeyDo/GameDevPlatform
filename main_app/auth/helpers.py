from flask import redirect, url_for, flash, session
from markdown import markdown
import bcrypt
import functools

############################################################
# HELPER FUNCTIONS
############################################################

# CHECK LOGGED IN
def logged_in():
    if not session["logged_in"]:
        flash("You must be logged in to do this.")
        return False
    return True

# CHECK NOT LOGGED IN
def logged_out():
    if session["logged_in"]:
        flash("You must be logged out to do this.")
        return False
    return True

# CHECK IF CORRECT USER IS LOGGED IN
def check_user(**kwargs):
    if not logged_in():
        return False
    if "user_id" in kwargs:
        if kwargs["user_id"] != session["user_id"]:
            flash("You must be logged in to the right account.")
            return False
        return True
    flash("Cannot verify user.")
    return False

def hash_password(password):
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)

def verify_hash(plain, hashed):
    plain = plain.encode("utf-8")
    return bcrypt.checkpw(plain, hashed)

def session_login(user_id, username):
    session["user_id"] = user_id
    session["username"] = username
    session["logged_in"] = True

def session_logout():
    session.pop("user_id")
    session.pop("username")
    session["logged_in"] = False

############################################################
# DECORATORS
############################################################

def login_flags(redirect_url="main.homepage", flags=[]):
    def wrapper(callback):
        @functools.wraps(callback)
        def wrapped(*args, **kwargs):
            if ("logged in" in flags and not logged_in()) \
                    or ("logged out" in flags and not logged_out()) \
                    or ("check user" in flags and not check_user(**kwargs)):
                return redirect(url_for(redirect_url))
            return callback(*args, **kwargs)
        return wrapped
    return wrapper