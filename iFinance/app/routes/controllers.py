from flask import make_response,send_from_directory
from flask_smorest import Blueprint

blp = Blueprint("controllers","controllers",description="controllers")

@blp.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static','sw.js'))
    return response

@blp.route('/favicon.ico')
def service_worker():
    response = make_response(send_from_directory('static','icons/favicon.ico'))
    return response

