from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,SubmitField,BooleanField
from wtforms.validators import DataRequired,EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired()])
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    job_title = StringField('Job title',validators = [DataRequired()])
    email = StringField('Email',validators = [DataRequired()])
    confirm_email = StringField('Confirm Email',validators = [DataRequired(),EqualTo('email', message='Emails must match')])
    password = PasswordField('Password',validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')