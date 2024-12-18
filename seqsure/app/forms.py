from flask_wtf import FlaskForm
from wt_forms import StringField,SubmitField
from wt_forms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired()])
    password = StringField('Password',validators = [DataRequired()])
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    job_title = StringField('Job title',validators = [DataRequired()])
    email = StringField('Email',validators = [DataRequired()])
    confirm_email = StringField('Confirm Email',validators = [DataRequired()])
    password = StringField('Password',validators = [DataRequired()])
    submit = SubmitField('Register')