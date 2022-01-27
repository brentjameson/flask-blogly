"""Blogly application."""

from imp import get_tag
from optparse import Values
from turtle import update
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag

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
def show_user_details(user_id):
    """show info on a single user"""

    user = User.query.get_or_404(user_id)

    return render_template('user-details.html', user=user)


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
    user_delete = User.query.get_or_404(user_id)
    db.session.delete(user_delete)
    db.session.commit()

    flash(f'{user_delete.first_name} {user_delete.last_name} has been deleted.') 
    
    return redirect('/users')


@app.route ('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """asdffadj"""
    user = User.query.get_or_404(user_id)

    tags = Tag.query.all()
    return render_template('new-post.html', user=user, tags=tags)


@app.route ('/users/<int:user_id>/posts/new', methods = ['POST'])
def handle_new_post(user_id):
    """asff"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    print('************************')
    print(tags)
    print('************************')
    
    new_post = Post(title = request.form['post_title'],
    content = request.form['post_content'],
    user = user,
    tags=tags
    )

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route ('/posts/<int:post_id>')
def show_post(post_id):
    """asdffadj"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags

    return render_template('show-post.html', post = post, tags = tags)


@app.route ('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """asdffadj"""

    post= Post.query.get_or_404(post_id)

    post_tags = []

    not_post_tags = []

    for tag in post.tags:
        post_tags.append(tag)

    all_tags = Tag.query.all()
    for tag in all_tags:
        if tag not in post_tags:
            not_post_tags.append(tag)
            # print('************************')
            # print(tag.id)
            # print('************************')

    return render_template('edit-post.html', post = post, post_tags = post_tags, not_post_tags = not_post_tags)


@app.route ('/posts/<int:post_id>/edit', methods = ['POST'])
def handle_edit_post(post_id):
    """asff"""

    post = Post.query.get_or_404(post_id)

    post_title = request.form['edit_post_title']
    post_content = request.form['edit_post_content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]

    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post.tags = tags

    post.title = post_title
    post.content = post_content
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route ('/tags')
def show_all_tags():
    """asdffadj"""
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)


@app.route ('/tags/<int:tag_id>')
def tag_details(tag_id):
    """asdffadj"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-details.html', tag = tag)


@app.route ('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """asdffadj"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit-tag.html', tag = tag)


@app.route ('/tags/<int:tag_id>/edit', methods = ['POST'])
def handle_tag_edit(tag_id):
    """asdffadj"""
    tag = Tag.query.get_or_404(tag_id)

    tag_edit = request.form['edit_tag_name']

    tag.name = tag_edit

    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')


@app.route ('/tags/<int:tag_id>/delete')
def show_delete_tag_form(tag_id):
    """asdffadj"""
    tag_delete = Tag.query.get_or_404(tag_id)
    db.session.delete(tag_delete)
    db.session.commit()

    flash(f'"{tag_delete.name}" tag has been deleted.') 
    
    return redirect('/tags')


@app.route ('/tags/new')
def create_tag_form():
    """asdffadj"""

    return render_template('create-new-tag.html')


@app.route ('/tags/new', methods = ['POST'])
def handle_new_tag():
    """asff"""

    tag_name = request.form['tag_name']
    
    tag = Tag(name = tag_name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')
