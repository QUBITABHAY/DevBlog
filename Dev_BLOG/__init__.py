import os
from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mail import Mail

load_dotenv()

app = Flask(__name__)


uri = f"mongodb+srv://codingcontestabhay:{os.getenv('MONGO_PASSWORD')}@cluster0.dst4g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "5ae1861867c107ac09ba2d30d107eb2c")


db = mongo_client["flask_db"]
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

login_manager.login_message_category = "error"

# Email Configuration
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = os.getenv('EMAIL_USER'),
    MAIL_PASSWORD = os.getenv('EMAIL_PASS'),
    MAIL_DEFAULT_SENDER = os.getenv('EMAIL_USER')
)

mail = Mail(app)

from DEV_BLOG import routes