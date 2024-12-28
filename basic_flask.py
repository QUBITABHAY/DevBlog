from flask import Flask
from flask import render_template as e
from flask import url_for 
app = Flask(__name__)

# Adding Dummy Data

post = [
    {
        "author": "Abhay",
        "title": "Blog Post 1",
        "content": "First Post Content",
        "date_posted": "December 27, 2024",
        "desc": "Hello how are you are all",
    },
    {
        "author": "Nikhil",
        "title": "Blog Post 2",
        "content": "Second Post Content",
        "date_posted": "December 28, 2024",
        "desc": "Hi, there hope you are all fine",
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

if __name__ == "__main__":
    app.run(debug=True)