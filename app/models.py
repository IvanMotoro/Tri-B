import sqlalchemy as sa
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class UserMed(db.Model, UserMixin):
    __tablename__ = 'users_med'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    gender = db.Column(db.String(10), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())

    role = db.relationship('Role')
    post = db.relationship('Post')

    def __repr__(self):
        return '<UserMed %r>' % self.login

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

class UserPat(db.Model, UserMixin):
    __tablename__ = 'users_pat'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    gender = db.Column(db.String(10), nullable=False)
    data_day = db.Column(db.Integer, nullable=False)
    data_month = db.Column(db.Integer, nullable=False)
    data_year = db.Column(db.Integer, nullable=False)
    home_address = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<UserPat %r>' % self.full_name

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])
    
    @property
    def birth_date(self):
        return '.'.join([self.data_day, self.data_month, self.data_year])

class MedPatient(db.Model):
    __tablename__ = 'med_patient'

    med_id = db.Column(db.Integer, db.ForeignKey('users_med.id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users_pat.id'), primary_key=True)

    med = db.relationship('UserMed')
    patient = db.relationship('UserPat')

    def __repr__(self):
        return '<MedPatient %r>' % self.med_id + self.patient_id

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.name

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.name

class Temp(db.Model):
    __tablename__ = 'temps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Temp %r>' % self.name
