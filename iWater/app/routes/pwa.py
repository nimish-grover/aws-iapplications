from datetime import date
import json
from flask import make_response, redirect, render_template, request, send_from_directory, g, session, url_for
from flask_smorest import Blueprint

from iWater.app.classes.water_demand import WaterDemand
from iWater.app.classes.water_supply import WaterSupply
from iWater.app.models import District, Block, Village
from iWater.app.models.rainfall import RainfallDatum
from iWater.app.models.state import State
from iWater.app.routes.water_budget import WaterBudgetCalc


blp = Blueprint("PWA", "pwa_calls", description="api call for pwa")

@blp.route('/')
def splash_screen():
    # return redirect(url_for('wb.dashboard'))
    return render_template('splash.html')

@blp.route('/states')
def index():
    session['payload'] = None
    states = WaterBudgetCalc.get_states()
    return render_template('index.html', states = states)

@blp.route('/districts',methods=['POST'])
def select_state():
    json_data = request.json
    districts = District.get_districts(json_data['select_id'])
    districts_json=[]
    for district in districts:
        districts_json.append(district.json())
    return districts_json

@blp.route('/blocks',methods=['POST'])
def select_state():
    json_data = request.json
    blocks = Block.get_blocks(json_data['select_id'])
    blocks_json = []
    for block in blocks:
        blocks_json.append(block.json())
    return blocks_json

@blp.route('/villages',methods=['POST'])
def select_state():
    json_data = request.json
    villages = Village.get_villages(json_data['select_id'])
    villages_json = []
    for village in villages:
        villages_json.append(village.json())
    return villages_json

@blp.route('/home', methods=['POST'])
def home():
    # Initialize
    # try:
    if session['payload']:
        payload = session['payload']
        breadcrumbs = session['breadcrumbs']
    else:
        village_id = request.form.get('ddVillages')
        payload = {"village_id": village_id} 
        if village_id is None:
            block_id = request.form.get('ddBlocks')
            payload = {"block_id": block_id}
            if block_id is None:
                district_id = request.form.get('ddDistricts')
                payload = {"district_id": district_id}
                if district_id is None: 
                    payload = request.form.get('payload')
                    payload = payload.replace("\'","\"")
                    payload = json.loads(payload)
        breadcrumbs = list(State.get_breadcrumps(payload))
        session['breadcrumbs']=breadcrumbs
        session['payload'] = payload

    agriculture_demand, human_demand, livestock_demand, available_runoff, harvested_runoff = get_water_budget(payload) 

    # calculate water budget
    water_demand = agriculture_demand + human_demand + livestock_demand
    water_supply = available_runoff + harvested_runoff
    return render_template('home.html',
                           water_demand_labels = ["Human", "Agriculture", "Livestock"],
                           water_demand = [round(human_demand,1),round(agriculture_demand,1),round(livestock_demand,1)],
                           water_supply_labels = ["harvested", "available"],
                           water_supply = [round(harvested_runoff,2), round(available_runoff,2)],
                           water_budget_labels = ['demand','supply'],
                           water_budget_data = [round(water_demand,2), round(water_supply,2)],
                           breadcrumbs = breadcrumbs)

@blp.route('/demand')
def demand():
    payload=session['payload']
    breadcrumbs = session['breadcrumbs']
    human_demand = WaterDemand.human_consumption(json_data=payload)
    human = get_chart_details(human_demand, 'Human', True)
    agriculture_demand = WaterDemand.agricuture_consumption(json_data=payload)
    agriculture = get_chart_details(agriculture_demand, 'Agriculture', True)    
    livestock_demand = WaterDemand.livestock_consumption(json_data=payload)
    livestock = get_chart_details(livestock_demand, 'Livestock', True)
    return render_template('demand.html',
                           human_chart_details = human,
                           agriculture_chart_details = agriculture,
                           livestock_chart_details = livestock,
                           payload = payload,
                           breadcrumbs = breadcrumbs)

@blp.route('/supply')
def supply():
    payload=session['payload']
    breadcrumbs = session['breadcrumbs']
    runoff_available = WaterSupply.available_runoff(json_data=payload)
    available = get_chart_details(runoff_available, 'Available', False)
    runoff_harvested = WaterSupply.harvested_runoff(json_data=payload)
    harvested = get_chart_details(runoff_harvested, 'Harvested', False)    
    return render_template('supply.html',
                           available_chart_details = available,
                           harvested_chart_details = harvested,
                           breadcrumbs = breadcrumbs)

@blp.route('/budget')
def budget():
    # Initialize
    # try:
    if session['payload']:
        payload = session['payload']
        breadcrumbs = session['breadcrumbs']
    else:
        village_id = request.form.get('ddVillages')
        payload = {"village_id": village_id} 
        if village_id is None:
            block_id = request.form.get('ddBlocks')
            payload = {"block_id": block_id}
            if block_id is None:
                district_id = request.form.get('ddDistricts')
                payload = {"district_id": district_id}
                if district_id is None: 
                    payload = request.form.get('payload')
                    payload = payload.replace("\'","\"")
                    payload = json.loads(payload)        
        breadcrumbs = State.get_breadcrumps(payload)
        session['breadcrumbs']=breadcrumbs
        session['payload'] = payload

    human = WaterDemand.human_consumption(json_data=payload)
    agriculture = WaterDemand.agricuture_consumption(json_data=payload)
    livestock = WaterDemand.livestock_consumption(json_data=payload)
    district_id = WaterSupply.get_payload(json_data=payload)
    rainfall = RainfallDatum.get_monthwise_rainfall(district_id, date.today().year - 1)
    runoff_available = WaterSupply.available_runoff(json_data=payload)
    total_runoff = sum(item['quantity'] for item in runoff_available)
    total_actual = sum(item.actual for item in rainfall)
    runoff_harvested = WaterSupply.harvested_runoff(json_data=payload)
    total_harvest = sum(item['supply'] for item in runoff_harvested)
    agriculture_demand, human_demand, livestock_demand, available_runoff, harvested_runoff = get_water_budget(payload) 

    # calculate water budget
    water_demand = agriculture_demand + human_demand + livestock_demand
    water_supply = available_runoff + harvested_runoff
    deficit_surplus = round(harvested_runoff,2)-round(water_demand,2)
    return render_template('budget.html',
                           water_demand_labels = ["Human", "Agriculture", "Livestock"],
                           water_demand = [round(human_demand,1),round(agriculture_demand,1),round(livestock_demand,1)],
                           water_demand_sum = round(round(human_demand,1)+round(agriculture_demand,1)+round(livestock_demand,1),1),
                           water_supply_labels = ["harvested", "available"],
                           water_supply = [round(harvested_runoff,2), round(available_runoff,2)],
                           water_supply_sum = round(round(harvested_runoff,2) + round(available_runoff,2),2),
                           water_budget_labels = ['demand','supply'],
                           water_budget_data = [round(water_demand,2), round(water_supply,2)],
                           humans = human,
                           agricultures = agriculture,
                           livestocks = livestock,
                           runoffs = runoff_available,
                           monthwise_rainfall = rainfall,
                           total_runoff = total_runoff,
                           total_actual = total_actual,
                           harvests=runoff_harvested,
                           total_harvest=total_harvest,
                           harvested_runoff=harvested_runoff,
                           deficit_surplus=deficit_surplus,
                           breadcrumbs = breadcrumbs)

def get_water_budget(payload):
    agriculture_demand, human_demand, livestock_demand = 0, 0, 0
    # calculate demand
    agriculture = WaterDemand.agricuture_consumption(json_data=payload)
    if agriculture:
        for item in range(len(agriculture)):
            agriculture_demand = agriculture[item]['demand'] + agriculture_demand
    human =WaterDemand.human_consumption(json_data=payload)
    if human:
        for item in range(len(human)):
            human_demand = human[item]['demand'] + human_demand
    livestock = WaterDemand.livestock_consumption(json_data=payload)
    if livestock:
        for item in range(len(livestock)):
            livestock_demand = livestock[item]['demand'] + livestock_demand

    # calculate supply
    available_runoff, harvested_runoff = 0, 0
    # supply = wb['supply']
    # supply = WaterBudgetCalc.water_supply(payload=payload)
    available = WaterSupply.get_available_runoff(json_data=payload)
    if available:
        available_runoff = available['good'] + available['average'] + available['bad']
    harvested= WaterSupply.get_harvested_runoff(json_data=payload)
    if harvested:
        for item in range(len(harvested)):
            harvested_runoff = harvested[item]['area'] + harvested_runoff
    return agriculture_demand,human_demand,livestock_demand,available_runoff,harvested_runoff


def get_chart_details(dict_list, chart_title, isDemand):
    chart_labels=[]
    chart_consume_data=[]
    chart_count_data = []
    for element in dict_list:
        chart_labels.append(element['type'].title())
        if isDemand:
            chart_consume_data.append(element['demand'])
        else:
            chart_consume_data.append(element['supply'])
        chart_count_data.append(element['quantity'])
    chart_details = {
        'chart_labels':chart_labels, 
        'chart_count_data':chart_count_data, 
        'chart_consume_data':chart_consume_data, 
        'chart_title': chart_title
        }
    return chart_details


