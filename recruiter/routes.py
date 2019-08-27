import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from recruiter import app, db, bcrypt
from recruiter.forms import RegistrationForm, LoginForm, UpdateProfileForm, JobForm
from recruiter.models import User, Job
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/display")
def display():
    jobs = Job.query.all()
    return render_template('display.html', jobs=jobs)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # If already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # If form is valid
    if form.validate_on_submit():
        # Hash the entered password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create the user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Add the user to database
        db.session.add(user)
        # Commit your changes
        db.session.commit()
        flash(f'Your account has been created. You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # If already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists and his email and password match
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log that user in 
            login_user(user, remember=form.remember.data)
            # To go back to the required page. 
            # Use get because it doesn't give error if no arguement present.
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else: 
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# To save the updated picture
def save_picture(form_picture):
    # Create a random name for the picture
    random_hex = secrets.token_hex(8)
    # To split the picture name into name(discarded) and its extension 
    _, f_ext = os.path.splitext(form_picture.filename)
    # Concat the extension to the hex name
    picture_fn = random_hex + f_ext
    # Create the actual path where the picture should be stored
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # Declare the image size to be 125 px
    output_size = (125,125)
    # Open the image
    i = Image.open(form_picture)
    # Resize the image to the above mentioned size
    i.thumbnail(output_size)

    # Save the resized picture at that location
    i.save(picture_path)

    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        # If the picture is changed
        if form.picture.data:
            # Call the save function
            picture_file = save_picture(form.picture.data)
            # Update the picture in the database
            current_user.image_file = picture_file
        # Update the user's username in the database
        current_user.username = form.username.data
        # Update the user's email in the database
        current_user.email = form.email.data
        # Commit the changes
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))

    # The user's current username and email should appear in the form    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile',
                            image_file=image_file, form=form)


@app.route("/job/new", methods=['GET', 'POST'])
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        # Create new job
        job = Job(title=form.title.data, salary=form.salary.data, min_exp=form.min_exp.data)
        # Add job to database
        db.session.add(job)
        # Add the current user as the applicant to this job(is wrong logically. written just to check)
        job.applicants.append(current_user)
        # Commit the changes
        db.session.commit()
        flash('Your job has been created!', 'success')
        return redirect(url_for('display'))
    return render_template('create_job.html', title='New Job', form=form)