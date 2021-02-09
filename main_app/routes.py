from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from markdown import markdown
from passlib.hash import pbkdf2_sha256
from main_app.forms import *
from main_app.models import *
from main_app import app, db
import os

main = Blueprint("main", __name__)

############################################################
# HELPER FUNCTIONS
############################################################

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_hash(a, b):
    return pbkdf2_sha256.verify(a, b)

# TODO: gotta be a better way to handle this
def check_logged_in():
    if not "user_id" in session:
        flash("You must be logged in to do this.")
        return redirect(url_for("main.login"))
    return True

def check_correct_login(user_id):
    if session["user_id"] != user_id:
        flash("You are not logged in as this user!")
        return redirect(url_for("main.homepage"))
    return True

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
# ROUTES
############################################################

@main.route("/")
def homepage():
    """Homepage"""
    return render_template("index.html")

@main.route("/users")
def users():
    """Display users"""
    if not (log := check_logged_in()) == True:
        return log
    users_data = db.users.find()
    return render_template("users.html", users=users_data)

@main.route("/posts")
def posts():
    """Display posts"""
    if not (log := check_logged_in()) == True:
        return log
    posts_data = db.posts.find()
    return render_template("posts.html", posts=posts_data)

@main.route("/users/<user_id>")
def user(user_id):
    """Display user information"""
    if not (log := check_logged_in()) == True:
        return log
    user_data = doc_from_id(db.users, user_id)
    return render_template("user.html", user=user_data)

@main.route("/profiles/<user_id>")
def profile(user_id):
    """Display profile information"""
    if not (log := check_logged_in()) == True:
        return log
    profile_data = db.profiles.find_one({"user_id": user_id})
    return render_template("profile.html", profile=profile_data)

@main.route("/posts/<post_id>", methods=["GET", "POST"])
def post(post_id):
    """Display post information"""
    if not (log := check_logged_in()) == True:
        return log
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
def create_user():
    """User creation"""
    if "user_id" in session:
        flash("You are already logged in!")
        return redirect(url_for("main.homepage"))
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
def create_post():
    """Post creation"""
    if not (log := check_logged_in()) == True:
        return log
    users = db.users.find()
    form = PostForm("Create Post", "Please fill out post info:", users)
    if request.method == "POST":
        new_post = blank_post(user_id=session["user_id"], **request.form)
        db.posts.insert_one(new_post)
        flash("Post created successfully.")
        return redirect(url_for("main.homepage"))
    return render_template("form.html", form=form)

@main.route("/edit-user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if not (log := check_logged_in()) == True:
        return log
    if not (log := check_correct_login(user_id)) == True:
        return log
    user_data = doc_from_id(db.users, user_id)
    form = UserForm("Edit User", "Please edit your info:")
    form.set_values(user_data)
    if request.method == "POST":
        edited_user = blank_user(**request.form)
        db.users.update_one(user_data, {"$set": edited_user})
        flash("User edited successfully.")
        return redirect(url_for("main.user", user_id=user_id))
    return render_template("form.html", form=form)

@main.route("/edit-profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    if not (log := check_logged_in()) == True:
        return log
    if not (log := check_correct_login(user_id)) == True:
        return log
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
def delete_user(user_id):
    if not (log := check_correct_login(user_id)) == True:
        return log
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
def logout():
    if "user_id" in session:
        session.pop("user_id")
    else:
        flash("You are not logged in.")
    return redirect(url_for("main.homepage"))