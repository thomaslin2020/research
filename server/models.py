from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from server.app import db


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Library(db.Model):
    __tablename__ = 'library'
    lib_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paper_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.DateTime)
