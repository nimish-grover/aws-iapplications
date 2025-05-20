from types import SimpleNamespace

from flask import url_for
from iJalagam.app.classes.budget_data import BudgetData
from iJalagam.app.models.block_crops import BlockCrop
from iJalagam.app.models.block_ground import BlockGround
from iJalagam.app.models.block_industries import BlockIndustry
from iJalagam.app.models.block_livestocks import BlockLivestock
from iJalagam.app.models.block_lulc import BlockLULC
from iJalagam.app.models.block_pop import BlockPop
from iJalagam.app.models.block_rainfall import BlockRainfall
from iJalagam.app.models.block_surface import BlockWaterbody
from iJalagam.app.models.block_territory import BlockTerritory
from datetime import datetime, timezone

from iJalagam.app.models.block_transfer import BlockWaterTransfer
from iJalagam.app.models.industries import Industry
from iJalagam.app.models.lulc_census import LULCCensus

class BlockData:
    @classmethod
    def get_bt_id(cls, block_id, district_id, state_id):
        bt_id = BlockTerritory.get_bt_id(block_id=int(block_id), district_id=int(district_id), state_id=int(state_id))
        if bt_id:
            return bt_id
        else:
            block_territory = BlockTerritory(state_id=state_id, district_id=district_id, block_id=block_id)
            block_territory.save_to_db()
            bt_id = BlockTerritory.get_bt_id(block_id, district_id, state_id)
            return bt_id
        
    @classmethod
    def get_human_consumption(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_human(block_id, district_id, bt_id, user_id)
    
    # inserted by system
    def get_or_insert_human(block_id, district_id, bt_id, user_id):
        human = BlockPop.get_by_bt_id(bt_id)
        if human:
            return human
        else:
            human_consumption = BudgetData.get_human_consumption(block_id=block_id, district_id=district_id)
            if human_consumption:
                for item in human_consumption:
                    block_population = BlockPop(
                                        population_id=item['id'],
                                        count=item['count'],
                                        bt_id=bt_id, 
                                        is_approved=False, 
                                        created_by=user_id)
                    block_population.save_to_db()
                human = BlockPop.get_by_bt_id(bt_id)     
                return human

    # updated / inserted by user
    def update_human(json_data, user_id):
        for item in json_data: 
            block_population = BlockPop(
                        population_id=item['population_id'],
                        count=item['count'],
                        bt_id=item['bt_id'], 
                        is_approved=True, 
                        created_by=user_id)
            if item['count'] >0:
                block_population.save_to_db()
            else:
                if item['count']==0:
                    if item['table_id']:
                        block_population = None
                        block_population = BlockPop.get_by_id(item['table_id']) 
                        if block_population:
                            block_population.delete_from_db()  
        return True
    
    @classmethod
    def get_livestock_consumption(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_livestock(block_id, district_id, bt_id, user_id)
    
    # inserted by system
    def get_or_insert_livestock(block_id, district_id, bt_id, user_id):
        livestock = BlockLivestock.get_by_bt_id(bt_id)
        if all(row['table_id'] is None for row in livestock):
            livestock_consumption = BudgetData.get_livestock_consumption(block_id=block_id, district_id=district_id)
            if livestock_consumption:
                for item in livestock_consumption:
                    block_livestock = BlockLivestock(
                                livestock_id=item['id'],
                                count=item['count'],
                                bt_id=bt_id,
                                is_approved=False, 
                                created_by=user_id)
                    block_livestock.save_to_db()
                livestock = BlockLivestock.get_by_bt_id(bt_id)     
                return livestock
        else:
            return livestock
            
    # updated / inserted by user
    def update_livestock(json_data, user_id):
        for item in json_data: 
            block_livestock = BlockLivestock(
                    livestock_id=item['id'],
                    count=item['count'],
                    bt_id=item['bt_id'],
                    is_approved=True, 
                    created_by=user_id)
            if item['count']>0:
                block_livestock.save_to_db()
            else:
                if item['count']==0:
                    if item['table_id']:
                        block_livestock = None
                        block_livestock = BlockLivestock.get_by_id(item['table_id']) 
                        if block_livestock:
                            block_livestock.delete_from_db()  
        return True

    @classmethod
    def get_crops_consumption(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_crops(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_crops(block_id, district_id, bt_id, user_id):
        crops = BlockCrop.get_by_bt_id(bt_id)
        if all(row['table_id'] is None for row in crops):
            crops_consumption = BudgetData.get_crops_consumption(block_id=block_id, district_id=district_id)
            if crops_consumption:
                for item in crops_consumption:
                    block_crops = BlockCrop(
                                crop_id=item['id'],
                                area=item['count'],
                                bt_id=bt_id,
                                is_approved=False, 
                                created_by=user_id)
                    block_crops.save_to_db()
                crops = BlockCrop.get_by_bt_id(bt_id)     
                return crops
        else:
            return crops
    
    def update_crops(json_data, user_id):
        for item in json_data: 
            block_crops = BlockCrop(
                    crop_id=item['crop_id'],
                    area=item['crop_area'],
                    bt_id=item['bt_id'],
                    is_approved=True, 
                    created_by=user_id)
            if item['crop_area']>0:
                block_crops.save_to_db()
            else:
                if item['crop_area']==0:
                    if item['table_id']:
                        block_crops = None
                        block_crops = BlockCrop.get_by_id(item['table_id']) 
                        if block_crops:
                            block_crops.delete_from_db()  
        return True
    
    @classmethod
    def get_block_industries(cls, block_id, district_id, state_id, user_id):
        bt_id = BlockTerritory.get_bt_id(block_id, district_id, state_id)
        return cls.get_industries(block_id, district_id, bt_id, user_id)

    def get_industries(block_id, district_id, bt_id, user_id):
        industries = BlockIndustry.get_by_bt_id(bt_id=bt_id)
        # results =[{'id': item.id, 'category':item.industry_sector } for item in industries]
        return industries
    
    def update_industries(json_data, user_id):
            bt_id = 0 
            for item in json_data: 
                bt_id = item['bt_id']
                block_industries = BlockIndustry(
                        industry_id=item['industry_id'],
                        allocation=item['allocation'],
                        unit = item['unit'],
                        count = item['count'],
                        bt_id=item['bt_id'],
                        is_approved=True, 
                        created_by=user_id)
                if item['allocation']>0:
                    block_industries.save_to_db()
                else:
                    if item['allocation']==0:
                        if item['table_id']:
                            block_industries = None
                            block_industries = BlockIndustry.get_by_id(item['table_id']) 
                            if block_industries:
                                block_industries.delete_from_db()  
                                
            # if there is no entry (all zeros) then enter a single row with zero                        
            filtered_json_data = [item for item in json_data if item['count'] > 0]
            if len(filtered_json_data) == 0:
                block_industries = BlockIndustry(
                        industry_id=1,
                        allocation=0,
                        unit = "HaM",
                        count = 0,
                        bt_id=bt_id,
                        is_approved=True, 
                        created_by=1)
                block_industries.save_to_db()
            return True

    # def update_industries(json_data, user_id):
    #     for item in json_data: 
    #         block_industries = BlockIndustry(
    #                 industry_id=item['industry_id'],
    #                 allocation=item['allocation'],
    #                 unit = item['unit'],
    #                 count = item['count'],
    #                 bt_id=item['bt_id'],
    #                 is_approved=True, 
    #                 created_by=user_id)
    #         if item['allocation']>0:
    #             block_industries.save_to_db()
    #         else:
    #             if item['allocation']==0:
    #                 if item['table_id']:
    #                     block_industries = None
    #                     block_industries = BlockIndustry.get_by_id(item['table_id']) 
    #                     if block_industries:
    #                         block_industries.delete_from_db()  
    #     return True

    @classmethod
    def get_surface_supply(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_surface_supply(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_surface_supply(block_id, district_id, bt_id, user_id):
        waterbodies = BlockWaterbody.get_by_bt_id(bt_id)
        if all(row['table_id'] is None for row in waterbodies):            
            surface_supply = BudgetData.get_surface_supply(block_id=block_id, district_id=district_id)
            if surface_supply:
                for item in surface_supply:
                    block_surface = BlockWaterbody(
                        wb_type_id = item['id'],
                        count = item['count'],
                        storage=item['value'],
                        bt_id=bt_id,
                        is_approved=False,
                        created_by=user_id
                    )
                    block_surface.save_to_db()
                waterbodies = BlockWaterbody.get_by_bt_id(bt_id)     
                return waterbodies
        else:
            return waterbodies
    
    def update_surface(json_data, user_id):
        for item in json_data: 
            block_surface = BlockWaterbody(
                    wb_type_id=item['wb_type_id'],
                    count=item['count'],
                    storage=item['storage'],
                    bt_id=item['bt_id'],
                    is_approved=True, 
                    created_by=user_id)
            if item['storage'] > 0:
                block_surface.save_to_db()
            else:
                if item['storage']==0:
                    if item['table_id']:
                        block_surface = None
                        block_surface = BlockWaterbody.get_by_id(item['table_id']) 
                        if block_surface:
                            block_surface.delete_from_db()  
        return True

    @classmethod
    def get_groundwater_supply(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_groundwater_supply(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_groundwater_supply(block_id, district_id, bt_id, user_id):
        groundwater_supply = BlockGround.get_by_bt_id(bt_id)
        if groundwater_supply:
            return groundwater_supply
        else: 
            groundwater_data = BudgetData.get_ground_supply(block_id, district_id)
            for item in groundwater_data:
                item = SimpleNamespace(**item)
                if item.name.lower() == 'extraction':
                    block_ground = BlockGround(extraction=item.value, 
                                            bt_id=bt_id, 
                                            is_approved=False, 
                                            created_by=user_id)
                    block_ground.save_to_db()
            groundwater_supply = BlockGround.get_by_bt_id(bt_id)
            return groundwater_supply
        
    def update_ground(json_data, user_id):
        for item in json_data: 
            if 'extraction' in item:
                id = item['id']
                block_ground = BlockGround.get_by_id(id)
                block_ground.extraction = item['extraction']
                block_ground.created_by = user_id
                block_ground.is_approved = True
                block_ground.update_db()
        return True
    
    @classmethod
    def get_rainfall_data(cls, block_id, district_id, state_id, user_id):
        bt_id = BlockTerritory.get_bt_id(block_id, district_id, state_id)
        return cls.get_or_insert_rainfall_data(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_rainfall_data(block_id, district_id, bt_id, user_id):
        rainfall = BlockRainfall.get_by_bt_id(bt_id)
        if not rainfall:            
            rainfall_supply = BudgetData.get_rainfall(block_id, district_id)
            if rainfall_supply:
                for item in rainfall_supply:
                    block_rainfall = BlockRainfall(normal=item['normal'],
                                                    actual=item['actual'],
                                                    month_year=datetime.strptime(item['month'], '%b-%y'),
                                                    bt_id=bt_id,
                                                    is_approved=False,
                                                    created_by=user_id)
                    block_rainfall.save_to_db()
                rainfall = BlockRainfall.get_by_bt_id(bt_id) 
                if rainfall:
                    return rainfall
                else:
                    return None
        else:
            return rainfall
                
    def update_rainfall(json_data, user_id):
        for item in json_data: 
            block_rainfall = BlockRainfall(
                    normal = item['normal'],
                    actual = item['actual'],
                    bt_id = item['bt_id'],
                    month_year=item['full_month_year'],
                    is_approved = True,
                    created_by=user_id)
            block_rainfall.save_to_db()
        return True
    
    @classmethod
    def get_lulc_supply(cls, block_id, district_id, state_id, user_id):
        bt_id = BlockTerritory.get_bt_id(block_id, district_id, state_id)
        return cls.get_or_insert_lulc(block_id, district_id, bt_id, user_id)

    def get_or_insert_lulc(block_id, district_id, bt_id, user_id):
        lulc = BlockLULC.get_by_bt_id(bt_id)
        if all(row['table_id'] is None for row in lulc):
            lulc_supply = LULCCensus.get_lulc(block_id=block_id, district_id=district_id)
            if lulc_supply:
                for item in lulc_supply:
                    if item['lulc_area']>0:
                        block_lulc = BlockLULC(
                            lulc_id=item['lulc_id'],
                            area=item['lulc_area'],
                            bt_id=bt_id,
                            is_approved=False,
                            created_by=user_id)
                        block_lulc.save_to_db()
                lulc = BlockLULC.get_by_bt_id(bt_id)     
                return lulc
        else:
            return lulc
            
    def update_lulc(json_data, user_id):
        for item in json_data: 
            block_lulc = BlockLULC(
                    lulc_id=item['lulc_id'],
                    area=item['area'],
                    bt_id=item['bt_id'],
                    is_approved=True, 
                    created_by=user_id)
            if item['area'] > 0:
                block_lulc.save_to_db()
            else:
                if item['area']==0:
                    if item['table_id']:
                        block_lulc = None
                        block_lulc = BlockLULC.get_by_id(item['table_id']) 
                        if block_lulc:
                            block_lulc.delete_from_db()  
        return True
    
    @classmethod
    def get_water_transfer(cls, block_id, district_id, state_id, user_id):
        bt_id = BlockTerritory.get_bt_id(block_id, district_id, state_id)
        return cls.get_or_insert_water_transfer(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_water_transfer(block_id, district_id, bt_id, user_id):
        water_transfer = BlockWaterTransfer.get_by_bt_id(bt_id)
        return water_transfer
    
    def update_water_transfer(json_data, user_id):
        for item in json_data: 
            block_water_transfer = BlockWaterTransfer(
                        transfer_quantity=item['quantity'],
                        transfer_type_id=item['type_id'],
                        transfer_sector_id=item['sector_id'],
                        bt_id=item['bt_id'],
                        is_approved=True,
                        created_by=user_id)
            if item['quantity'] > 0:
                    block_water_transfer.save_to_db()
            else:
                if item['quantity']==0:
                    if item['table_id']:
                        block_water_transfer = None
                        block_water_transfer = BlockWaterTransfer.get_by_id(item['table_id'])
                        if block_water_transfer:
                            block_water_transfer.delete_from_db()      
        return True
    
    @classmethod
    def get_progress_status(cls, block_id, district_id, state_id):
        bt_id = cls.get_bt_id(block_id, district_id, state_id)
        status = BlockTerritory.get_status_by_bt_id(bt_id)
        query_result = status[0]  # Assuming only one result from the query
        categories = ['Human', 'Livestocks', 'Crops',  'Industry', 'Surface', 'Groundwater', 'LULC', 'Rainfall', 'Water Transfer']
        category_urls = ['human', 'livestocks', 'crops', 'industries', 'surface', 'ground', 'lulc', 'rainfall', 'transfer']

        progress_status = [
            {
                'id': idx + 1,
                'category': category,
                'status': bool(query_result[idx]),
                'url': url_for(f'desktop.{category_urls[idx]}')
            }
            for idx, category in enumerate(categories)
        ]
        return progress_status
    