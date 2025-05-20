from flask import Blueprint, json, make_response, redirect, render_template, request, session, url_for
from flask_login import current_user

from iJalagam.app.classes.budget_data import BudgetData
from iJalagam.app.models import TerritoryJoin
from iJalagam.app.models.states import State


blp = Blueprint("mobile","mobile")

@blp.route('/')
def splash():
    return redirect(url_for('.index'))
    # return render_template("splash_screen.html")

@blp.route('/index', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        json_data = request.json
        payload = json.dumps(json_data)
        if 'payload' in session:
            session['payload'] = ''
        session['payload'] = payload
        if current_user.is_authenticated:
            return json.dumps(url_for('desktop.status'))
        return json.dumps(url_for('.home'))
    if current_user.is_authenticated:
        if current_user.isAdmin:
            states = TerritoryJoin.get_aspirational_states()
        else:
            states = State.get_states_by_id(current_user.state_id)
    else:
        states = TerritoryJoin.get_aspirational_states()
    return render_template("mobile/index.html", states=states)

@blp.route("/districts", methods=['POST'])
def districts():
    json_data = request.json
    if json_data is not None:
        state_id = int(json_data['state_id'])
    else:
        return make_response('', 400)
    districts = TerritoryJoin.get_aspirational_districts(state_id)
    if districts:
        return districts
    else:
        return make_response('', 400)
    
@blp.route("/blocks", methods=['POST'])
def blocks():
    json_data = request.json
    if json_data is not None:
        district_id = int(json_data['district_id'])
    else:
        return make_response('', 400)
    blocks = TerritoryJoin.get_aspirational_blocks(district_id)
    if blocks:
        return blocks
    else:
        return make_response('', 400)

@blp.route('/home')
def home():
    payload = session.get('payload')
    if not payload:
        return redirect(url_for('.index'))
    else:
        payload = json.loads(payload)
    demand_side = BudgetData.get_demand_side(payload['block_id'], payload['district_id'])
    supply_side = BudgetData.get_supply_side(payload['block_id'], payload['district_id'])
    budget = BudgetData.get_water_budget(payload['block_id'], payload['district_id'])
    budget_data = []
    budget_data.append(demand_side)
    budget_data.append(supply_side)
    budget_data.append(budget)
    return render_template("mobile/home.html", 
                           breadcrumbs = get_breadcrumbs(payload),
                           demand_side = budget_data[0],
                           supply_side = budget_data[1],
                           water_budget = budget_data[2],
                           menu = get_main_menu(),
                           chart_data = json.dumps(budget_data),
                           toggle_labels=['chart', 'table'])

@blp.route('/human')
def human():
    """
    Handle human demand route.
    """
    return render_demand_template(
        "mobile/demand/human.html",
        demand_function=BudgetData.get_human_consumption,
        template_data_key='human'
    )

@blp.route('/livestocks')
def livestocks():
    return render_demand_template(
        "mobile/demand/livestocks.html",
        demand_function=BudgetData.get_livestock_consumption,
        template_data_key='livestocks'
    )

@blp.route('/crops')
def crops():
    return render_demand_template(
        "mobile/demand/crops.html",
        demand_function=BudgetData.get_crops_consumption,
        template_data_key='crops'
    )

@blp.route('/industry')
def industry():
    payload = session.get('payload')
    if not payload:
        return redirect(url_for('.index'))
    else:
        payload = json.loads(payload)
    return render_template("mobile/demand/industry.html", 
                        breadcrumbs= get_breadcrumbs(payload), 
                        menu= get_demand_menu(),
                        toggle_labels=['chart', 'table'])

@blp.route('/surface')
def surface():
    return render_supply_template(
        "mobile/supply/surface.html",
        supply_function=BudgetData.get_surface_supply,
        template_data_key='waterbodies'
    )

@blp.route('/ground')
def ground():
    return render_supply_template(
        "mobile/supply/ground.html",
        supply_function=BudgetData.get_ground_supply,
        template_data_key='groundwater'
    )

@blp.route('/rainfall')
def rainfall():
    payload = session.get('payload')
    if not payload:
        return redirect(url_for('.index'))
    else:
        payload = json.loads(payload)
    rainfall_data = BudgetData.get_rainfall(payload['block_id'], payload['district_id'])
    return render_template("mobile/supply/rainfall.html", 
                           monthwise_rainfall = rainfall_data,
                           chart_data = json.dumps(rainfall_data),
                           breadcrumbs = get_breadcrumbs(payload),
                           menu= get_supply_menu(),
                           toggle_labels=['chart', 'table'])

@blp.route('/runoff')
def runoff():
    payload = session.get('payload')
    if not payload:
        return redirect(url_for('.index'))
    else:
        payload = json.loads(payload)
    runoff_data = BudgetData.get_runoff(payload['block_id'], payload['district_id'])
    return render_template("mobile/supply/runoff.html", 
                           catchments=runoff_data,
                           chart_data = json.dumps(runoff_data),
                           breadcrumbs = get_breadcrumbs(payload),
                           menu= get_supply_menu(),
                           toggle_labels=['chart', 'table'])

def render_supply_template(template, supply_function, template_data_key):
    payload = session.get('payload')
    if not payload:
        return redirect(url_for('.index'))
    else:
        payload = json.loads(payload)
    # Fetch supply data
    chart_data = supply_function(payload['block_id'], payload['district_id'])
    toggle_labels=['chart', 'table']

    context = {
        template_data_key: chart_data,
        "chart_data": json.dumps(chart_data),
        "toggle_labels": toggle_labels,
        "breadcrumbs": get_breadcrumbs(payload), 
        "menu": get_supply_menu()
    }

    return render_template(template, **context)


def render_demand_template(template, demand_function, template_data_key):
    """
    Render a demand-related template with shared logic for retrieving demand data and rendering the page.

    Args:
        template (str): Template path to render.
        demand_function (callable): Function to fetch demand data (e.g., WaterBudget.get_human_demand).
        toggle_labels (list): Labels for toggling chart/table views.
        template_data_key (str): Key for the primary data object in the template context.

    Returns:
        Rendered HTML template or a redirect if session data is missing.
    """
    payload = session.get('payload')
    if not payload:
        return redirect(url_for('.index'))
    else:
        payload = json.loads(payload)
    # block, district = payload['block_id'], payload['district_id']

    # Fetch demand data
    chart_data = demand_function(payload['block_id'], payload['district_id'])

    toggle_labels=['chart', 'table']
    # Prepare template context
    context = {
        template_data_key: chart_data,
        "chart_data": json.dumps(chart_data),
        "toggle_labels": toggle_labels,
        "breadcrumbs": get_breadcrumbs(payload), 
        "menu": get_demand_menu()
    }

    return render_template(template, **context)


def get_breadcrumbs(payload):
    """
    Generate breadcrumb navigation based on the current payload.

    Returns:
        list: Breadcrumbs for the current context.
    """
    return [
        {'name': payload['state_name'], 'href': '#'},
        {'name': payload['district_name'], 'href': '#'},
        {'name': payload['block_name'], 'href': '#'}
    ]

def get_supply_menu():
    return [
        { "route" : url_for('.home'), "label":"back", "icon":"fa-solid fa-left-long"},
        { "route" : url_for('.surface'), "label":"surface", "icon":"fa-solid fa-water"},
        { "route" : url_for('.ground'), "label":"ground", "icon":"fa-solid fa-arrow-up-from-ground-water"},
        { "route" : url_for('.runoff'), "label":"runoff", "icon":"fa-solid fa-cloud-showers-water"},
        { "route" : url_for('.rainfall'), "label":"rainfall", "icon":"fa-solid fa-cloud-rain"},
    ]

def get_demand_menu():
    return [
        { "route" : url_for('.home'), "label":"back", "icon":"fa-solid fa-left-long"},
        { "route" : url_for('.human'), "label":"human", "icon":"fa-solid fa-people-roof"},
        { "route" : url_for('.livestocks'), "label":"livestock", "icon":"fa-solid fa-paw"},
        { "route" : url_for('.crops'), "label":"crops", "icon":"fa-brands fa-pagelines"},
        { "route" : url_for('.industry'), "label":"industry", "icon":"fa-solid fa-industry"},
    ]

def get_main_menu():
    return [
        { "route" : url_for('.human'), "label":"demand", "icon":"fa-solid fa-chart-line"},
        { "route" : url_for('.index'), "label":"home", "icon":"fa-solid fa-house"},
        { "route" : url_for('.surface'), "label":"supply", "icon":"fa-solid fa-glass-water-droplet"},
    ]