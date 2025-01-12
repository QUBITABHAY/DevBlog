from flask import Blueprint, render_template, request, flash, redirect, url_for
from Dev_BLOG import db, bcrypt
from Dev_BLOG.models import User
from Dev_BLOG.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from bson import ObjectId
from Dev_BLOG.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
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
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = db.users.find_one({"email": form.email.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user = User.from_db(user_data)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Login successful!", "success")
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login unsuccessful. Please check email and password", "error")
    return render_template('login.html', title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title = "Account", image_file=image_file, form=form)

@users.route("/user/<username>")
def user_posts(username):
    user_data = db.users.find_one({"username": username})
    if user_data:
        posts = db.posts.find({"user_id": str(user_data["_id"])}).sort("date_posted", -1)
        return render_template("user_posts.html", posts=posts, user=user_data)
    else:
        flash("User not found!", "error")
        return redirect(url_for("main.home"))

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user_data = db.users.find_one({"email": form.email.data})
        if user_data:
            user = User.from_db(user_data)
            send_reset_email(user)
            flash("An email has been sent with instructions to reset your password.", "info")
            return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        user.save()
        flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)