from flask import Blueprint, render_template


blp = Blueprint('ldn','ldn','land degradation dashboard')

@blp.route("/")
def dashboard():
    return render_template('dashboard.html')