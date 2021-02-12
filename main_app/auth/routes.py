from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from main_app.auth.forms import *
from main_app.auth.helpers import *
from main_app.main.helpers import *
from main_app.models import *
from main_app import db
import random
import functools
import os

auth = Blueprint("auth", __name__)

############################################################
# ROUTES
############################################################

@auth.route("/sign-up", methods=["GET", "POST"])
@login_flags(flags=["logged out"])
def sign_up():
    """User creation"""
    form = UserForm("Create User", "Please fill out your info:")
    if request.method == "POST":
        new_user = blank_user(**request.form)
        new_user["password"] = hash_password(new_user["password"])
        if db.users.count_documents({ "username": request.form.get("username")}, limit=1):
            flash("Username already exists!")
            return redirect(url_for("auth.sign_up"))
        db.users.insert_one(new_user)
        new_user_id = db.users.find_one(new_user)["_id"]
        new_user_email = new_user["email"]
        new_profile = blank_profile(str(new_user_id), new_user_email)
        db.profiles.insert_one(new_profile)
        flash("User created successfully.")
        return redirect(url_for("auth.login", user_id=new_user_id))
    return render_template("form.html", form=form)

@auth.route("/login", methods=["GET", "POST"])
@login_flags(flags=["logged out"])
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

@auth.route("/logout")
@login_flags(flags=["logged in"])
def logout():
    if "user_id" in session:
        session.pop("user_id")
    return redirect(url_for("main.homepage"))