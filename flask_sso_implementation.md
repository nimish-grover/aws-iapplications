
# Single Sign-On (SSO) for Multiple Flask Applications

## Overview
This document outlines the steps to implement a Single Sign-On (SSO) solution for multiple Flask applications. The `iCore` app will handle centralized authentication, while the other apps (`ibot`, `iWater`, etc.) will verify authentication using JSON Web Tokens (JWT) issued by `iCore`.

## Directory Structure
```
.
├── run.py
├── iCore
│   ├── models
│   │   └── user.py
│   ├── routes
│   │   └── login.py
│   ├── static
│   ├── templates
│   │   ├── login.html
│   └── app.py
├── ibot
│   ├── routes.py
│   ├── static
│   ├── templates
└── iWater
    ├── routes.py
    ├── static
    ├── templates
```

## Step-by-Step Implementation

### 1. Install Flask-Login and Flask-JWT-Extended

```bash
pip install Flask-Login Flask-JWT-Extended
```

### 2. Define User Model in iCore

```python
# iCore/models/user.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
```

### 3. Configure JWT and Login Manager in `iCore/app.py`

```python
# iCore/app.py
from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from models.user import db, User
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db.init_app(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login logic, generate JWT token, and redirect to the requested app
    pass

if __name__ == '__main__':
    app.run()
```

### 4. Login Logic with JWT in `iCore/routes/login.py`

```python
# iCore/routes/login.py
from flask import request, redirect, url_for, jsonify
from flask_login import login_user
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.user import User

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        login_user(user)
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)  # Return JWT token
    
    return 'Invalid credentials', 401
```

### 5. Modify Other Apps to Use Central Authentication

Each application (`ibot`, `iWater`, etc.) will need to verify the token provided by the `iCore` login.

```python
# ibot/routes.py
from flask import request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()  # Get the current user from the token
    if not current_user:
        return redirect(url_for('iCore.login'))  # Redirect to iCore if not authenticated
    
    return 'Welcome to ibot dashboard!'
```

### 6. Redirect to iCore Login Page

Modify each app to redirect unauthenticated users to the login page in `iCore` if no valid token is present.

```python
@app.before_request
def require_login():
    token = request.cookies.get('access_token')
    if not token:
        return redirect('http://icore.example.com/login')  # Redirect to iCore login page
```

### 7. Centralized Logout

Create a centralized logout route in `iCore` that invalidates the session or token.

```python
# iCore/routes/logout.py
from flask_login import logout_user

@app.route('/logout')
def logout():
    logout_user()
    # Invalidate the JWT token as needed
    return redirect(url_for('login'))
```

## Summary
By following this approach, all Flask applications can use a common authentication method while maintaining their individual logic, databases, and models.
