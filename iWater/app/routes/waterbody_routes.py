from flask import render_template, session
from flask_smorest import Blueprint

from iWater.app.routes.water_budget import WaterBudgetCalc
from iWater.app.routes import wb_api


blp = Blueprint("wb","wb", description="waterbodies of India")

@blp.route("/dashboard")
def dashboard():
    session['payload'] = None
    states = WaterBudgetCalc.get_states()
    return render_template('dashboard.html', states = states)

@blp.route("/maps")
def get_markers():
    markers = wb_api.get_lat_long()
    json_markers = []
    lat_total = 0.0
    long_total = 0.0
    for marker in markers:
        lat_total = lat_total + float(marker['latitude'])
        long_total = long_total + float(marker['longitude'])
        marker = {
        'lat':marker['latitude'],
        'lon':marker['longitude'],
        'popup':marker['name']
        }
        json_markers.append(marker)
    avg_lat = lat_total/len(json_markers)
    avg_long = long_total/len(json_markers)
    # markers=[
    #     {
    #     'lat':51.505,
    #     'lon':-0.09,
    #     'popup':'This is the middle of the map.'
    #     }
    # ]
    return render_template('wb_maps.html',markers=json_markers,avg_lat=avg_lat, avg_long=avg_long )