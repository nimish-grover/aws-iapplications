import json
from flask import jsonify, request
from flask_smorest import Blueprint

from iWater.app.models.water_bodies import Water_bodies


blp = Blueprint("wb_api", "waterbodies_api", description="API for waterbodies")

@blp.route("/dash", methods=["POST"])
def get_dashboard_data():
    form_data = request.json
    if 'country_id' in form_data:
         payload = form_data
    elif form_data is not None:
        village_id = form_data['village_id']
        payload = {"village_id": village_id} 
        if village_id is None or village_id == '-1':
                block_id = form_data['block_id']
                payload = {"block_id": block_id}
                if block_id is None or block_id == '-1':
                    district_id = form_data['district_id']
                    payload = {"district_id": district_id}
                    if district_id is None or district_id == '-1': 
                        state_id = form_data['state_id']
                        payload = {"state_id": state_id}
                        if state_id is None or state_id == '-1':
                            payload = {'state_id': '-1'}

    
    # get wb count, storage and area
    primary_data = json.dumps(Water_bodies.get_count_and_sum(payload))
    # get chart data for top five
    top_five = Water_bodies.get_top_five(payload)
    top_all = Water_bodies.get_top_five(json_data=payload,is_top_five=False)
    barhchart_x_data=[]
    barhchart_y_data = []
    html_table = []
    if top_five is not None:
        for index,row in enumerate(top_five):             
                barhchart_y_data.append(row['name'])  
                barhchart_x_data.append(row['wb_count'])
                html_table.append({"S.No.":index+1,"Name":row['name'], "Count": row['wb_count'], "Storage": row['storage'], "Area": row['spread_area']})  
    top_all_table = []
    if top_all is not None:
        for index,row in enumerate(top_all):             
                top_all_table.append({"S.No.":index+1,"Name":row['name'], "Count": row['wb_count'], "Storage": row['storage'], "Area": row['spread_area']})   
    # get chart data for wb types
    wb_type_data = json.dumps(Water_bodies.get_wb_type(payload))
    # get table data

    # get chart data for bubble chart for storage

    return jsonify({"primary_data": primary_data, 
                      "wb_type_data":wb_type_data,
                      "top_five": html_table,
                      "top_all": top_all_table,
                      "barhchart_y_data":barhchart_y_data,
                      "barhchart_x_data":barhchart_x_data})

@blp.route("/lat_long")
def get_lat_long():
     markers = Water_bodies.get_lat_long()
     converted_markers = []
     for marker in markers:
        marker['latitude'] = WaterbodyHelper.convert_deg_to_deci(marker['latitude'])
        marker['longitude'] = WaterbodyHelper.convert_deg_to_deci(marker['longitude'])
        converted_markers.append(marker)
     return converted_markers

class WaterbodyHelper():
    def convert_deg_to_deci(value_in_deg):
        if value_in_deg:
            deg_min_sec = str(value_in_deg).split(":")[1].split("/")
            deg = float(deg_min_sec[0])
            min = float(deg_min_sec[1])
            sec = float(deg_min_sec[2])
            return deg + (min+(sec/60))/60
        
     