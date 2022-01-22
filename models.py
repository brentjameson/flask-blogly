"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

    # def edit_user_info(self):
        # Edit user information
        # return User.query.filter_by(id = self.id).update(dict(first_name = self.first_name, last_name = self.last_name, image_url = self.image_url))
        #  db.session.add(user)
        #  db.session.commit()
