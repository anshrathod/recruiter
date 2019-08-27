from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from recruiter.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # To check if the username already exists
    def validate_username(self, username):
        # Search for username in database
        user = User.query.filter_by(username=username.data).first()
        # If it exists
        if user:
            raise ValidationError('That username is taken. Please choose another.')

    # To check if the email already exists
    def validate_email(self, email):
        # Search for email in database
        user = User.query.filter_by(email=email.data).first()
        # If it exists
        if user:
            raise ValidationError('That email is taken. Please choose another.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', 
                        validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    # To check if the username already exists
    def validate_username(self, username):
        # If username is updated then only check
        if username.data != current_user.username:
            # Search for username in database
            user = User.query.filter_by(username=username.data).first()
            # If it exists
            if user:
                raise ValidationError('That username is taken. Please choose another.')

    # To check if the email already exists
    def validate_email(self, email):
        # If email is updated then only check
        if email.data != current_user.email:
            # Search for email in database
            user = User.query.filter_by(email=email.data).first()
            # If it exists
            if user:
                raise ValidationError('That email is taken. Please choose another.')


class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    min_exp = StringField('Experience Required', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Job')