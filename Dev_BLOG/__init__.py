import os
from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mail import Mail

# Load environment variables in development
if os.path.exists('.env'):
    load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
uri = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@cluster0.dst4g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))

# App Configuration
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "5ae1861867c107ac09ba2d30d107eb2c")
app.config["PREFERRED_URL_SCHEME"] = "https"  # Force HTTPS

# Database
db = mongo_client["flask_db"]

# Extensions
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "error"

# Email Configuration
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.getenv('EMAIL_USER'),
    MAIL_PASSWORD = os.getenv('EMAIL_PASS'),
    MAIL_DEFAULT_SENDER = os.getenv('EMAIL_USER')
)

mail = Mail(app)

from DEV_BLOG import routes