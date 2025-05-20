from flask import make_response, render_template, send_from_directory
from flask_smorest import Blueprint

blp = Blueprint('controllers', 'controllers', description="controllers for pwa")

@blp.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'sw.js'))
    # response.headers['Cache-Control'] = 'no-cache'
    return response

@blp.route('/manifest.json')
def service_worker():
    response = make_response(send_from_directory('static', 'manifest.json'))
    # response.headers['Cache-Control'] = 'no-cache'
    return response

@blp.route('/favicon.ico')
def service_worker():
    response = make_response(send_from_directory('static', 'assets/favicon.ico'))
    return response

@blp.route('/style.css')
def service_worker():
    response = make_response(send_from_directory('static', 'css/style.css'))
    return response

@blp.route('/app.js')
def service_worker():
    response = make_response(send_from_directory('static', 'js/app.js'))
    return response

@blp.route('/')
def welcome_page():
    return render_template('index.html')