from flask import flash, redirect, render_template, url_for, request
from basic_flask.forms import RegistrationForm, LoginForm, UpdateAccountForm
from basic_flask import app, db, bcrypt
from basic_flask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# Dummy data remains the same for demonstration
posts = [
    {
        "author": "Abhay",
        "title": "Blog Post 1",
        "content": "First Post Content",
        "date_posted": "December 27, 2024",
        "desc": "Hello how are you all",
        "category": "Programming",
        "tags": ["Python", "Web Development", "Flask"]
    },
    {
        "author": "Nikhil",
        "title": "Blog Post 2",
        "content": "Second Post Content",
        "date_posted": "December 28, 2024",
        "desc": "Hi, there hope you are all fine",
        "category": "Programming",
        "tags": ["Python", "Web Development", "Flask"]
    },
    {
        "author": "Vishal",
        "title": "Blog Post 3",
        "content": "Third Post Content",
        "date_posted": "December 28, 2024",
        "desc": "Good day, how are you all",
        "category": "Programming",
        "tags": ["Python", "Web Development", "Flask"]
    },
    {
        "author": "John Smith",
        "title": "Getting Started with Flask",
        "content": "Flask is a lightweight WSGI web application framework in Python. It's designed to get started quickly and scale up to complex applications.",
        "date_posted": "January 15, 2024",
        "desc": "Learn the basics of Flask framework and build your first web application",
        "category": "Programming",
        "tags": ["Python", "Web Development", "Flask"]
    },
    {
        "author": "Emma Wilson",
        "title": "Python Best Practices",
        "content": "Understanding Python best practices is crucial for writing clean, maintainable code. Let's explore key principles and patterns.",
        "date_posted": "January 16, 2024",
        "desc": "Essential tips for writing better Python code",
        "category": "Development",
        "tags": ["Python", "Clean Code", "Best Practices"]
    },
    {
        "author": "Michael Chen",
        "title": "Web Security Fundamentals",
        "content": "Security is paramount in web development. This post covers essential security practices for modern web applications.",
        "date_posted": "January 17, 2024",
        "desc": "Learn about crucial web security concepts and implementations",
        "category": "Security",
        "tags": ["Security", "Web Development", "Best Practices"]
    },
    {
        "author": "Sarah Johnson",
        "title": "Database Design Patterns",
        "content": "Effective database design is crucial for application performance. Explore common patterns and anti-patterns.",
        "date_posted": "January 18, 2024",
        "desc": "Master database design patterns for better applications",
        "category": "Database",
        "tags": ["Database", "Design Patterns", "Architecture"]
    },
    {
        "author": "James Brown",
        "title": "Advanced JavaScript Concepts",
        "content": "Deep dive into advanced JavaScript concepts such as closures, promises, and asynchronous programming.",
        "date_posted": "January 20, 2024",
        "desc": "Master complex JavaScript concepts for better web development",
        "category": "Programming",
        "tags": ["JavaScript", "Web Development", "Asynchronous"]
    },
    {
        "author": "Olivia Green",
        "title": "Building RESTful APIs with Flask",
        "content": "In this post, we explore how to build RESTful APIs with Flask, including methods like GET, POST, PUT, and DELETE.",
        "date_posted": "January 22, 2024",
        "desc": "Learn how to create RESTful APIs with Flask and Python",
        "category": "Programming",
        "tags": ["Flask", "API", "RESTful"]
    },
    {
        "author": "David Lee",
        "title": "Mastering SQL Queries",
        "content": "SQL is the backbone of many applications. This post explores key SQL query techniques to improve your database interactions.",
        "date_posted": "January 25, 2024",
        "desc": "Learn how to write complex SQL queries efficiently",
        "category": "Database",
        "tags": ["SQL", "Database", "Queries"]
    }
]

@app.route("/")
@app.route("/home")
def home():
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


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # if form.picture.data:
            # picture_file = save_picture(form.picture.data)
            # current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.users.update_one(
            {"_id": (current_user.id)},
            {"$set": {"username": current_user.username, "email": current_user.email}}
        )
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title = "Account", image_file=image_file, form=form)