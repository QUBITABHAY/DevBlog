from datetime import datetime as dt
from basic_flask import db, login_manager
from bson import ObjectId
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id')) if user_data else None
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.password = user_data.get('password')
        self.image_file = user_data.get('image_file', 'default.jpg')

    @staticmethod
    def from_db(user_data):
        if not user_data:
            return None
        return User(user_data)
    
    def save(self):
        # Create unique indexes
        db.users.create_index([("username", 1)], unique=True)
        db.users.create_index([("email", 1)], unique=True)
        
        user_data = {
            "_id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "image_file": self.image_file
        }
        db.users.insert_one(user_data)

@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None
    try:
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        return User.from_db(user_data)
    except:
        return None
    

class Post:
    def __init__(self, title, content, user_id, date_posted=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.title = title
        self.content = content
        self.user_id = user_id
        self.date_posted = date_posted or dt.utcnow()

    @staticmethod
    def from_db(data):
        if not data:
            return None
        return Post(
            title=data['title'],
            content=data['content'],
            user_id=data['user_id'],
            date_posted=data['date_posted'],
            _id=data.get('_id')
        )

    def save(self):
        # Create index for user_id for efficient querying
        db.posts.create_index([("user_id", 1)])
        
        post_data = {
            "_id": self._id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "date_posted": self.date_posted
        }
        db.posts.insert_one(post_data)