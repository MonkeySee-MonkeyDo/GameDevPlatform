from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from markdown import markdown
from main_app.forms import *
from main_app.models import *
from main_app import app, db
import os

main = Blueprint("main", __name__)

############################################################
# HELPER FUNCTIONS
############################################################

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
    users_data = db.users.find()
    return render_template("users.html", users=users_data)

@main.route("/posts")
def posts():
    # TODO: jinja template
    """Display posts"""
    posts_data = db.posts.find()
    return render_template("posts.html", posts=posts_data)

@main.route("/users/<user_id>")
def user(user_id):
    """Display user information"""
    user_data = doc_from_id(db.users, user_id)
    return render_template("user.html", user=user_data)

@main.route("/profiles/<user_id>")
def profile(user_id):
    """Display profile information"""
    profile_data = db.profiles.find_one({"user_id": user_id})
    return render_template("profile.html", profile=profile_data)

@main.route("/posts/<post_id>", methods=["GET", "POST"])
def post(post_id):
    # TODO: jinja template
    """Display post information"""
    post_data = doc_from_id(db.posts, post_id)
    post_data["user"] = doc_from_id(db.users, post_data["user_id"])
    post_data["body"] = markdown(post_data["body"])
    users = db.users.find()
    replies = [reply for reply in db.replies.find({"post_id": post_id})]
    for reply in replies:
        reply["user"] = doc_from_id(db.users, reply["user_id"])
        reply["body"] = markdown(reply["body"])
    form = ReplyForm(None, None, users)
    if request.method == "POST":
        reply_variables = {
            "user_id": request.form.get("user_id"),
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
    form = UserForm("Create User", "Please fill out your info:")
    if request.method == "POST":
        new_user = blank_user(**request.form)
        if db.users.count_documents({ "username": request.form.get("username")}, limit=1):
            flash("Username already exists!")
            return redirect(url_for("main.create_user"))
        db.users.insert_one(new_user)
        new_user_id = db.users.find_one(new_user)["_id"]
        new_user_email = new_user["email"]
        new_profile = blank_profile(str(new_user_id), new_user_email)
        db.profiles.insert_one(new_profile)
        flash("User created successfully.")
        return redirect(url_for("main.user", user_id=new_user_id))
    return render_template("form.html", form=form)

@main.route("/create-post", methods=["GET", "POST"])
def create_post():
    """Post creation"""
    users = db.users.find()
    form = PostForm("Create Post", "Please fill out post info:", users)
    if request.method == "POST":
        new_post = blank_post(**request.form)
        db.posts.insert_one(new_post)
        flash("Post created successfully.")
        return redirect(url_for("main.homepage"))
    return render_template("form.html", form=form)

@main.route("/edit-user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
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
    form = DeleteUserForm()
    user_data = doc_from_id(db.users, user_id)
    if request.method == "POST":
        password = request.form.get("password")
        if user_data["password"] == password:
            db.users.delete_one(user_data)
            db.profiles.delete_one({"user_id": user_id})
            flash("User deleted successfully.")
            return redirect(url_for("main.homepage"))
        else:
            flash("Password was not correct.")
    return render_template("form.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm("Log In", "Please enter your credentials:")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        for db_password in db.users.find({"username": username}):
            if password == db_password["password"]:
                flash("Password correct!")
                return redirect(url_for("main.homepage"))
        flash("Password incorrect. Please try again.")
    return render_template("form.html", form=form)