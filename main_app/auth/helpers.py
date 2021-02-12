from flask import redirect, url_for, flash, session
from markdown import markdown
import bcrypt
import functools

############################################################
# HELPER FUNCTIONS
############################################################

# CHECK LOGGED IN
def logged_in():
    if not "user_id" in session:
        flash("You must be logged in to do this.")
        return False
    return True

# CHECK NOT LOGGED IN
def logged_out():
    if "user_id" in session:
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
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)

def verify_hash(plain, hashed):
    return bcrypt.checkpw(plain, hashed)

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