from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os
from datetime import datetime
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# WordPress configuration
WORDPRESS_URL = 'https://flaskdev.wordpress.com/'
WORDPRESS_USERNAME = 'sharmaprashansa57'
WORDPRESS_PASSWORD = '67c5qrnxbksygwrz'

class WordPressClient:
    def __init__(self, site_url, username=None, password=None):
        self.site_url = site_url.rstrip('/')
        self.api_url = f"https://public-api.wordpress.com/wp/v2/sites/flaskdev.wordpress.com"

        self.username = username
        self.password = password
        self.auth_header = self._get_auth_header() if username and password else None
    
    def _get_auth_header(self):
        """Create basic auth header for WordPress API"""
        credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        return {'Authorization': f'Basic {credentials}'}
    
    def get_posts(self, page=1, per_page=10, status='publish'):
        """Fetch blog posts from WordPress"""
        try:
            url = f"{self.api_url}/posts"
            params = {
                'page': page,
                'per_page': per_page,
                'status': status,
                '_embed': True  # Include featured images and author info
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            posts = response.json()
            total_pages = int(response.headers.get('X-WP-TotalPages', 1))
            total_posts = int(response.headers.get('X-WP-Total', 0))
            
            return {
                'posts': posts,
                'total_pages': total_pages,
                'total_posts': total_posts,
                'current_page': page
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching posts: {e}")
            return None
    
    def get_post(self, post_id):
        """Fetch a single blog post by ID"""
        try:
            url = f"{self.api_url}/posts/{post_id}"
            params = {'_embed': True}
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching post: {e}")
            return None
    
    def get_post_by_slug(self, slug):
        """Fetch a single blog post by slug"""
        try:
            url = f"{self.api_url}/posts"
            params = {'slug': slug, '_embed': True}
            response = requests.get(url, params=params)
            response.raise_for_status()
            posts = response.json()
            return posts[0] if posts else None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching post: {e}")
            return None
    
    def create_post(self, title, content, excerpt=None, status='draft', tags=None, categories=None):
        """Create a new blog post (requires authentication)"""
        if not self.auth_header:
            return {'error': 'Authentication required for creating posts'}
        
        try:
            url = f"{self.api_url}/posts"
            
            data = {
                'title': title,
                'content': content,
                'status': status,
                'excerpt': excerpt or '',
            }
            
            # Add tags if provided
            if tags:
                tag_ids = self._get_or_create_tags(tags)
                if tag_ids:
                    data['tags'] = tag_ids
            
            # Add categories if provided
            if categories:
                category_ids = self._get_or_create_categories(categories)
                if category_ids:
                    data['categories'] = category_ids
            
            headers = {
                'Content-Type': 'application/json',
                **self.auth_header
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating post: {e}")
            return {'error': str(e)}
    
    def _get_or_create_tags(self, tag_names):
        """Get or create tags and return their IDs"""
        tag_ids = []
        for tag_name in tag_names:
            try:
                # First, try to find existing tag
                url = f"{self.api_url}/tags"
                params = {'search': tag_name.strip()}
                response = requests.get(url, params=params)
                tags = response.json()
                
                if tags:
                    tag_ids.append(tags[0]['id'])
                else:
                    # Create new tag
                    create_url = f"{self.api_url}/tags"
                    tag_data = {'name': tag_name.strip()}
                    headers = {
                        'Content-Type': 'application/json',
                        **self.auth_header
                    }
                    create_response = requests.post(create_url, json=tag_data, headers=headers)
                    if create_response.status_code == 201:
                        new_tag = create_response.json()
                        tag_ids.append(new_tag['id'])
            except Exception as e:
                print(f"Error handling tag '{tag_name}': {e}")
                continue
        
        return tag_ids
    
    def _get_or_create_categories(self, category_names):
        """Get or create categories and return their IDs"""
        category_ids = []
        for category_name in category_names:
            try:
                # First, try to find existing category
                url = f"{self.api_url}/categories"
                params = {'search': category_name.strip()}
                response = requests.get(url, params=params)
                categories = response.json()
                
                if categories:
                    category_ids.append(categories[0]['id'])
                else:
                    # Create new category
                    create_url = f"{self.api_url}/categories"
                    category_data = {'name': category_name.strip()}
                    headers = {
                        'Content-Type': 'application/json',
                        **self.auth_header
                    }
                    create_response = requests.post(create_url, json=category_data, headers=headers)
                    if create_response.status_code == 201:
                        new_category = create_response.json()
                        category_ids.append(new_category['id'])
            except Exception as e:
                print(f"Error handling category '{category_name}': {e}")
                continue
        
        return category_ids
    
    def get_categories(self):
        """Get all categories"""
        try:
            url = f"{self.api_url}/categories"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching categories: {e}")
            return []
    
    def get_tags(self):
        """Get all tags"""
        try:
            url = f"{self.api_url}/tags"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tags: {e}")
            return []

# Initialize WordPress client
wp_client = WordPressClient(WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD)

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

@app.route('/')
def index():
    """Home page displaying all blog posts"""
    page = request.args.get('page', 1, type=int)
    result = wp_client.get_posts(page=page, per_page=5)
    
    if result:
        posts = result['posts']
        total_pages = result['total_pages']
        current_page = result['current_page']
        
        # Process posts to add excerpt if missing
        for post in posts:
            if not post.get('excerpt', {}).get('rendered'):
                post['excerpt'] = {
                    'rendered': extract_text_from_html(post.get('content', {}).get('rendered', ''))
                }
    else:
        posts = []
        total_pages = 1
        current_page = 1
        flash('Error loading posts. Please check your WordPress configuration.', 'error')
    
    return render_template('index.html', 
                         posts=posts, 
                         total_pages=total_pages, 
                         current_page=current_page)

@app.route('/post/<slug>')
def post_detail(slug):
    """Display a single blog post"""
    post = wp_client.get_post_by_slug(slug)
    
    if post:
        return render_template('post_detail.html', post=post)
    
    flash('Post not found', 'error')
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """Create a new blog post"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        status = request.form.get('status', 'draft')
        tags = request.form.get('tags', '').split(',') if request.form.get('tags') else []
        categories = request.form.get('categories', '').split(',') if request.form.get('categories') else []
        
        # Clean up tags and categories
        tags = [tag.strip() for tag in tags if tag.strip()]
        categories = [cat.strip() for cat in categories if cat.strip()]
        
        if title and content:
            result = wp_client.create_post(
                title=title,
                content=content,
                excerpt=excerpt,
                status=status,
                tags=tags,
                categories=categories
            )
            
            if 'error' not in result:
                flash('Post created successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash(f'Error creating post: {result.get("error", "Unknown error")}', 'error')
        else:
            flash('Please fill in the title and content fields', 'error')
    
    # Get existing categories and tags for the form
    categories = wp_client.get_categories()
    tags = wp_client.get_tags()
    
    return render_template('create_post.html', categories=categories, tags=tags)

@app.route('/create1', methods=['GET', 'POST'])
def create_post_1():
    """Create a new blog post"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        status = request.form.get('status', 'draft')
        tags = request.form.get('tags', '').split(',') if request.form.get('tags') else []
        categories = request.form.get('categories', '').split(',') if request.form.get('categories') else []
        
        # Clean up tags and categories
        tags = [tag.strip() for tag in tags if tag.strip()]
        categories = [cat.strip() for cat in categories if cat.strip()]
        
        if title and content:
            result = wp_client.create_post(
                title=title,
                content=content,
                excerpt=excerpt,
                status=status,
                tags=tags,
                categories=categories
            )
            
            if 'error' not in result:
                flash('Post created successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash(f'Error creating post: {result.get("error", "Unknown error")}', 'error')
        else:
            flash('Please fill in the title and content fields', 'error')
    
    # Get existing categories and tags for the form
    categories = wp_client.get_categories()
    tags = wp_client.get_tags()
    
    return render_template('create_post_1.html', categories=categories, tags=tags)

@app.route('/api/test-connection')
def test_connection():
    """Test WordPress API connection"""
    try:
        result = wp_client.get_posts(per_page=1)
        if result:
            return jsonify({
                'status': 'success',
                'message': 'WordPress API connection successful',
                'site_url': wp_client.site_url,
                'total_posts': result.get('total_posts', 0)
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to connect to WordPress API'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Connection error: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)