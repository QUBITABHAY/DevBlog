import secrets
from PIL import Image
import os
from flask import flash, redirect, render_template, url_for, request
from DEV_BLOG.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, DeletePostForm, RequestResetForm, ResetPasswordForm
from DEV_BLOG import app, db, bcrypt, mail
from DEV_BLOG.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from bson import ObjectId
from flask_mail import Message
import datetime as dt

@app.route("/")
@app.route("/home")
def home():
    posts = list(db.posts.find().sort("date_posted", -1))
    for post in posts:
        post['_id'] = str(post['_id'])
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
        try:

            existing_user = db.users.find_one({
                "$or": [
                    {"email": form.email.data},
                    {"username": form.username.data}
                ]
            })
            
            if existing_user:
                if existing_user.get('email') == form.email.data:
                    flash("Email already registered. Please use a different email.", "danger")
                else:
                    flash("Username already taken. Please choose a different one.", "danger")
                return render_template("register.html", title="Register", form=form)

            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user_data = {
                'username': form.username.data,
                'email': form.email.data,
                'password': hashed_password,
                'image_file': 'default.jpg'
            }
            
            result = db.users.insert_one(user_data)
            if result.inserted_id:
                flash("Your account has been created! You can now log in", "success")
                return redirect(url_for("login"))
            else:
                flash("Error creating account. Please try again.", "danger")
                
        except Exception as e:
            flash(f"Error creating account: {str(e)}", "danger")
            
    return render_template("register.html", title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user_data = db.users.find_one({"email": form.email.data})
            if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
                user = User(user_data)  # Create User instance with user_data
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash("Login successful!", "success")
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash("Login unsuccessful. Please check email and password", "error")
        except Exception as e:
            flash(f"Login error: {str(e)}", "error")
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

    output_size = (400, 400)

    i = Image.open(form_picture)

    if i.mode in ('RGBA', 'P'):
        i = i.convert('RGB')
    
    width, height = i.size
    if width > height:
        delta = width - height
        left = int(delta/2)
        right = width - int(delta/2)
        top = 0
        bottom = height
    else:
        delta = height - width
        left = 0
        right = width
        top = int(delta/2)
        bottom = height - int(delta/2)
    
    i = i.crop((left, top, right, bottom))
    i.thumbnail(output_size, Image.Resampling.LANCZOS)
    
    i.save(picture_path, quality=85, optimize=True)
    
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

            db.posts.update_many(
                {"user_id": current_user.id},
                {"$set": {"author_image": picture_file}}
            )
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": {
                "username": current_user.username,
                "email": current_user.email,
                "image_file": current_user.image_file
            }}
        )
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    posts_count = db.posts.count_documents({"user_id": current_user.id})
    recent_posts = list(db.posts.find(
        {"user_id": current_user.id}
    ).sort("date_posted", -1).limit(5))

    for post in recent_posts:
        post['_id'] = str(post['_id'])

    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title = "Account", image_file=image_file, form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        tags = [tag.strip() for tag in form.tags.data.split(',')] if form.tags.data else []
        post_data = {
            "title": form.title.data,
            "content": form.content.data,
            "user_id": current_user.id,
            "author": current_user.username,
            "author_image": current_user.image_file,
            "category": form.category.data,
            "tags": tags,
            "date_posted": dt.datetime.utcnow()
        }

        result = db.posts.insert_one(post_data)
        post_data['_id'] = str(result.inserted_id)
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")

@app.route("/post/<post_id>")
def post(post_id):
    try:
        post = db.posts.find_one({"_id": ObjectId(post_id)})
        form = DeletePostForm()
        if post:
            return render_template("post.html", title=post["title"], post=post, form=form)
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
                    {"$set": {
                        "title": form.title.data,
                        "content": form.content.data,
                        "category": form.category.data,
                        "tags": tags,
                        "author_image": current_user.image_file
                    }}
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
    
@app.route("/post/<post_id>/delete", methods=["POST"])
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
    return redirect(url_for("home"))

@app.route("/user/<username>")
def user_posts(username):
    user_data = db.users.find_one({"username": username})
    if user_data:
        posts = db.posts.find({"user_id": str(user_data["_id"])}).sort("date_posted", -1)
        return render_template("user_posts.html", posts=posts, user=user_data)
    else:
        flash("User not found!", "error")
        return redirect(url_for("home"))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    reset_url = url_for('reset_token', token=token, _external=True)
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.

This link will expire in 30 minutes.
'''
    try:
        mail.send(msg)
        print(f"Reset URL: {reset_url}")  # For debugging
        return True
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user_data = db.users.find_one({"email": form.email.data})
        if user_data:
            user = User(user_data)
            if send_reset_email(user):
                flash('An email has been sent with instructions to reset your password.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error sending email. Please try again.', 'error')
        else:
            flash('No account found with that email.', 'error')
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.users.update_one(
                {"_id": ObjectId(user.id)},
                {"$set": {"password": hashed_password}}
            )
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error updating password. Please try again.', 'error')
            print(f"Password update error: {str(e)}")
    return render_template('reset_token.html', title='Reset Password', form=form)