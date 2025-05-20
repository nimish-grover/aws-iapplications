import json
from flask import jsonify, request
from flask_smorest import Blueprint
from iWater.app.classes.water_demand import WaterDemand
from iWater.app.models.block import Block
from iWater.app.models.district import District
from iWater.app.models.state import State

from iWater.app.models.strange_table import StrangeRunoff
from iWater.app.classes.water_supply import WaterSupply
from iWater.app.models.village import Village

blp = Blueprint("Water_Budget", "water_budget", description="water budget calculation")

class WaterBudgetCalc:

    @blp.route('/yield', methods=['POST'])
    def runoff_yield():
        json_data = request.json
        runoff_yield = StrangeRunoff.get_runoff_yield(rainfall=json_data['rainfall'])
        return runoff_yield

    @blp.route('/demand', methods=['POST'])
    def water_demand():
        json_data = request.json
        human_demand = WaterDemand.human_consumption(json_data)
        agriculture_demand = WaterDemand.agricuture_consumption(json_data)
        livestock_demand = WaterDemand.livestock_consumption(json_data)
        return jsonify({ 'livestock' : livestock_demand, 'agriculture': agriculture_demand, 'human': human_demand })


    @blp.route("/supply", methods=['POST'])
    def water_supply():
        json_data = request.json
        available_runoff = WaterSupply.get_available_runoff(json_data)
        harvested_runoff = WaterSupply.get_harvested_runoff(json_data)   
        return {"available": available_runoff, "harvested": harvested_runoff}

    @blp.route("/states", methods=['GET','POST'])
    def get_states():
        states = State.get_states()
        states_json = []
        for state in states:
            states_json.append(state.json())
        return states_json

    @blp.route("/districts", methods=['POST'])
    def get_districts():
        json_data = request.json
        districts = District.get_districts(json_data['select_id'])
        districts_json = []
        for district in districts:
            districts_json.append(district.json())
        return districts_json

    @blp.route("/blocks", methods=['POST'])
    def get_blocks():
        json_data = request.json
        blocks = Block.get_blocks(json_data['select_id'])
        blocks_json = []
        for block in blocks:
            blocks_json.append(block.json())
        return blocks_json

    @blp.route("/villages", methods=['POST'])
    def get_villages():
        json_data = request.json
        villages = Village.get_villages(json_data['select_id'])
        villages_json = []
        for village in villages:
            villages_json.append(village.json())
        return villages_json


from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)