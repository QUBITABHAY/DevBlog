from datetime import datetime as dt
from DEV_BLOG import db, login_manager, app
from bson import ObjectId
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.from_db(db.users.find_one({"_id": ObjectId(user_id)}))

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id')) if user_data else None
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.password = user_data.get('password')
        self.image_file = user_data.get('image_file', 'default.jpg')
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}).encode('utf-8')
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.from_db(db.users.find_one({'_id': ObjectId(user_id)}))

    @staticmethod
    def from_db(user_data):
        if not user_data:
            return None
        return User(user_data)
    
    def save(self):
        if self.id:
            db.users.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {
                    'username': self.username,
                    'email': self.email,
                    'password': self.password,
                    'image_file': self.image_file
                }}
            )
        else:
            result = db.users.insert_one({
                'username': self.username,
                'email': self.email,
                'password': self.password,
                'image_file': self.image_file
            })
            self.id = str(result.inserted_id)

class Post:
    def __init__(self, post_data):
        self.id = str(post_data.get('_id')) if post_data else None
        self.title = post_data.get('title')
        self.content = post_data.get('content')
        self.date_posted = post_data.get('date_posted', dt.utcnow())
        self.user_id = str(post_data.get('user_id'))
        self.category = post_data.get('category')
        self.tags = post_data.get('tags', [])
    
    @staticmethod
    def from_db(post_data):
        if not post_data:
            return None
        return Post(post_data)
    
    def save(self):
        if self.id:
            db.posts.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {
                    'title': self.title,
                    'content': self.content,
                    'date_posted': self.date_posted,
                    'user_id': ObjectId(self.user_id),
                    'category': self.category,
                    'tags': self.tags
                }}
            )
        else:
            result = db.posts.insert_one({
                'title': self.title,
                'content': self.content,
                'date_posted': self.date_posted,
                'user_id': ObjectId(self.user_id),
                'category': self.category,
                'tags': self.tags
            })
            self.id = str(result.inserted_id)