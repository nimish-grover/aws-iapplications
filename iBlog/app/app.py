from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify
from datetime import datetime
import os
import uuid
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://db_master:w24JyTn0SIEHfS@144.24.103.183:5432/flask_blog')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name or self.username,
            'avatar_url': self.avatar_url,
            'bio': self.bio
        }

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='draft')
    view_count = db.Column(db.Integer, default=0)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    categories = db.relationship('Category', secondary='post_categories', backref=db.backref('posts', lazy=True))
    tags = db.relationship('Tag', secondary='post_tags', backref=db.backref('posts', lazy=True))
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def generate_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        count = 1
        
        while Post.query.filter_by(slug=slug).first() is not None:
            slug = f"{base_slug}-{count}"
            count += 1
            
        return slug
    
    def publish(self):
        self.status = 'published'
        self.published_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'excerpt': self.excerpt,
            'featured_image': self.featured_image,
            'author': self.author.to_dict() if self.author else None,
            'status': self.status,
            'view_count': self.view_count,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'categories': [c.to_dict() for c in self.categories],
            'tags': [t.to_dict() for t in self.tags],
            'comment_count': len(self.comments)
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description
        }

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }

# Association tables
post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_name = db.Column(db.String(100))
    author_email = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author_name': self.author_name or (self.user.display_name if self.user else None),
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat(),
            'has_replies': len(self.replies) > 0,
            'replies': [reply.to_dict() for reply in self.replies if reply.is_approved]
        }

# Helper functions for text processing
def extract_text_from_html(html_content, max_length=200):
    """Extract plain text from HTML content for excerpts"""
    import re
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', html_content)
    # Clean up whitespace
    text = ' '.join(text.split())
    # Truncate if needed
    if len(text) > max_length:
        text = text[:max_length] + '...'
    return text

# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('index'))
            
        return f(*args, **kwargs)
    return decorated_function

# Request hooks
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# Routes
@app.route('/')
def index():
    """Home page displaying all blog posts"""
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # Get published posts
    posts_query = Post.query.filter_by(status='published').order_by(Post.published_at.desc())
    
    # Paginate results
    pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items
    
    return render_template('index.html', 
                          posts=posts, 
                          pagination=pagination)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/post/<slug>')
def post_detail(slug):
    """Display a single blog post"""
    post = Post.query.filter_by(slug=slug, status='published').first_or_404()
    
    # Increment view count
    post.view_count += 1
    db.session.commit()
    
    # Get approved comments
    comments = Comment.query.filter_by(post_id=post.id, is_approved=True, parent_id=None).all()
    
    return render_template('post_detail.html', post=post, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
                
            flash('You have been logged in successfully', 'success')
            return redirect(next_page)
        
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        error = None
        
        if not username:
            error = 'Username is required'
        elif not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required'
        elif password != confirm_password:
            error = 'Passwords do not match'
        elif User.query.filter_by(username=username).first() is not None:
            error = 'Username is already taken'
        elif User.query.filter_by(email=email).first() is not None:
            error = 'Email is already registered'
            
        if error is None:
            user = User(username=username, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in', 'success')
            return redirect(url_for('login'))
        
        flash(error, 'danger')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_posts = Post.query.filter_by(author_id=g.user.id).order_by(Post.created_at.desc()).all()
    return render_template('dashboard.html', posts=user_posts)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new blog post"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        status = request.form.get('status', 'draft')
        category_ids = request.form.getlist('categories')
        tag_names = request.form.get('tags', '').split(',') if request.form.get('tags') else []
        
        # Validate input
        if not title or not content:
            flash('Please fill in the title and content fields', 'danger')
            categories = Category.query.all()
            tags = Tag.query.all()
            return render_template('create_post.html', categories=categories, tags=tags)
        
        # Create new post
        post = Post(
            title=title,
            content=content,
            excerpt=excerpt or extract_text_from_html(content),
            author_id=g.user.id,
            status=status
        )
        
        # Generate slug
        post.slug = post.generate_slug()
        
        # Set published_at if status is published
        if status == 'published':
            post.published_at = datetime.utcnow()
        
        # Add categories
        if category_ids:
            categories = Category.query.filter(Category.id.in_(category_ids)).all()
            post.categories = categories
        
        # Add tags
        if tag_names:
            # Clean up tags
            tag_names = [tag.strip() for tag in tag_names if tag.strip()]
            
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                
                if not tag:
                    # Create new tag
                    tag = Tag(name=tag_name, slug=slugify(tag_name))
                    db.session.add(tag)
                
                post.tags.append(tag)
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # Get all categories and tags for the form
    categories = Category.query.all()
    tags = Tag.query.all()
    
    return render_template('create_post.html', categories=categories, tags=tags)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit an existing blog post"""
    post = Post.query.get_or_404(post_id)
    
    # Check if the current user is the author
    if post.author_id != g.user.id and not g.user.is_admin:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        status = request.form.get('status', 'draft')
        category_ids = request.form.getlist('categories')
        tag_names = request.form.get('tags', '').split(',') if request.form.get('tags') else []
        
        # Validate input
        if not title or not content:
            flash('Please fill in the title and content fields', 'danger')
            categories = Category.query.all()
            tags = Tag.query.all()
            return render_template('edit_post.html', post=post, categories=categories, tags=tags)
        
        # Update post
        post.title = title
        post.content = content
        post.excerpt = excerpt or extract_text_from_html(content)
        
        # Update status and published_at if needed
        if status == 'published' and post.status != 'published':
            post.status = status
            post.published_at = datetime.utcnow()
        else:
            post.status = status
        
        # Update categories
        if category_ids:
            categories = Category.query.filter(Category.id.in_(category_ids)).all()
            post.categories = categories
        else:
            post.categories = []
        
        # Update tags
        post.tags = []
        if tag_names:
            # Clean up tags
            tag_names = [tag.strip() for tag in tag_names if tag.strip()]
            
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                
                if not tag:
                    # Create new tag
                    tag = Tag(name=tag_name, slug=slugify(tag_name))
                    db.session.add(tag)
                
                post.tags.append(tag)
        
        db.session.commit()
        
        flash('Post updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # Get all categories and tags for the form
    categories = Category.query.all()
    tags = Tag.query.all()
    
    # Get post tags as comma-separated string
    post_tags = ','.join([tag.name for tag in post.tags])
    
    return render_template('edit_post.html', post=post, categories=categories, tags=tags, post_tags=post_tags)

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a blog post"""
    post = Post.query.get_or_404(post_id)
    
    # Check if the current user is the author
    if post.author_id != g.user.id and not g.user.is_admin:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/category/<slug>')
def category_posts(slug):
    """Display posts in a specific category"""
    category = Category.query.filter_by(slug=slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # Get published posts in this category
    posts_query = Post.query.filter_by(status='published').filter(Post.categories.contains(category)).order_by(Post.published_at.desc())
    
    # Paginate results
    pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items
    
    return render_template('category_posts.html', 
                          category=category,
                          posts=posts, 
                          pagination=pagination)

@app.route('/tag/<slug>')
def tag_posts(slug):
    """Display posts with a specific tag"""
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # Get published posts with this tag
    posts_query = Post.query.filter_by(status='published').filter(Post.tags.contains(tag)).order_by(Post.published_at.desc())
    
    # Paginate results
    pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items
    
    return render_template('tag_posts.html', 
                          tag=tag,
                          posts=posts, 
                          pagination=pagination)

@app.route('/post/<slug>/comment', methods=['POST'])
def add_comment(slug):
    """Add a comment to a post"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    content = request.form.get('content')
    parent_id = request.form.get('parent_id')
    
    if not content:
        flash('Comment cannot be empty', 'danger')
        return redirect(url_for('post_detail', slug=slug))
    
    # Create comment
    comment = Comment(
        post_id=post.id,
        content=content,
        parent_id=parent_id if parent_id else None
    )
    
    # Set author information
    if g.user:
        comment.author_id = g.user.id
        comment.is_approved = True  # Auto-approve for logged-in users
    else:
        comment.author_name = request.form.get('author_name')
        comment.author_email = request.form.get('author_email')
        comment.is_approved = False  # Require approval for guest comments
    
    db.session.add(comment)
    db.session.commit()
    
    if comment.is_approved:
        flash('Your comment has been added successfully', 'success')
    else:
        flash('Your comment has been submitted and is awaiting approval', 'info')
    
    return redirect(url_for('post_detail', slug=slug))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    return render_template('admin/dashboard.html')

@app.route('/admin/posts')
@admin_required
def admin_posts():
    """Admin posts management"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@app.route('/admin/comments')
@admin_required
def admin_comments():
    """Admin comments management"""
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin/comments.html', comments=comments)

@app.route('/admin/approve-comment/<int:comment_id>', methods=['POST'])
@admin_required
def approve_comment(comment_id):
    """Approve a comment"""
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    
    flash('Comment approved successfully', 'success')
    return redirect(url_for('admin_comments'))

@app.route('/admin/delete-comment/<int:comment_id>', methods=['POST'])
@admin_required
def delete_comment(comment_id):
    """Delete a comment"""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    
    flash('Comment deleted successfully', 'success')
    return redirect(url_for('admin_comments'))

@app.route('/admin/categories')
@admin_required
def admin_categories():
    """Admin categories management"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/add-category', methods=['POST'])
@admin_required
def add_category():
    """Add a new category"""
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        flash('Category name is required', 'danger')
        return redirect(url_for('admin_categories'))
    
    # Create category
    category = Category(
        name=name,
        slug=slugify(name),
        description=description
    )
    
    db.session.add(category)
    db.session.commit()
    
    flash('Category added successfully', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/edit-category/<int:category_id>', methods=['POST'])
@admin_required
def edit_category(category_id):
    """Edit a category"""
    category = Category.query.get_or_404(category_id)
    
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        flash('Category name is required', 'danger')
        return redirect(url_for('admin_categories'))
    
    # Update category
    category.name = name
    category.slug = slugify(name)
    category.description = description
    
    db.session.commit()
    
    flash('Category updated successfully', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/delete-category/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    """Delete a category"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted successfully', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/tags')
@admin_required
def admin_tags():
    """Admin tags management"""
    tags = Tag.query.all()
    return render_template('admin/tags.html', tags=tags)

@app.route('/admin/delete-tag/<int:tag_id>', methods=['POST'])
@admin_required
def delete_tag(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    
    flash('Tag deleted successfully', 'success')
    return redirect(url_for('admin_tags'))

@app.route('/search')
def search():
    """Search for posts"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # Search in title and content
    posts_query = Post.query.filter(
        Post.status == 'published',
        db.or_(
            Post.title.ilike(f'%{query}%'),
            Post.content.ilike(f'%{query}%')
        )
    ).order_by(Post.published_at.desc())
    
    # Paginate results
    pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items
    
    return render_template('search.html', 
                          query=query,
                          posts=posts, 
                          pagination=pagination)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize database tables
@app.cli.command('init-db')
def init_db():
    """Create database tables"""
    db.create_all()
    
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin_password')  # Change this in production!
        db.session.add(admin)
    
    # Create default categories
    for name in ['General', 'Technology', 'Travel', 'Food', 'Health']:
        if not Category.query.filter_by(name=name).first():
            category = Category(name=name, slug=slugify(name))
            db.session.add(category)
    
    db.session.commit()
    print('Database initialized successfully')

if __name__ == '__main__':
    app.run(debug=True)