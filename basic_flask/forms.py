from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from basic_flask import db
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