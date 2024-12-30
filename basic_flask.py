from flask import Flask, flash, redirect
from flask import render_template as e
from flask import url_for 
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# 
app.config["SECRET_KEY"] = "5ae1861867c107ac09ba2d30d107eb2c"


# Adding Dummy Data

post = [
    {
        "author": "Abhay",
        "title": "Blog Post 1",
        "content": "First Post Content",
        "date_posted": "December 27, 2024",
        "desc": "Hello how are you are all",
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
    }
]

# Making Home Page 

@app.route("/")
@app.route("/home")
def home():
    return e("home.html", post=post)

# Making About Page

@app.route("/about")
def about():
    return e("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return e("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return e("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)