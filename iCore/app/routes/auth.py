
from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from iCore.app.models import User
from passlib.hash import pbkdf2_sha256

blp = Blueprint("auth", "auth")

# Login route
@blp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.find_by_username(username)      
        if user:
            db_username = user.username
            db_pass = user.password
            hash_check = pbkdf2_sha256.verify(password,db_pass)        
            if db_username == username and hash_check:
                login_user(user)
                token = create_access_token(identity=user.id)
                response = make_response(redirect(url_for('routes.home')))
                response.set_cookie('access_token', token)
                return response
                # return jsonify(access_token=token)
        
        return 'Invalid credentials', 401
    
    return render_template('login.html')
@blp.route('/logout')
def logout():
    logout_user()
    # Invalidate the JWT token as needed
    return redirect(url_for('login'))

@blp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
    
        user = User.find_by_username(username)
        if user:
            flash('username already exists')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            return 'Passwords do not match', 400
    
        hash_password = pbkdf2_sha256.hash(password)
        user = User(username, hash_password)
        user.save_to_db()
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')