import json
import os
import secrets

import mysql.connector
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image
from flask import render_template, url_for, flash, redirect, request,session
from recruiter import app#, db, bcrypt
from recruiter.forms import ApplicantRegistrationForm, LoginForm, UpdateProfileForm, JobForm,CompanyRegistrationForm
# from recruiter.models import User, Job
# from flask_login import login_user, current_user, logout_user, login_required
import mysql.connector,json

@app.route("/")
@app.route("/home")
def home():
    current_user = None
    if ('username' in session and session['username']!=None):
        current_user = session['username']
    if ('company' in session and session['company']!=None):
        current_user = session['company']
    return render_template('home.html',current_user=current_user)

# @app.route("/display")
# def display():
#     jobs = Job.query.all()
#     return render_template('display.html', jobs=jobs)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/applicant", methods=['GET', 'POST'])
def register():
    # If already logged in
    current_user = None
    if ('username' in session and session['username']!=None):
        current_user = session['username']
        return render_template('home.html',current_user=current_user)
    elif ('company' in session and session['company']!=None):
        current_user = session['company']
        return render_template('home.html',current_user=current_user)
    else:
        if request.method == 'POST':
            form = ApplicantRegistrationForm()
            if form.validate_on_submit():
                cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
                cur = cnx.cursor(buffered=True)
                username = form.username.data
                email = form.email.data
                name = form.name.data
                password = form.password.data
                if form.gender.data:
                    gender = form.gender.data
                else:
                    gender = ''
                try:
                    import datetime
                    x = str(datetime.datetime.now())
                    cur.execute("insert into applicants values(%s,%s,%s,aes_encrypt(%s,'key'),%s,%s,'');",(x,username,email,password,name,gender))
                    cnx.commit()
                    cur.close()
                    cnx.close()
                    print("yess")
                    flash(f'Your account has been created . You can now login.', 'success')
                    return redirect(url_for('home'))
                except Exception as e:
                    print('Registration Failed',e)
                    flash(f'An error occured while registering.Please try again.', 'error')
                cnx.commit()
                cur.close()
                cnx.close()
                return redirect(url_for('register'))
        form = ApplicantRegistrationForm()
        return render_template('register.html' ,title='Register', form=form)


@app.route("/company", methods=['GET', 'POST'])
def registercomp():
    # session['type'] = usertype
    if ('username' in session and session['username']!=None):
        current_user = session['username']
        return render_template('home.html',current_user=current_user)
    elif ('company' in session and session['company']!=None):
        current_user = session['company']
        return render_template('home.html',current_user=current_user)
    else:
        if request.method == 'POST':
            print("post")
            form = CompanyRegistrationForm()
            if form.validate_on_submit():
                print("hmm")
                cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
                cur = cnx.cursor(buffered=True)
                name = form.name.data
                location = form.location.data
                email = form.email.data
                password = form.password.data
                c_type = form.c_type.data
                try:
                    import datetime
                    x = str(datetime.datetime.now())
                    cur.execute("insert into company values(%s,%s,%s,aes_encrypt(%s,'key'),%s,%s);",(x,name,email,password,location,c_type))
                    cnx.commit()
                    cur.close()
                    cnx.close()
                    print("yess")
                    flash(f'Your account has been created . You can now login.', 'success')
                    return redirect(url_for('home'))
                except Exception as e:
                    print('Registration Failed',e)
                    flash(f'An error occured while registering.Please try again.', 'error')
                cnx.commit()
                cur.close()
                cnx.close()
                return redirect(url_for('registercomp'))
        print(form.errors)
        form = CompanyRegistrationForm()
        return render_template('register_company.html' ,title='Register', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    # If already logged in
    if ('username' in session and session['username']!=None):
        current_user = session['username']
        return render_template('home.html',current_user=current_user)
    elif ('company' in session and session['company']!=None):
        current_user = session['company']
        return render_template('home.html',current_user=current_user)
    # form = LoginForm()
    # if form.validate_on_submit():
    cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
    cur = cnx.cursor(buffered=True)
    cur.execute("select * from applicants where email=%s and password=aes_encrypt(%s,'key');",(request.form['email'],request.form['password']))
    user = cur.fetchone()
    cur.execute("select * from company where email=%s and password=aes_encrypt(%s,'key');",(request.form['email'],request.form['password']))
    company = cur.fetchone()
    print(user)
        # Check if user exists and his email and password match
    if user:
        # Log that user in 
        session['username'] = user[1]
        # To go back to the required page. 
        # Use get because it doesn't give error if no arguement present.
        next_page = request.args.get('next')
        cnx.commit()
        cur.close()
        cnx.close()
        if next_page:
            return redirect(next_page)
        else: 
            return redirect(url_for('home'))
    elif company:
        # Log that user in 
        session['company'] = company[1]
        # To go back to the required page. 
        # Use get because it doesn't give error if no arguement present.
        next_page = request.args.get('next')
        cnx.commit()
        cur.close()
        cnx.close()
        if next_page:
            return redirect(next_page)
        else: 
            return redirect(url_for('home'))
    else:
        cnx.commit()
        cur.close()
        cnx.close()
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('home.html')


@app.route("/logout")
def logout():
    session['username'] = None
    session['company'] = None
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
    print(picture_path)
    # Declare the image size to be 125 px
    output_size = (125,125)
    # Open the image
    i = Image.open(form_picture)
    # Resize the image to the above mentioned size
    i.thumbnail(output_size)

    # Save the resized picture at that location
    i.save(picture_path)

    return picture_fn

@app.route("/profile/update/", methods=['GET', 'POST'])
def updateprofile():
    # If user is logged in then continue
    if 'username' in session and session['username']!=None:
        form = UpdateProfileForm()
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor(buffered=True)
        cur.execute("select * from applicants where username=%s;",(session['username'],))
        user = cur.fetchone()
        print(user)
        if request.method =="POST":
            print("hfvnusi")
            if form.validate_on_submit():
                print("in validate")
            # If the picture is changed
                if form.picture.data:
                    os.remove(url_for('static', filename='profile_pics/' + user[6]))
                    picture_file = save_picture(form.picture.data)
                else:
                    picture_file = user[6]
                # Update the table
                cur.execute("update applicants set name=%s,username=%s,gender=%s,image_file=%s where a_id=%s",(form.name.data,form.username.data,form.gender.data,picture_file,user[0]))
                # Commit the changes
                cnx.commit()
                # Also update the session variable since it was changed
                session['username'] = form.username.data
                cur.close()
                cnx.close()
                flash('Your profile has been updated!', 'success')
                return redirect(url_for('profile'))
            else:
                print(form.errors)

       # When clicked on update form then populate the form with original values     
        elif request.method == 'GET':
            print("wrong")
            form.username.data = user[1]
            form.name.data = user[4]
            form.gender.data = user[5]
        image_file = url_for('static', filename='profile_pics/' + user[6])
        return render_template('update_profile.html', title='Profile',
                                    image_file=image_file, form=form,username=user[1],current_user=session['username'])
    
    # Not logged in then redirect to login
    else:
        return redirect(url_for('login'))


@app.route("/addskill/", methods=['GET','POST'])
def addskill():
    # Get the name of the skill to be added
    skill = request.form['AddaSkill']
    cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
    cur = cnx.cursor(buffered=True)
    cur.execute("select * from applicants where username=%s;",(session['username'],))
    user = cur.fetchone()
    cur.execute("insert into applicant_skill values(%s,%s);",(user[0],skill))
    cnx.commit()
    cur.close()
    cnx.close()
    return redirect(url_for('profile'))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' in session and session['username']!=None:
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor(buffered=True)
        if request.method == "POST":
            # company=request.POST['company']
            # title=request.POST['title']
            # fromdate=request.POST['fromdate']
            # todate=request.POST['todate']
            # cur.execute("insert into applicant_job values(%s,%s,%s,%s)",(company,title,fromdate,todate))
            # cnx.commit()
            # cur.close()
            # cnx.close()
            return redirect(url_for('profile'))
        else:
            cur.execute("select * from applicants where username=%s;",(session['username'],))
            user = cur.fetchone()
            image_file = url_for('static', filename='profile_pics/' + str(user[6]))
            cur.execute("select skill from applicant_skill where a_id = %s;",(user[0],))
            skills = cur.fetchall()
            w,x,y,z=[],[],[],[]
            for i in skills:
                x.append(i[0])
            cur.execute("select a_id,name,title,j_status from company inner join job inner join applied_job on job.j_id=applied_job.j_id and company.c_id=job.c_id ")
            jobs = cur.fetchall()
            for i in jobs:
                if i[0] ==user[0]:
                    y.append(i[1])
                    z.append(i[2])
                    w.append(i[3])
            appliedjobs=zip(y,z,w)
            cur.execute("select company,title,fromdate,todate from applicant_job where a_id=%s",(user[0],))
            jobs = cur.fetchall()
            w,q,y,z=[],[],[],[]
            for i in jobs:
                y.append(i[0])
                z.append(i[1])
                w.append(i[2])
                q.append(i[3])
            myjobs = zip(y,z,w,q)
            cnx.commit()
            cur.close()
            cnx.close()
            return render_template('profile.html', title='Profile',current_user = user[1],appliedjobs=appliedjobs,
                                    image_file=image_file,username=user[1],email=user[2],skills=x,myjobs=myjobs)
    else:
        return redirect(url_for('login'))

@app.route("/company/profile", methods=['GET', 'POST'])
def company():
    if session['company']:
        cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
        cur = cnx.cursor(buffered=True)
        cur.execute('select * from company where c_id=%s',(session['company'],))
        company = cur.fetchone()
        print(company)
        # company_logo = url_for('static', filename='profile_pics/' + str(company[6]))
        cur.execute('select * from job where c_id=%s',(company[0],))
        jobs = cur.fetchall()
        print(jobs)
        return render_template('company_profile.html',company=company,jobs=jobs)
    

    
@app.route("/job/new", methods=['GET', 'POST'])
def new_job():
    if 'company' in session and session['company']!='':
        form = JobForm()
        if form.validate_on_submit():
            # Create new job
            import datetime
            j_id = str(datetime.datetime.now())
            title = form.title.data
            salary = form.salary.data
            min_exp = form.min_exp.data
            c_id = session['company']
            cnx = mysql.connector.connect(host='localhost',user='root', database='recruiter')
            cur = cnx.cursor(buffered=True)
            cur.execute("insert into job values(%s,%s,%s,%s,%s);",(j_id,title,salary,min_exp,c_id))
            cnx.commit()
            cur.close()
            cnx.close()
            # Add job to database
            # Add the current user as the applicant to this job(is wrong logically. written just to check)
            # Commit the changes
            flash('Your job has been created!', 'success')
            return redirect(url_for('display'))
        return render_template('create_job.html', title='New Job', form=form)
    else:
        return redirect(url_for('login'))
