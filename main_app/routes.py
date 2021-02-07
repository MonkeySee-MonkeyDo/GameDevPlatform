from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from main_app.forms import UserForm, ProfileForm
from main_app.models import blank_user, blank_profile
from main_app import app, db

main = Blueprint("main", __name__)

############################################################
# ROUTES
############################################################

@main.route("/")
def homepage():
    """Homepage -- Displays users for the time being"""
    users_data = db.users.find()
    return render_template("index.html", users=users_data)

@main.route("/user/<user_id>")
def user(user_id):
    """Display user information"""
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("user.html", user=user_data)

@main.route("/profile/<user_id>")
def profile(user_id):
    """Display profile information"""
    profile_data = db.profiles.find_one({"user_id": user_id})
    return render_template("profile.html", profile=profile_data)

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