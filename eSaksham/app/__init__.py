from flask import Flask,render_template,request,redirect

def create_app():
    # Initialize Flask application
    app = Flask(__name__, static_folder='scorm', template_folder='scorm')
    return app


    
