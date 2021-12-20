from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField

class Signup(FlaskForm):
    firstname = StringField('fname')
    email = StringField('Email')
    password = PasswordField('password')
    confirm_password = PasswordField('confirm_password')
    
    submit = SubmitField('submit')

# class PostForm(FlaskForm):
#      firstname = StringField('title', validators[DataRequired()])

