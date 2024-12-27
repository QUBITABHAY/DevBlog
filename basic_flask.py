from flask import Flask
from flask import render_template as e
app = Flask(__name__)

# Making Home Page 

@app.route("/")
@app.route("/home")
def home():
    return e("home.html")


@app.route("/about")
def about():
    return e("about.html")

if __name__ == "__main__":
    app.run(debug=True)