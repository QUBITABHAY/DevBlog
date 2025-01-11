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

# Configure MongoDB
uri = f"mongodb+srv://codingcontestabhay:{os.getenv('MONGO_PASSWORD')}@cluster0.dst4g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))

# Configure Flask
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "5ae1861867c107ac09ba2d30d107eb2c")

# Initialize MongoDB and other extensions
db = mongo_client["flask_db"]
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

login_manager.login_message_category = "error"

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from basic_flask import routes