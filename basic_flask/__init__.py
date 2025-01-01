from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 
app.config["SECRET_KEY"] = "5ae1861867c107ac09ba2d30d107eb2c"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

from basic_flask import routes