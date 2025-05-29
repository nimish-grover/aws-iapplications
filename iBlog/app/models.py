from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    display_name = db.Column(db.String(64))
    bio = db.Column(db.Text)
    role = db.Column(db.Enum('admin', 'editor', 'author', 'subscriber', name='user_roles'))
    avatar_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    uploads = db.relationship('Media', backref='uploader', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    slug = db.Column(db.String(256), unique=True, nullable=False)
    status = db.Column(db.Enum('draft', 'published', 'private', 'trash', name='post_status'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    featured_image_url = db.Column(db.String(256))
    meta_title = db.Column(db.String(256))
    meta_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    categories = db.relationship('Category', secondary='post_categories', backref=db.backref('posts', lazy='dynamic'))
    tags = db.relationship('Tag', secondary='post_tags', backref=db.backref('posts', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Media(db.Model):
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    file_path = db.Column(db.String(256), nullable=False)
    original_name = db.Column(db.String(256))
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(128))
    media_type = db.Column(db.Enum('image', 'video', 'document', 'table', 'report', name='media_types'))
    alt_text = db.Column(db.Text)
    caption = db.Column(db.Text)
    media = db.Column(db.JSON)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Media {self.filename}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(120))
    author_url = db.Column(db.String(256))
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('approved', 'pending', 'spam', 'trash', name='comment_status'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]))
    
    def __repr__(self):
        return f'<Comment {self.id}>'

# Association tables for many-to-many relationships
post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)