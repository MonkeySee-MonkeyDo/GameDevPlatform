from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from main_app.auth.helpers import *
from main_app.main.helpers import *
from main_app.main.forms import *
from main_app.models import *
from main_app import app, db

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def homepage():
    """Homepage"""
    return render_template("mainScreen.html")

@main.route("/users", methods=["GET"])
@login_flags(flags=["logged in"])
def users():
    """Display users"""
    users_data = db.users.find()
    return render_template("users.html", users=users_data)

@main.route("/posts", methods=["GET"])
@login_flags(flags=["logged in"])
def posts():
    """Display posts"""
    posts_data = db.posts.find()
    return render_template("posts.html", posts=posts_data)

@main.route("/users/<user_id>", methods=["GET"])
@login_flags(flags=["logged in"])
def user(user_id):
    """Display user information"""
    user_data = db.users.find_one(get_id(user_id))
    return render_template("user.html", user=user_data)

# @main.route("/profiles/<user_id>", methods=["GET"])
# @login_flags(flags=["logged in"])
# def profile(user_id):
#     """Display profile information"""
#     profile_data = db.profiles.find_one({"user_id": user_id})
#     following = False
#     if "followers" in profile_data:
#         if session["user_id"] in profile_data["followers"]:
#             following = True
#     return render_template("profile.html", profile=profile_data, following=following)

@main.route("/users/<user_id>/edit", methods=["GET", "POST"])
@login_flags(flags=["logged in", "check user"])
def edit_user(user_id):
    '''Allows the user to edit their password'''
    user_data = db.users.find_one(get_id(user_id))
    form = EditUserForm("Edit User", "Please edit your info:")
    form.set_values(user_data)
    if request.method == "POST":
        edited_user = blank_user(**request.form)
        edited_user["password"] = hash_password(edited_user["password"])
        db.users.update_one(user_data, {"$set": edited_user})
        if "profile_picture" in request.files:
            profile_picture = request.files["profile_picture"]
            save_file(profile_picture, f"user_{user_id}.png", "uploads", "images")
        flash("User edited successfully.")
        return redirect(url_for("main.user", user_id=user_id))
    return render_template("form.html", form=form)

# @main.route("/profiles/<user_id>/edit", methods=["GET", "POST"])
# @login_flags(flags=["logged in", "check user"])
# def edit_profile(user_id):
#     '''Allows editing of user profiles'''
#     profile_data = db.profiles.find_one({"user_id": user_id})
#     form = ProfileForm("Edit Profile", "Please edit your info:")
#     form.set_values(profile_data)
#     if request.method == "POST":
#         edited_profile = blank_profile(
#             profile_data["user_id"],
#             profile_data["email"],
#             **request.form)
#         if "profile_picture" in request.files:
#             profile_picture = request.files["profile_picture"]
#             save_file(profile_picture, f"profile_{user_id}", "uploads", "images")
#             db.profiles.update_one(profile_data, {"$set": edited_profile})
#         flash("User edited successfully.")
#         return redirect(url_for("main.profile", user_id=user_id))
#     return render_template("form.html", form=form)

@main.route("/users/<user_id>/delete", methods=["GET", "POST"])
@login_flags(flags=["logged in", "check user"])
def delete_user(user_id):
    '''Allows deletion of user profile'''
    user_data = db.users.find_one(get_id(user_id))
    form = DeleteUserForm()
    if request.method == "POST":
        if verify_hash(request.form.get("password"), user_data["password"]):
            db.users.delete_one(user_data)
            flash("User deleted successfully.")
            return redirect(url_for("auth.logout_user"))
        else:
            flash("Password was not correct.")
    return render_template("form.html", form=form)

@main.route("/follow/<user_id>", methods=["GET"])
@login_flags(flags=["logged in"])
def follow_user(user_id):
    '''Allows following of users'''
    if user_id == session["user_id"]:
        flash("You cannot follow yourself!")
        return redirect(url_for("main.user", user_id=user_id, following=False))
    follower_data = db.users.find_one(get_id(session["user_id"]))
    following_data = db.users.find_one(get_id(user_id))
    if "following" in follower_data:
        following = follower_data["following"]
    else:
        db.users.update_one(get_id(session["user_id"]), {"$set": {"following": []}})
        following = []
    if "followers" in following_data:
        followers = following_data["followers"]
    else:
        db.users.update_one(get_id(user_id), {"$set": {"followers": []}})
        followers = []
    if not user_id in following:
        db.users.update_one(get_id(session["user_id"]), {"$push": {"following": user_id}})
        db.users.update_one(get_id(user_id), {"$push": {"followers": session["user_id"]}})
        flash("You have successfully followed this user.")
    else:
        flash("You are already following this user!")
    return redirect(url_for("main.user", user_id=user_id, following=True))

@main.route("/unfollow/<user_id>", methods=["GET"])
@login_flags(flags=["logged in"])
def unfollow_user(user_id):
    '''Allows unfollowing of users'''
    if user_id == session["user_id"]:
        flash("You cannot unfollow yourself!")
        return redirect(url_for("main.profile", user_id=user_id, following=False))
    follower_data = db.profiles.find_one(get_id(session["user_id"]))
    following_data = db.profiles.find_one(get_id(user_id))
    if "following" in follower_data:
        following = follower_data["following"]
    else:
        db.profiles.update_one(get_id(session["user_id"]), {"$set": {"following": []}})
        flash("You are not following this user!")
        return redirect(url_for("main.profile", user_id=user_id, following=False))
    if "followers" in following_data:
        followers = following_data["followers"]
    else:
        db.profiles.update_one(get_id(user_id), {"$set": {"followers": []}})
        flash("You are not following this user!")
        return redirect(url_for("main.profile", user_id=user_id, following=False))
    if user_id in following:
        db.profiles.update_one(get_id(session["user_id"]), {"$pull": {"following": user_id}})
        db.profiles.update_one(get_id(user_id), {"$pull": {"followers": session["user_id"]}})
        flash("You have successfully unfollowed this user.")
    else:
        flash("You are not following this user!")
    return redirect(url_for("main.user", user_id=user_id, following=False))

@main.route("/projects", methods=["GET"])
@login_flags(flags=["logged in"])
def projects():
    projects_data = db.projects.find()
    return render_template("projects.html", projects=projects_data)

@main.route("/projects/<project_id>", methods=["GET"])
@login_flags(flags=["logged in"])
def project(project_id):
    '''Is the project that the user creates'''
    project_data = db.projects.find_one(get_id(project_id))
    return render_template("project.html", project=project_data)

@main.route("/projects/create", methods=["GET", "POST"])
@login_flags(flags=["logged in"])
def create_project():
    '''Allows the user to create a project'''
    form = ProjectForm("Create Project", "Please fill out project info:")
    if request.method == "POST":
        new_project = blank_project(session["user_id"], **request.form)
        db.projects.insert_one(new_project)
        project_id = str(db.projects.find_one(new_project)["_id"])
        flash("Project successfully created.")
        return redirect(url_for("main.project", project_id=project_id))
    return render_template("form.html", form=form)

@main.route("/projects/<project_id>/edit", methods=["GET"])
@login_flags(flags=["logged in"])
def edit_project(project_id):
    '''Allows the user to edit a prexisting project'''
    project_data = db.projects.find_one(get_id(project_id))
    if not check_user(user_id=project_data["user_id"]):
        return redirect(url_for("main.homepage"))
    form = ProjectForm("Edit Project", "Please edit your profile:")
    form.set_values(project_data)
    if request.method == "POST":
        edited_profile = blank_profile(**request.form)
        db.users.update_one(user_data, {"$set": edited_project})
        flash("Project edited successfully.")
        return redirect(url_for("main.project", project_id=project_id))
    return render_template("form.html", form=form)