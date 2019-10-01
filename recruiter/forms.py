import json

import mysql.connector
from flask import session
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (BooleanField, IntegerField, PasswordField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from recruiter.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    gender = StringField('Gender')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # To check if the username already exists
    def validate_username(self, username):
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor()
        cur.execute("select * from applicants where username=%s;",(session['username'],))
        user = cur.fetchone()
        # Search for username in database
        # Search for username in database
        user = cur.execute("Select username from applicants where username=%s",(username.data,))
        # If it exists
        if user:
            raise ValidationError('That username is taken. Please choose another.')

    # To check if the email already exists
    def validate_email(self, email):
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor()
        cur.execute("select * from applicants where username=%s;",(session['username'],))
        user = cur.fetchone()
       # Search for email in database
        user = cur.execute("select email from applicants where email=%s",(email.data,))
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
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Profile Picture', 
                        validators=[FileAllowed(['jpg','png'])])
    gender = StringField('Gender')
    submit = SubmitField('Update')

    # To check if the username already exists
    def validate_username(self, username):
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor()
        cur.execute("select * from applicants where username=%s;",(session['username'],))
        user = cur.fetchone()
        # If username is updated then only check
        if username.data != user[1]:
            # Search for username in database
            user = cur.execute("Select username from applicants where username=%s",(username.data,))
            # If it exists
            if user:
                raise ValidationError('That username is taken. Please choose another.')

    # To check if the email already exists
    def validate_email(self, email):
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor()
        cur.execute("select * from applicants where username=%s;",(session['username'],))
        user = cur.fetchone()
        # If email is updated then only check
        if email.data != user[2]:
            # Search for email in database
            user = cur.execute("select email from applicants where email=%s",(email.data,))
            # If it exists
            if user:
                raise ValidationError('That email is taken. Please choose another.')


class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    min_exp = StringField('Experience Required', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Job')
