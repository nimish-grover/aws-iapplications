from collections import Counter
from datetime import date
from datetime import datetime
from flask import render_template, request, session,url_for,redirect,flash
from flask_smorest import Blueprint, abort
from iFinance.app.db_extensions import *
from iFinance.app.models.project import projectDataModel, pywfModel
from iFinance.app.models.admin_model import  AdminModel
from iFinance.app.schemas import FinancialDataSchema
from passlib.hash import pbkdf2_sha256
from flask_login import login_user
from flask_login import login_required, current_user,logout_user


blp = Blueprint("admin", "admin",
                description="blueprint for admin pages")\
                

@blp.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = AdminModel.query.filter_by(username=username).first()       
        if user:
            db_username = user.username
            db_pass = user.password
            hash_check = pbkdf2_sha256.verify(password,db_pass)        
            if db_username == username and hash_check:
                login_user(user)
                return redirect(url_for('dashboard.financials'))
        else:
            flash('Please Check your login credentials and try again !! ')
            return redirect(url_for('admin.login'))
        
    return render_template('login.html')


@blp.route('/register',methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        name = request.form.get('name')
        password = pbkdf2_sha256.hash(request.form.get('password'))

        user = AdminModel.get_user_by_username(username)
        if user:
            flash('Email address already exists')
            return redirect(url_for('admin.register'))

        user = AdminModel(name,username,password)
        user.save_to_db()
        return redirect(url_for('admin.login'))

    return render_template('register.html')


@blp.route('/logout')
@login_required
def logout():
    
    logout_user()
    session['logged_out']=True
    return redirect(url_for('admin.login'))


@blp.route('/view_profile')
@login_required
def profile():

    return render_template('profile.html',name=current_user.name, username=current_user.username)

@blp.route('/update_user/<id>')
@login_required
def update_user(id):
    
    if request.method == "POST":
            
        name = request.form.get('name')
        username = request.form.get('username')
        
        data = {"name":name,"username":username}
        AdminModel.update_db(data,id)   

        return redirect(url_for('admin.profile'))
    
    if request.method == "GET":
        user=AdminModel.get_user_by_id(id)
        
        return render_template('update_user.html',user=user)
    
@blp.route('/view_users')
def view_users():
    
    if request.method == "GET":
        users=AdminModel.get_all()
        
        return render_template('view_users.html',users=users)
    
@blp.route('/change_password/<id>',methods=['GET','POST'])
@login_required
def change_password(id):

    if request.method == "POST":
            
        current_pwd = request.form.get('curr_pwd')
        new_pwd = pbkdf2_sha256.hash(request.form.get('new_pwd'))

        user = AdminModel.query.filter_by(id=id).first()       
        if user:
        
            db_pass = user.password
            hash_check = pbkdf2_sha256.verify(current_pwd,db_pass)        
            if hash_check:
                data = {"password":new_pwd}
                AdminModel.update_db(data,id)   

                return redirect(url_for('admin.profile'))
            
            else:
                flash('Please Check Your Old Password and Try Again !! ')
                return redirect(url_for('admin.change_password',id=id))
    
    if request.method == "GET":
        user=AdminModel.get_user_by_id(id)
        
        return render_template('change_password.html',user=user)
    
