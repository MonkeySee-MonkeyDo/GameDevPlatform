from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

############################################################
# SETUP
############################################################

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

############################################################
# ROUTES
############################################################

@app.route("/")
def home():
    """Homepage -- Displays users for the time being"""
    users_data = mongo.db.users.find()
    return render_template("index.html", users=users_data)

@app.route("/user/<user_id>")
def user(user_id):
    """Display user information"""
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("user.html", user=user_data)

@app.route("/create", methods=["GET", "POST"])
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

        mongo.db.users.insert_one(new_user)
        new_user_id = mongo.db.users.find_one(new_user)["_id"]

        return redirect(url_for("user"), user_id=new_user_id)
    else:
        return render_template("create.html")

if __name__ == '__main__':
    app.run(debug=True)