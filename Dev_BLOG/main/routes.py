from flask import Blueprint, render_template, request
from Dev_BLOG import db

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    posts = db.posts.find().sort("date_posted", -1)
    return render_template("home.html", post=posts)

@main.route("/about")
def about():
    return render_template("about.html", title="About")