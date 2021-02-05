from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from main_app.forms import UserForm
from main_app import app, db

main = Blueprint("main", __name__)

############################################################
# ROUTES
############################################################

@main.route("/")
def home():
    """Homepage -- Displays users for the time being"""
    # get list of all users
    users_data = db.users.find()
    return render_template("index.html", users=users_data)

@main.route("/user/<user_id>")
def user(user_id):
    """Display user information"""
    # get user document
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("user.html", user=user_data)

@main.route("/create", methods=["GET", "POST"])
def create():
    """User creation"""
    # create new user form
    form = UserForm()
    # if form submitted
    if request.method == "POST":
        # create new user document using form values
        new_user = request.form.to_dict()
        new_user["links"] = [new_user["links"]]
        # create function to set empty values to "not set"
        def check_not_set(*keys):
            for key in keys:
                if not new_user[key]:
                    new_user[key] = "not set"
        # set phone number and dob to "not set" if values are empty
        check_not_set("phone_number", "dob")
        # add new user to collection
        db.users.insert_one(new_user)
        # get new user id
        new_user_id = db.users.find_one(new_user)["_id"]
        flash("User created successfully.")
        # redirect to new user
        return redirect(url_for("main.user", user_id=new_user_id))
    else:
        # render create page
        return render_template("create.html", form=form)

@main.route("/edit/<user_id>", methods=["GET", "POST"])
def edit(user_id):
    # get user data
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    # create new form object and set default values based on user data
    form = UserForm()
    form.set_values(user_data)
    # if form is submitted
    if request.method == "POST":
        # create edited user document using form values
        edited_user_data = request.form.to_dict()
        edited_user_data["links"] = [edited_user_data["links"]]
        # iterate through edited data and update values
        for key, value in edited_user_data.items():
            if value != user_data[key]:
                db.users.update_one(user_data, {"$set": {key: value}})
        flash("User edited successfully.")
        return redirect(url_for("main.user", user_id=user_id))
    else:
        # render edit page
        return render_template("edit.html", form=form)