from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    username=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(160),unique=True)
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    posts=db.relationship('Post',backref='user',passive_deletes=True)
    comments=db.relationship('Comments',backref='user',passive_deletes=True)
    likes=db.relationship('Likes',backref='user',passive_deletes=True)
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    post_text=db.Column(db.String(256),nullable=False)
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    author=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    comments=db.relationship('Comments',backref='post',passive_deletes=True)
    likes=db.relationship('Likes',backref='post',passive_deletes=True)
class Comments(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    cm_text=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    author=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id',ondelete="CASCADE"),nullable=False) 

class Likes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    author=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id',ondelete="CASCADE"),nullable=False) 
    