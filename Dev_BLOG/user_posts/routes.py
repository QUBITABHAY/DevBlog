from flask import Blueprint, render_template, request, flash, redirect, url_for
from Dev_BLOG import db
from Dev_BLOG.models import Post
from Dev_BLOG.user_posts.forms import PostForm, DeletePostForm
from flask_login import current_user, login_required
from bson import ObjectId


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        tags = [tag.strip() for tag in form.tags.data.split(',')] if form.tags.data else []
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        post_data = {
            "_id": post._id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "author": current_user.username,
            "category": form.category.data,
            "tags": tags,
            "date_posted": post.date_posted
        }
        db.posts.insert_one(post_data)
        flash("Your post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")

@posts.route("/post/<post_id>")
def post(post_id):
    try:
        post = db.posts.find_one({"_id": ObjectId(post_id)})
        form = DeletePostForm()
        if post:
            return render_template("post.html", title=post["title"], post=post, form=form)
        else:
            flash("Post not found!", "error")
            return redirect(url_for("main.home"))
    except:
        flash("Invalid post ID!", "error")
        return redirect(url_for("main.home"))

@posts.route("/post/<post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    try:
        post = db.posts.find_one({"_id": ObjectId(post_id)})
        if post:
            if post["user_id"] != current_user.id:
                flash("You are not authorized to update this post!", "error")
                return redirect(url_for("main.home"))
            form = PostForm()
            if form.validate_on_submit():
                tags = [tag.strip() for tag in form.tags.data.split(',')] if form.tags.data else []
                db.posts.update_one(
                    {"_id": ObjectId(post_id)},
                    {"$set": {"title": form.title.data, "content": form.content.data, "category": form.category.data, "tags": tags}}
                )
                flash("Your post has been updated!", "success")
                return redirect(url_for("posts.post", post_id=post_id))
            elif request.method == "GET":
                form.title.data = post["title"]
                form.content.data = post["content"]
                form.category.data = post["category"]
                form.tags.data = ", ".join(post["tags"])
            return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")
        else:
            flash("Post not found!", "error")
            return redirect(url_for("main.home"))
    except:
        flash("Invalid post ID!", "error")
        return redirect(url_for("main.home"))

@posts.route("/post/<post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    try:
        post = db.posts.find_one({"_id": ObjectId(post_id)})
        if post and post["user_id"] == current_user.id:
            db.posts.delete_one({"_id": ObjectId(post_id)})
            flash("Your post has been deleted!", "success")
        else:
            flash("You do not have permission to delete this post.", "error")
    except:
        flash("Invalid post ID!", "error")
    return redirect(url_for("main.home"))