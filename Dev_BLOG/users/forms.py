from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Dev_BLOG import db
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6), EqualTo("password")])
    submit = SubmitField("Sign Up")
    
    # Validate Feilds
    def validate_username(self, username):
        user = db.users.find_one({"username": username.data})
        if user:
            raise ValidationError("Username already exists. Please choose a different one.")

    def validate_email(self, email):
        user = db.users.find_one({"email": email.data})
        if user:
            raise ValidationError("Email already exists. Please choose a different one.")
    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
    
class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture  = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    # Validate Feilds
    def validate_username(self, username):
        if username.data != current_user.username:
            user = db.users.find_one({"username": username.data})
            if user:
                raise ValidationError("Username already exists. Please choose a different one.")
            
    def validate_email(self, email):
        if email.data != current_user.email:
                user = db.users.find_one({"email": email.data})
                if user:
                    raise ValidationError("Email already exists. Please choose a different one.")
                
<<<<<<< HEAD:Dev_BLOG/users/forms.py
<<<<<<< HEAD:Dev_BLOG/users/forms.py
                
class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    
    def validate_email(self, email):
        user = db.users.find_one({"email": email.data})
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6), EqualTo("password")])
    submit = SubmitField("Reset Password")
=======
=======
>>>>>>> parent of 79edb7f (add to change password feature):basic_flask/forms.py

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    tags = StringField("Tags", validators=[DataRequired()])
    submit = SubmitField("Post")

class DeletePostForm(FlaskForm):
<<<<<<< HEAD:Dev_BLOG/users/forms.py
    submit = SubmitField('Delete')
>>>>>>> parent of 79edb7f (add to change password feature):basic_flask/forms.py
=======
    submit = SubmitField('Delete')
>>>>>>> parent of 79edb7f (add to change password feature):basic_flask/forms.py
