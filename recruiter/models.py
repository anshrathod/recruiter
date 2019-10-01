
# from recruiter import db, login_manager
# from flask_login import UserMixin

# # Required to proceed
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# applied = db.Table('applied',
#         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#         db.Column('job_id', db.Integer, db.ForeignKey('job.id')),        
#     )

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     applied_for = db.relationship('Job', secondary=applied, backref=db.backref('applicants', lazy=True))


#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# class Job(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50), nullable=False)
#     salary = db.Column(db.String(30), nullable=False)
#     min_exp = db.Column(db.String(20), nullable=False)    

#     def __repr__(self):
#         return f"User('{self.title}', '{self.salary}', '{self.min_exp}')"
