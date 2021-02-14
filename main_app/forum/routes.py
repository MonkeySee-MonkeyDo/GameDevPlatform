from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from misaka import html
from main_app.auth.helpers import *
from main_app.main.helpers import *
from main_app.forum.forms import *
from main_app.models import *
from main_app import db

forum = Blueprint("forum", __name__)

@forum.route("/create-post", methods=["GET", "POST"])
@login_flags(flags=["logged in"])
def create_post():
    """Post creation"""
    users = db.users.find()
    form = PostForm("Create Post", "Please fill out post info:", users)
    if request.method == "POST":
        new_post = blank_post(user_id=session["user_id"], **request.form)
        db.posts.insert_one(new_post)
        new_post_id = db.posts.find_one(new_post)["_id"]
        flash("Post created successfully.")
        return redirect(url_for("forum.post", post_id=str(new_post_id)))
    return render_template("form.html", form=form)

@forum.route("/posts/<post_id>", methods=["GET", "POST"])
@login_flags(flags=["logged in"])
def post(post_id):
    """Display post information"""
    post_data = doc_from_id(db.posts, post_id)
    post_data["user"] = doc_from_id(db.users, post_data["user_id"])
    users = db.users.find()
    replies = [reply for reply in db.replies.find({"post_id": post_id})]
    for reply in replies:
        reply["user"] = doc_from_id(db.users, reply["user_id"])
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
        return redirect(url_for("forum.post", post_id=post_id))
    return render_template("post.html", post=post_data, form=form, replies=replies)