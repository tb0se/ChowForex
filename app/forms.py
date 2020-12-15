from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email
import email_validator

class RegistrationForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired()])
    lname = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[ DataRequired(),
        EqualTo('confirmPassword', message='Passwords must match')
    ])
    confirmPassword = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Confirm Password',validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')