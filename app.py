"""Blogly application."""

from optparse import Values
from turtle import update
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

# from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import update

@app.route ('/', methods = ['GET'])
def redirect_to_users():
    """List Users"""
    return redirect(f"/users")

@app.route ('/users', methods = ['GET'])
def list_users():
    """List Users"""
    users = User.query.all();
    return render_template('user_list.html', users = users)


@app.route ('/users/new', methods = ['GET'])
def get_new_user_form():
    """List Users"""
    return render_template('new-user-form.html')


@app.route ('/', methods = ['POST'])
def add_user():
    """Add User"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name = first_name, last_name = last_name, image_url  = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route ('/users/<int:user_id>')
def show_user(user_id):
    """show info on a single user"""

    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user)


@app.route ('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Allow user to edit user info"""
    user = User.query.get_or_404(user_id)

    return render_template('edit-user.html', user = user)


@app.route ('/users/<int:user_id>/edit', methods = ['POST'] )
def post_user_edit(user_id):
    """updates database and shows user information edit"""
    first_name = request.form['edit_first_name']
    last_name = request.form['edit_last_name']
    image_url = request.form['edit_image_url']

    User.query.filter_by(id = user_id).update(dict(first_name = first_name, last_name = last_name, image_url  = image_url))
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route ('/users/<int:user_id>/delete', methods = ['POST'] )
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    User.query.filter_by(id = user_id).delete()
    db.session.commit()

    flash(f'{user.first_name} {user.last_name} has been deleted as a User') 
    
    return redirect('/')


@app.route ('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """asdffadj"""

    user = User.query.get_or_404(user_id)
    return render_template('new-post.html', user=user)


@app.route ('/users/<int:user_id>/posts/new', methods = ['POST'])
def handle_new_post(user_id):
    """asff"""

    # user = User.query.get_or_404(user_id)
    post_title = request.form['post_title']
    post_content = request.form['post_content']

    post = Post(title = post_title, content = post_content, user_id = user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route ('/posts/<int:post_id>')
def show_post(post_id):
    """asdffadj"""

    post = Post.query.get_or_404(post_id)

    return render_template('show-post.html', post = post)








@app.route ('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """asdffadj"""

    post= Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post = post)


@app.route ('/posts/<int:post_id>/edit', methods = ['POST'])
def handle_edit_post(post_id):
    """asff"""

    post = Post.query.get_or_404(post_id)

    post_title = request.form['edit_post_title']
    post_content = request.form['edit_post_content']

    post.title = post_title
    post.content = post_content
    db.session.commit()

    return redirect(f"/posts/{post_id}")