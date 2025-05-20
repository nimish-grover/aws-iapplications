from datetime import date
from iWater.app.models.block import Block
from iWater.app.models.rainfall import RainfallDatum
from iWater.app.models.strange_table import StrangeRunoff
from iWater.app.models.census import CensusDatum
from iWater.app.models.village import Village
from iWater.app.models.waterbody import Waterbody


class WaterSupply:

    def __init__(self):
        pass

    def get_available_runoff(json_data):
        census = CensusDatum.get_census_data(json_data=json_data)
        good_catchment_area = census.forest_area + census.non_agricultural_area + census.uncultivable_land_area
        average_catchment_area = census.grazing_land_area + census.misc_crops_area + census.wasteland_area
        irrigated_area = census.canals_area + census.tubewell_area + census.tank_lake_area + census.waterfall_area + census.other_sources_area
        bad_catchment_area = census.fallows_land_area + census.current_fallows_area + census.unirrigated_land_area + irrigated_area
        district_id = WaterSupply.get_payload(json_data)
        rainfall = RainfallDatum.get_rainfall(district_id, date.today().year - 1)
        runoff = StrangeRunoff.get_runoff_yield(rainfall=rainfall)
        water_resources = {'good': round((good_catchment_area/10000) * runoff['good'],2),
                           'average': round((average_catchment_area/10000) * runoff['average'],2),
                           'bad': round((bad_catchment_area/10000) * runoff['bad'],2)}
        return water_resources

    def get_payload(json_data):
        if 'village_id' in json_data:
            result = Village.get_district_by_village(json_data['village_id'])
            district_id = result.district_id
        if 'block_id' in json_data:
            result = Block.get_district_by_block(json_data['block_id'])
            district_id = result.district_id
        if 'district_id' in json_data:
            district_id = json_data['district_id']
        return district_id
    
    def available_runoff(json_data):
        census = CensusDatum.get_census_data(json_data=json_data)
        catchments = {'good': 0.0, 'average':0.0, 'bad':0.0}
        catchments['good'] = census.forest_area + census.non_agricultural_area + census.uncultivable_land_area
        catchments['average'] = census.grazing_land_area + census.misc_crops_area + census.wasteland_area
        irrigated_area = census.canals_area + census.tubewell_area + census.tank_lake_area + census.waterfall_area + census.other_sources_area
        catchments['bad'] = census.fallows_land_area + census.current_fallows_area + census.unirrigated_land_area + irrigated_area
        district_id = WaterSupply.get_payload(json_data)
        rainfall = RainfallDatum.get_rainfall(district_id, date.today().year - 1)
        runoff = StrangeRunoff.get_runoff_yield(rainfall=rainfall)
        water_resources=[]
        for key in catchments.keys():
            water_resources.append({'type': key, 'supply':round((catchments[key]/10000) * runoff[key],2), 'quantity': runoff[key]})
        return water_resources
    
    def get_harvested_runoff(json_data):
        harvested_runoff = []
        waterbodies = Waterbody.get_waterbodies(json_data=json_data)
        for item in waterbodies:
            harvested_runoff.append({'area': round(float(item[0]),2), 'waterbody':item[1]})
        return harvested_runoff
    
    def harvested_runoff(json_data):
        waterbodies = Waterbody.get_waterbodies(json_data=json_data)
        waterbody_types = {w.waterbody for w in waterbodies}       
        water_harvested = []
        for type in waterbody_types:
            count = 0
            count = sum(i.waterbody==type for i in waterbodies)
            total_area = 0.0
            total_area = sum(list(i.area for i in waterbodies if i.waterbody==type))
            water_harvested.append({'type': type, 'supply':round((total_area),2), 'quantity': count})            
        return water_harvested