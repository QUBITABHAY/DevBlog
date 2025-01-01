from flask import Flask, flash, redirect
from flask import render_template as e
from flask import url_for 
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)

# 
app.config["SECRET_KEY"] = "5ae1861867c107ac09ba2d30d107eb2c"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default="")
    password = db.Column(db.String(60), nullable = False)
    post = db.relationship("Post", backref = 'author', lazy = True)
    
    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = dt.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    
    def __repr__(self):
        return f"Post ('{self.title}', '{self.date_posted}')"
        
# Adding Dummy Data
post = [
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

# Making Home Page 

@app.route("/")
@app.route("/home")
def home():
    return e("home.html", post = post)

# Making About Page

@app.route("/about")
def about():
    return e("about.html", title = "About")


@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return e("register.html", title = "Register", form = form)


@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "1234567":
            flash(f"You have been looged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check Username and Password", "error")
    return e("login.html", title = "Login", form = form)


if __name__ == "__main__":
    app.run(debug=True)