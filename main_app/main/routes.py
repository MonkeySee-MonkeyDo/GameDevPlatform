from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from main_app.auth.helpers import *
from main_app.main.helpers import *
from main_app.main.forms import *
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
@login_flags(flags=["logged in"])
def users():
    """Display users"""
    users_data = db.users.find()
    return render_template("users.html", users=users_data)

@main.route("/posts")
@login_flags(flags=["logged in"])
def posts():
    """Display posts"""
    posts_data = db.posts.find()
    return render_template("posts.html", posts=posts_data)

@main.route("/users/<user_id>")
@login_flags(flags=["logged in"])
def user(user_id):
    """Display user information"""
    user_data = doc_from_id(db.users, user_id)
    return render_template("user.html", user=user_data)

@main.route("/profiles/<user_id>")
@login_flags(flags=["logged in"])
def profile(user_id):
    """Display profile information"""
    profile_data = db.profiles.find_one({"user_id": user_id})
    return render_template("profile.html", profile=profile_data)

@main.route("/users/<user_id>/edit", methods=["GET", "POST"])
@login_flags(flags=["logged in", "check user"])
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

@main.route("/profiles/<user_id>/edit", methods=["GET", "POST"])
@login_flags(flags=["logged in", "check user"])
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

@main.route("/users/<user_id>/delete", methods=["GET", "POST"])
@login_flags(flags=["logged in", "check user"])
def delete_user(user_id):
    user_data = doc_from_id(db.users, user_id)
    form = DeleteUserForm()
    if request.method == "POST":
        if verify_hash(request.form.get("password"), user_data["password"]):
            db.users.delete_one(user_data)
            db.profiles.delete_one({"user_id": user_id})
            flash("User deleted successfully.")
            return redirect(url_for("auth.logout"))
        else:
            flash("Password was not correct.")
    return render_template("form.html", form=form)