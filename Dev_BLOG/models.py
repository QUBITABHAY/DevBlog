from datetime import datetime as dt
from DEV_BLOG import db, login_manager, app
from bson import ObjectId
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password = user_data['password']
        self.image_file = user_data.get('image_file', 'default.jpg')
    
    def get_reset_token(self):
        serializer = Serializer(app.config['SECRET_KEY'])
        # Include both user_id and email in token
        return serializer.dumps({'user_id': self.id, 'email': self.email})
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token, max_age=expires_sec)
            user_data = db.users.find_one({
                '_id': ObjectId(data['user_id']),
                'email': data['email']
            })
            return User(user_data) if user_data else None
        except:
            return None

    @staticmethod
    def from_db(user_data):
        if not user_data:
            return None
        return User(user_data)
    
    def save(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'image_file': self.image_file
        }
        
        if hasattr(self, 'id') and self.id:
            db.users.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': user_data}
            )
        else:
            result = db.users.insert_one(user_data)
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