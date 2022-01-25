"""Models for Blogly."""
# from time import timezone
# from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy
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

    the_user = db.relationship('User', backref = 'posts')