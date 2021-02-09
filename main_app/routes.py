from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from markdown import markdown
from passlib.hash import pbkdf2_sha256
from main_app.forms import *
from main_app.models import *
from main_app import app, db
import functools
import os

main = Blueprint("main", __name__)

############################################################
# HELPER FUNCTIONS
############################################################

def logged_in():
    if not "user_id" in session:
        flash("You must be logged in to do this.")
        return False
    return True

def logged_out():
    if "user_id" in session:
        flash("You must be logged out to do this.")
        return False
    return True

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
    return pbkdf2_sha256.hash(password)

def verify_hash(a, b):
    return pbkdf2_sha256.verify(a, b)

def doc_from_id(collection, id):
    return collection.find_one({"_id": ObjectId(id)})

def rename_file(file, filename):
    file.filename = f"{filename}.{file.filename.split('.')[1]}"
    return file.filename

def save_file(file, filename, *folders):
    if file:
        filename = rename_file(file, filename)
        filename = secure_filename(filename)
        path = main.root_path
        for folder in folders:
            path = os.path.join(path, folder)
        file.save(os.path.join(path, filename))

############################################################
# DECORATORS
############################################################

def login_flags(redirect_url, *flags):
    def wrapper(callback):
        @functools.wraps(callback)
        def wrapped(*args, **kwargs):
            if "logged in" in flags:
                # CHECK LOGGED IN
                if not logged_in():
                    return redirect(url_for(redirect_url))
            if "logged out" in flags:
                # CHECK NOT LOGGED IN
                if not logged_out():
                    return redirect(url_for(redirect_url))
            if "check user" in flags:
                # CHECK IF CORRECT USER IS LOGGED IN
                if not check_user(**kwargs):
                    return redirect(url_for(redirect_url))
            return callback(*args, **kwargs)
        return wrapped
    return wrapper

############################################################
# ROUTES
############################################################

@main.route("/")
def homepage():
    """Homepage"""
    return render_template("index.html")

@main.route("/users")
@login_flags("main.homepage", "logged in")
def users():
    """Display users"""
    users_data = db.users.find()
    return render_template("users.html", users=users_data)

@main.route("/posts")
@login_flags("main.homepage", "logged in")
def posts():
    """Display posts"""
    posts_data = db.posts.find()
    return render_template("posts.html", posts=posts_data)

@main.route("/users/<user_id>")
@login_flags("main.homepage", "logged in")
def user(user_id):
    """Display user information"""
    user_data = doc_from_id(db.users, user_id)
    return render_template("user.html", user=user_data)

@main.route("/profiles/<user_id>")
@login_flags("main.homepage", "logged in")
def profile(user_id):
    """Display profile information"""
    profile_data = db.profiles.find_one({"user_id": user_id})
    return render_template("profile.html", profile=profile_data)

@main.route("/posts/<post_id>", methods=["GET", "POST"])
@login_flags("main.homepage", "logged in")
def post(post_id):
    """Display post information"""
    post_data = doc_from_id(db.posts, post_id)
    post_data["user"] = doc_from_id(db.users, post_data["user_id"])
    post_data["body"] = markdown(post_data["body"])
    users = db.users.find()
    replies = [reply for reply in db.replies.find({"post_id": post_id})]
    for reply in replies:
        reply["user"] = doc_from_id(db.users, reply["user_id"])
        reply["body"] = markdown(reply["body"])
    form = ReplyForm("New Reply", "Please fill out reply info:", users)
    if request.method == "POST":
        reply_variables = {
            "user_id": session["user_id"],
            "post_id": post_id,
            "body": request.form.get("body")
        }
        new_reply = blank_reply(**reply_variables)
        db.replies.insert_one(new_reply)
        flash("Reply created successfully")
        return redirect(url_for("main.post", post_id=post_id))
    return render_template("post.html", post=post_data, form=form, replies=replies)

@main.route("/create", methods=["GET", "POST"])
@login_flags("main.homepage", "logged out")
def create_user():
    """User creation"""
    form = UserForm("Create User", "Please fill out your info:")
    if request.method == "POST":
        new_user = blank_user(**request.form)
        new_user["password"] = hash_password(new_user["password"])
        if db.users.count_documents({ "username": request.form.get("username")}, limit=1):
            flash("Username already exists!")
            return redirect(url_for("main.create_user"))
        db.users.insert_one(new_user)
        new_user_id = db.users.find_one(new_user)["_id"]
        new_user_email = new_user["email"]
        new_profile = blank_profile(str(new_user_id), new_user_email)
        db.profiles.insert_one(new_profile)
        session["user_id"] = str(new_user_id)
        flash("User created successfully.")
        return redirect(url_for("main.user", user_id=new_user_id))
    return render_template("form.html", form=form)

@main.route("/create-post", methods=["GET", "POST"])
@login_flags("main.homepage", "logged in")
def create_post():
    """Post creation"""
    users = db.users.find()
    form = PostForm("Create Post", "Please fill out post info:", users)
    if request.method == "POST":
        new_post = blank_post(user_id=session["user_id"], **request.form)
        db.posts.insert_one(new_post)
        new_post_id = db.posts.find_one(new_post)["_id"]
        flash("Post created successfully.")
        return redirect(url_for("main.post", post_id=str(new_post_id)))
    return render_template("form.html", form=form)

@main.route("/edit-user/<user_id>", methods=["GET", "POST"])
@login_flags("main.homepage", "logged in", "check user")
def edit_user(user_id):
    user_data = doc_from_id(db.users, user_id)
    form = UserForm("Edit User", "Please edit your info:")
    form.set_values(user_data)
    if request.method == "POST":
        edited_user = blank_user(**request.form)
        edited_user["password"] = hash_password(edited_user["password"])
        db.users.update_one(user_data, {"$set": edited_user})
        flash("User edited successfully.")
        return redirect(url_for("main.user", user_id=user_id))
    return render_template("form.html", form=form)

@main.route("/edit-profile/<user_id>", methods=["GET", "POST"])
@login_flags("main.homepage", "logged in", "check user")
def edit_profile(user_id):
    profile_data = db.profiles.find_one({"user_id": user_id})
    form = ProfileForm("Edit Profile", "Please edit your info:")
    form.set_values(profile_data)
    if request.method == "POST":
        edited_profile = blank_profile(
            profile_data["user_id"],
            profile_data["email"],
            **request.form)
        if "profile_picture" in request.files:
            profile_picture = request.files["profile_picture"]
            save_file(profile_picture, f"profile_{user_id}", "uploads", "images")
            db.profiles.update_one(profile_data, {"$set": edited_profile})
        flash("User edited successfully.")
        return redirect(url_for("main.profile", user_id=user_id))
    return render_template("form.html", form=form)

@main.route("/delete/<user_id>", methods=["GET", "POST"])
@login_flags("main.homepage", "logged in", "check user")
def delete_user(user_id):
    user_data = doc_from_id(db.users, user_id)
    form = DeleteUserForm()
    if request.method == "POST":
        if verify_hash(request.form.get("password"), user_data["password"]):
            db.users.delete_one(user_data)
            db.profiles.delete_one({"user_id": user_id})
            flash("User deleted successfully.")
            return redirect(url_for("main.logout"))
        else:
            flash("Password was not correct.")
    return render_template("form.html", form=form)

@main.route("/login", methods=["GET", "POST"])
@login_flags("main.homepage", "logged out")
def login():
    form = LoginForm("Log In", "Please enter your credentials:")
    if request.method == "POST":
        username = request.form.get("username")
        for document in db.users.find({"username": username}):
            if verify_hash(request.form.get("password"), document["password"]):
                session["user_id"] = str(document["_id"])
                flash("Password correct!")
                return redirect(url_for("main.homepage"))
        flash("Password incorrect. Please try again.")
    return render_template("form.html", form=form)

@main.route("/logout")
@login_flags("main.homepage", "logged in")
def logout():
    if "user_id" in session:
        session.pop("user_id")
    return redirect(url_for("main.homepage"))