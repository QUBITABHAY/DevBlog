from datetime import datetime as dt
from basic_flask import db

class User:
    def __init__(self, username, email, password, image_file="default.jpg"):
        self.username = username
        self.email = email
        self.password = password
        self.image_file = image_file
        
    @staticmethod
    def from_db(data):
        if not data:
            return None
        return User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            image_file=data.get('image_file', 'default.jpg')
        )

    def save(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "image_file": self.image_file
        }
        db.users.insert_one(user_data)

class Post:
    def __init__(self, title, content, user_id, date_posted=None):
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
            date_posted=data['date_posted']
        )

    def save(self):
        post_data = {
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "date_posted": self.date_posted
        }
        db.posts.insert_one(post_data)