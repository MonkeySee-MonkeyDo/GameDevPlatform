from flask import Blueprint, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from main_app import app, db

main = Blueprint("main", __name__)
sexes = [["Not Set", "Select One..."], ["male", "Male"], ["female", "Female"], ["prefer not to say", "Prefer Not To Say"]]
roles = [["Not Set", "Select One..."], ["developer", "Developer"], ["artist", "Artist"], ["combination", "Both"]]

############################################################
# ROUTES
############################################################

@main.route("/")
def home():
    """Homepage -- Displays users for the time being"""
    users_data = db.users.find()
    return render_template("index.html", users=users_data)

@main.route("/user/<user_id>")
def user(user_id):
    """Display user information"""
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("user.html", user=user_data)

@main.route("/create", methods=["GET", "POST"])
def create():
    """User creation"""
    if request.method == "POST":
        new_user = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "email": request.form.get("email"),
            "phone_number": request.form.get("phone_number"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "dob": request.form.get("dob"),
            "sex": request.form.get("sex"),
            "role": request.form.get("role"),
            "links": [request.form.get("link")]
        }

        # def check_not_set(*keys):
        #     for key in keys:
        #         if not new_user[key]:
        #             new_user[key] = "Not Set"

        db.users.insert_one(new_user)
        new_user_id = db.users.find_one(new_user)["_id"]

        return redirect(url_for("main.user"), user_id=new_user_id)
    else:
        return render_template("create.html", sexes=sexes, roles=roles)

@main.route("/edit/<user_id>", methods=["GET", "POST"])
def edit(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        edited_user_data = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "email": request.form.get("email"),
            "phone_number": request.form.get("phone_number"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "dob": request.form.get("dob"),
            "sex": request.form.get("sex"),
            "role": request.form.get("role"),
            "links": [request.form.get("link")]
        }
        for key, value in edited_user_data.items():
            if value is not user_data[key]:
                db.users.update_one(user_data, {"$set": {key: value}})
        
        return redirect(url_for("main.user", user_id=user_id))
    else:
        return render_template("edit.html", user=user_data, sexes=sexes, roles=roles)