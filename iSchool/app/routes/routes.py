from flask import Blueprint, render_template


blp = Blueprint('routes','routes')

@blp.route("/")
def home():
    return render_template('home.html')