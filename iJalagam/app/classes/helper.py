from itertools import cycle
from flask import url_for

from iJalagam.app.models.states import State
from iJalagam.app.models.users import User


class HelperClass():
    COLORS = ['#5470c6','#91cc75','#fac858','#ee6666','#73c0de','#3ba272','#fc8452','#9a60b4']

    @classmethod
    def get_dashboard_menu(cls):
        progress_data = State.get_all_states_status()
        chart_data = []
        
        color_cycle = cycle(cls.COLORS)
        for item in progress_data:
            if item['completed']:
                color = next(color_cycle)
                chart_data.append({'state_name':item['state_name'], 'completed':item['completed'],'block_name':item['block_name'],
                                'color':color,'district_name':item['district_name'],'percentage':str(item['completed'])+'%',
                                'state_short_name':item['state_short_name']})
        return chart_data
    
    @classmethod
    def get_card_data(cls,chart_data):
        completed_blocks = sum(1 for item in chart_data if item.get('completed') == 100)
        user_status = User.get_active_count()
        return [
            {'title': 'Users Active', 'value': cls.format_value(user_status['active_users']), 'icon': 'fa-user-gear'},
            {'title': 'Users Registered', 'value': cls.format_value(user_status['active_users']+user_status['inactive_users']), 'icon': 'fa-user-check'},
            {'title': 'Blocks In-Progress', 'value': cls.format_value(len(chart_data)-completed_blocks), 'icon': 'fa-gears'},
            {'title': 'Blocks Completed', 'value': cls.format_value(completed_blocks), 'icon': 'fa-list-check'}]
    
    def format_value(value):
        if value < 10:
            return f"{value:02d}"
        return str(value)

    def get_supply_menu():
        return [
            { "route" : url_for('.status'), "label":"back", "icon":"fa-solid fa-left-long"},
            { "route" : url_for('.surface'), "label":"surface", "icon":"fa-solid fa-water"},
            { "route" : url_for('.ground'), "label":"ground", "icon":"fa-solid fa-arrow-up-from-ground-water"},
            { "route" : url_for('.lulc'), "label":"lulc", "icon":"fa-solid fa-cloud-showers-water"},
            { "route" : url_for('.rainfall'), "label":"rainfall", "icon":"fa-solid fa-cloud-rain"},
        ]

    def get_demand_menu():
        return [
            { "route" : url_for('.status'), "label":"back", "icon":"fa-solid fa-left-long"},
            { "route" : url_for('.human'), "label":"human", "icon":"fa-solid fa-people-roof"},
            { "route" : url_for('.livestocks'), "label":"livestock", "icon":"fa-solid fa-paw"},
            { "route" : url_for('.crops'), "label":"crops", "icon":"fa-brands fa-pagelines"},
            { "route" : url_for('.industries'), "label":"industries", "icon":"fa-solid fa-industry"},
        ]
    
    def get_main_menu():
        return [
            { "route" : url_for('mobile.index'), "label":"home", "icon":"fa-solid fa-house"},
            { "route" : url_for('desktop.status'), "label":"status", "icon":"fa-solid fa-list-check"},
            { "route" : url_for('desktop.human'), "label":"demand", "icon":"fa-solid fa-chart-line"},
            { "route" : url_for('desktop.surface'), "label":"supply", "icon":"fa-solid fa-glass-water-droplet"},
            { "route" : url_for('desktop.transfer'), "label":"transfer", "icon":"fa-solid fa-arrow-right-arrow-left"},
        ]
    
    def get_admin_menu():
        return [
            { "route" : url_for('.dashboard'), "label":"dashboard", "icon":"fa-solid fa-gauge"},
            { "route" : url_for('.approve'), "label":"approve", "icon":"fa-solid fa-list-check"},
            { "route" : url_for('.progress'), "label":"progress", "icon":"fa-solid fa-bars-progress"}
        ]
    
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