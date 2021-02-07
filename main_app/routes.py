from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from main_app.forms import UserForm, ProfileForm, PostForm
from main_app.models import *
from main_app import app, db

main = Blueprint("main", __name__)

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
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("user.html", user=user_data)

@main.route("/profiles/<user_id>")
def profile(user_id):
    """Display profile information"""
    profile_data = db.profiles.find_one({"user_id": user_id})
    return render_template("profile.html", profile=profile_data)

@main.route("/posts/<post_id>")
def post(post_id):
    # TODO: jinja template
    """Display post information"""
    post_data = db.posts.find_one({"_id": ObjectId(post_id)})
    return render_template("post.html", post=post_data)

@main.route("/create", methods=["GET", "POST"])
def create_user():
    """User creation"""
    form = UserForm()
    if request.method == "POST":
        new_user = blank_user(**request.form)
        db.users.insert_one(new_user)
        new_user_id = db.users.find_one(new_user)["_id"]
        new_user_email = new_user["email"]
        new_profile = blank_profile(str(new_user_id), new_user_email)
        db.profiles.insert_one(new_profile)
        flash("User created successfully.")
        return redirect(url_for("main.user", user_id=new_user_id))
    return render_template("create.html", form=form)

@main.route("/create-post", methods=["GET", "POST"])
def create_post():
    """Post creation"""
    users = db.users.find({})
    form = PostForm(users)
    if request.method == "POST":
        new_post = blank_post(**request.form)
        db.posts.insert_one(new_post)
        flash("Post created successfully.")
        return redirect(url_for("main.homepage"))
    return render_template("create_post.html", form=form)

@main.route("/edit-user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    form = UserForm()
    form.set_values(user_data)
    if request.method == "POST":
        edited_user = blank_user(**request.form)
        db.users.update_one(user_data, {"$set": edited_user})
        flash("User edited successfully.")
        return redirect(url_for("main.user", user_id=user_id))
    return render_template("edit_user.html", form=form)

@main.route("/edit-profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    profile_data = db.profiles.find_one({"user_id": user_id})
    form = ProfileForm()
    form.set_values(profile_data)
    if request.method == "POST":
        edited_profile = blank_profile(
            profile_data["user_id"],
            profile_data["email"],
            **request.form)
        db.profiles.update_one(profile_data, {"$set": edited_profile})
        flash("User edited successfully.")
        return redirect(url_for("main.profile", user_id=user_id))
    return render_template("edit_user.html", form=form)

@main.route("/delete/<user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        password = request.form.get("password")
        if user_data["password"] == password:
            db.users.delete_one(user_data)
            db.profiles.delete_one({"user_id": user_id})
            flash("User deleted successfully.")
            return redirect(url_for("main.homepage"))
        else:
            flash("Password was not correct.")
    return render_template("delete.html")