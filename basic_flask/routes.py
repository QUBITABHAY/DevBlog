import secrets
from PIL import Image
import os
from flask import flash, redirect, render_template, url_for, request
from basic_flask.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from basic_flask import app, db, bcrypt
from basic_flask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from bson import ObjectId


@app.route("/")
@app.route("/home")
def home():
    posts = db.posts.find()
    return render_template("home.html", post=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_data = {
            'username': form.username.data,
            'email': form.email.data,
            'password': hashed_password,
            'image_file': 'default.jpg'
        }
        new_user = User(user_data)
        new_user.save()
        flash("Your account has been created! You can now log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = db.users.find_one({"email": form.email.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user = User.from_db(user_data)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Login successful!", "success")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check email and password", "error")
    return render_template('login.html', title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": {"username": current_user.username, "email": current_user.email, "image_file": current_user.image_file}}
        )
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title = "Account", image_file=image_file, form=form)


@app.route("/post/new", methods=["GET", "POST"])
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
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")

@app.route("/post/<post_id>")
def post(post_id):
    try:
        post = db.posts.find_one({"_id": ObjectId(post_id)})
        if post:
            return render_template("post.html", title=post["title"], post=post)
        else:
            flash("Post not found!", "error")
            return redirect(url_for("home"))
    except:
        flash("Invalid post ID!", "error")
        return redirect(url_for("home"))
    
@app.route("/post/<post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    try:
        post = db.posts.find_one({"_id": ObjectId(post_id)})
        if post:
            if post["user_id"] != current_user.id:
                flash("You are not authorized to update this post!", "error")
                return redirect(url_for("home"))
            form = PostForm()
            if form.validate_on_submit():
                tags = [tag.strip() for tag in form.tags.data.split(',')] if form.tags.data else []
                db.posts.update_one(
                    {"_id": ObjectId(post_id)},
                    {"$set": {"title": form.title.data, "content": form.content.data, "category": form.category.data, "tags": tags}}
                )
                flash("Your post has been updated!", "success")
                return redirect(url_for("post", post_id=post_id))
            elif request.method == "GET":
                form.title.data = post["title"]
                form.content.data = post["content"]
                form.category.data = post["category"]
                form.tags.data = ", ".join(post["tags"])
            return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")
        else:
            flash("Post not found!", "error")
            return redirect(url_for("home"))
    except:
        flash("Invalid post ID!", "error")
        return redirect(url_for("home"))