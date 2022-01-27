"""Models for Blogly."""
# from time import timezone
# from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import backref
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    image_url = db.Column(db.String)

    posts = db.relationship(
        'Post',
        backref= 'user',
        cascade="all, delete-orphan"
    )
        


class Post(db.Model):
    """POSTS"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.String, nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.datetime.now
        )

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)

    # tags = db.relationship(
    #     'Tag', 
    #     secondary = 'post_tags',
    #     cascade='all,delete',
    #     backref = 'posts')


class Tag(db.Model):
    """ads;fjkda"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)

    name = db.Column(db.String(50), nullable=False)

    posts = db.relationship(
        'Post', 
        secondary = 'post_tags',
        cascade='all,delete',
        backref = 'tags',
        )


class PostTag(db.Model):
    """ads;fjkda"""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)



