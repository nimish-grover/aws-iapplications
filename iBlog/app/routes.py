from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from app import db
from app.models import User, Post, Category, Tag
from app.forms import PostForm
from datetime import datetime
import re

main_bp = Blueprint('main', __name__)

# Helper function to generate slug
def generate_slug(title):
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower().strip()
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    return slug

# # Create a test user if needed (temporary for development)
# @main_bp.before_app_request
# def create_test_user():
#     if User.query.filter_by(username='admin').first() is None:
#         user = User(username='admin', email='admin@example.com', display_name='Admin', role='admin')
#         user.set_password('password')
#         db.session.add(user)
#         db.session.commit()
@main_bp.context_processor
def inject_now():
    return {'now': datetime.utcnow()}
# Home page - display all posts
@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(status='published').order_by(Post.published_at.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', posts=posts)

# Display a single post
@main_bp.route('/post/<string:slug>')
def show_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post)

# Create a new post
@main_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    
    if form.validate_on_submit():
        # For now, we'll use the admin user as the author
        author = User.query.filter_by(username='prashansa-sharma').first()
        
        post = Post(
            title=form.title.data,
            slug=form.slug.data or generate_slug(form.title.data),
            excerpt=form.excerpt.data,
            content=form.content.data,
            status=form.status.data,
            featured_image_url=form.featured_image_url.data,
            meta_title=form.meta_title.data,
            meta_description=form.meta_description.data,
            author=author
        )
        
        if form.status.data == 'published':
            post.published_at = datetime.utcnow()
            
        db.session.add(post)
        db.session.commit()
        
        flash('Post has been created successfully!', 'success')
        return redirect(url_for('main.show_post', slug=post.slug))
    
    return render_template('create_post.html', form=form, title='Create Post')

# Edit a post
@main_bp.route('/post/<string:slug>/edit', methods=['GET', 'POST'])
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        was_published = post.status == 'published'
        
        post.title = form.title.data
        post.slug = form.slug.data or generate_slug(form.title.data)
        post.excerpt = form.excerpt.data
        post.content = form.content.data
        post.status = form.status.data
        post.featured_image_url = form.featured_image_url.data
        post.meta_title = form.meta_title.data
        post.meta_description = form.meta_description.data
        
        # If post is being published for the first time
        if form.status.data == 'published' and not was_published:
            post.published_at = datetime.utcnow()
            
        db.session.commit()
        
        flash('Post has been updated successfully!', 'success')
        return redirect(url_for('main.show_post', slug=post.slug))
    
    return render_template('edit_post.html', form=form, post=post, title='Edit Post')

# Delete a post
@main_bp.route('/post/<string:slug>/delete', methods=['POST'])
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post has been deleted successfully!', 'success')
    return redirect(url_for('main.index'))