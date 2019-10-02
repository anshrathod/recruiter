from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from recruiter.models import User
import mysql.connector,json
from flask import session, request

class ApplicantRegistrationForm(FlaskForm):
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
    user_type = StringField('Type')


    submit = SubmitField('Sign Up')

    # To check if the username already exists
    def validate_username(self, username):
        print(username.data)
        print(request.form['user_type'])
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor(buffered=True)
        # cur.execute("select * from applicants where username=%s;",(username.data,))
        # user = cur.fetchone()
        # Search for username in database
        # Search for username in database
        cur.execute("Select username from applicants where username=%s",(username.data,))
        user = cur.fetchone()
        print(user)
        # If it exists
        if user:
            raise ValidationError('That username is taken. Please choose another.')
        cur.close()
        cnx.close()

    # To check if the email already exists
    def validate_email(self, email):
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor(buffered=True)
        # cur.execute("select * from applicants where username=%s;",(session['username'],))
        # user = cur.fetchone()
       # Search for email in database
        cur.execute("select email from applicants where email=%s",(email.data,))
        user = cur.fetchone()
        # If it exists
        if user:
            raise ValidationError('That email is taken. Please choose another.')
        cur.close()
        cnx.close()


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateProfileForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Profile Picture', 
                        validators=[FileAllowed(['jpg','png'])])
    gender = StringField('Gender')
    submit = SubmitField('Update')

    # To check if the username already exists
    def validate_username(self, username):
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor(buffered=True)
        cur.execute("select username from applicants where username=%s;",(username.data,))
        user = cur.fetchone()
        print(user,session['username'])
        if user != session['username']:
            if user:
                raise ValidationError('That username is taken. Please choose another.')
        cur.close()
        cnx.close()

class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    min_exp = StringField('Experience Required', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Job')

class CompanyRegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    location = TextAreaField('Location', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    c_type = StringField('Company Type',
                           validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
            
    submit = SubmitField('Sign Up')

    # To check if the email already exists
    def validate_email(self, email):
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor(buffered=True)
        cur.execute("select email from company where email=%s",(email.data,))
        user = cur.fetchone()
        if user:
            raise ValidationError('That email is taken. Please choose another.')
        cur.close()
        cnx.close()

    