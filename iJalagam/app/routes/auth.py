from flask import Blueprint, flash, get_flashed_messages, json, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from iJalagam.app.classes.helper import HelperClass
from iJalagam.app.models.states import State
from iJalagam.app.models.territory import TerritoryJoin
from iJalagam.app.models.users import User

blp = Blueprint("auth","auth")

@blp.route('/register', methods=['POST','GET'])
def register():
    message = get_message()
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        state_id = request.form.get('dd_states')
        user = User.find_by_username(username.lower())
        if user:
            flash('username already exists!')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('auth.register'))

        user = User(username.lower(), password,state_id, False, False)
        user.set_password(password)
        user.save_to_db()

        flash('Registered successfully!')
        return redirect(url_for('auth.login'))
    states = TerritoryJoin.get_aspirational_states()
    return render_template("auth/register_user.html", 
                           flash_message=message, 
                           states = states)

@blp.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next = request.args.get('next')
        try:        
            user = User.query.filter_by(username=username.lower()).first()
            if user and User.check_password(user, password) and user.isActive:
                login_user(user)
                return redirect(url_for('mobile.index'))
            elif user is None:
                flash('User does not exist!')
            elif not User.check_password(user, password):
                flash('Password is incorrect')
            elif not user.isActive:
                flash('User is not authorized. Please contact State Coordinator')
        except Exception as e:
            flash('There was an error while connecting to database!')
            print(e)
    message = get_message()
    return render_template('auth/login.html', flash_message = message)

@blp.route('/logout')
def logout():
    logout_user()
    session.clear()
    session['logged_out']=True
    return redirect(url_for('.login'))

@blp.route('/change_password', methods=['POST','GET'])
@login_required
def change_password():
    if request.method=='POST':
        password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        try:
            user = User.query.filter_by(id=current_user.id).first()
            if user and User.check_password(user, password) and user.isActive:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.update_db()
                    flash('Password changed successfully! Please login with new password!')
                    return redirect(url_for('auth.logout'))
                else:
                    flash('new and confirm password do not match!')
                    return redirect(url_for('auth.change_password'))
            elif user is None:
                flash('User does not exist!')
            elif not User.check_password(user, password):
                flash('Old password is incorrect')
            elif not user.isActive:
                flash('User is not active. Please contact State Coordinator')
        except Exception as e:
            flash('There was an error while connecting to database!')
            print(e)    
    message = get_message()
    return render_template("auth/change_password.html", flash_message = message)

@blp.route('/forgot_password')
@login_required
def forgot_password():
    return render_template("auth/forgot_password.html")

@blp.route('/reset_password', methods=['POST','GET'])
@login_required
def reset_password():
    if current_user.isAdmin: 
        users = User.get_all()           
        if request.method=='POST':
            try:
                json_data = request.json
                user = User.query.filter_by(id=json_data['id']).first()
                if user and user.isActive:
                    reset_pwd = user.username + '_123'
                    user.set_password(reset_pwd)
                    user.update_db()
                    flash('Password reset successfully! Please login with new password!')
                    return {'redirect_url' : url_for('auth.approve')}
                elif user is None:
                    flash('User does not exist!')
                elif not user.isActive:
                    flash('User is not active!')
            except Exception as e:
                flash('There was an error connecting to database!')
                print(e)        
        # return render_template("auth/reset_password.html")
    else:
        flash("Only admin can reset password!")
    message = get_message()
    return render_template("auth/reset_password.html",
                           post_url = url_for('.reset_password'),
                           flash_message = message,
                           users=users,
                           user_data=json.dumps(users))
    

@blp.route('/approve', methods=['POST','GET'])
@login_required
def approve():
    if request.method =='POST':
        json_data = request.json
        for item in json_data:
            if item['id']:
                user_object = User.get_by_id(item['id'])
                user_object.isActive = bool(item['isActive'])
                user_object.update_db()
        flash("The user(s) is/are approved!!")
        return jsonify({'redirect_url': url_for('mobile.index')})
    if current_user.isAdmin:
        users = User.get_all()
        # states = State.get_all()
        message = get_message()
        return render_template('auth/approve.html',
                            flash_message = message,
                            users=users,
                            user_data=json.dumps(users),
                            menu= HelperClass.get_admin_menu())
    else: 
        flash('You must be admin to view this page!')
        return redirect(url_for('auth.login'))

@blp.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    chart_data = HelperClass.get_dashboard_menu()
    card_data = HelperClass.get_card_data(chart_data)
            
    return render_template('auth/dashboard.html',
                           card_data = card_data,
                           chart_data = json.dumps(chart_data),
                           flash_message = get_message(),
                           menu= HelperClass.get_admin_menu())

@blp.route('/progress')
@login_required
def progress():
    if current_user.isAdmin:
        progress = State.get_all_states_status()
        status_dummy = [{'category':'Human','id':'population'},
                        {'category':'Livestocks','id':'livestock'},
                        {'category':'Crops','id':'crop'},
                        {'category':'Industry','id':'industry'},
                        {'category':'Surface','id':'surface'},
                        {'category':'Groundwater','id':'ground'},
                        {'category':'LULC','id':'lulc'},
                        {'category':'Rainfall','id':'rainfall'},
                        {'category':'Water Transfer','id':'water_transfer'}]
        return render_template('auth/progress.html',
                            progress=sorted(progress, key=lambda x: x["completed"], reverse=True),
                            status = status_dummy,
                            menu = HelperClass.get_admin_menu(),
                            progress_data = json.dumps(progress))
    else: 
        flash('You must be admin to view this page!')
        return redirect(url_for('auth.login'))

def get_message():
    messages = get_flashed_messages()
    # if len(messages) > 0:
    #     message = messages[0]
    # else:
    #     message = ''

    return messages
