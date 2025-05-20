from flask import Blueprint, render_template, url_for


blp = Blueprint('routes','routes')

@blp.route('/')
def home():
    appList = [
        {'name': 'Training', 'route':'/itraining', 'image_url':url_for('static', filename='assets/images/training.png')},
        {'name': 'River', 'route':'/iriver', 'image_url':url_for('static', filename='assets/images/river.png')},
        {'name': 'Land', 'route':'/iland', 'image_url':url_for('static', filename='assets/images/land.png')},
        {'name': 'Water', 'route':'/iwater', 'image_url':url_for('static', filename='assets/images/water.png')},
        {'name': 'MaP', 'route':'/imap', 'image_url':url_for('static', filename='assets/images/map.png')},
        {'name': 'Climate', 'route':'/iclimate', 'image_url':url_for('static', filename='assets/images/climate.png')},
        {'name': 'Saksham', 'route':'/isaksham', 'image_url':url_for('static', filename='assets/images/gis.png')},
        {'name': 'RbM', 'route':'/irbm', 'image_url':url_for('static', filename='assets/images/rbm.png')},
        {'name': 'Finance', 'route':'/ifinance', 'image_url':url_for('static', filename='assets/images/finance.png')},
        {'name': 'Bot', 'route':'/ibot', 'image_url':url_for('static', filename='assets/images/waterbot_bg.png')},
        {'name': 'Carbon', 'route':'icarbon','image_url':url_for('static', filename='assets/images/carbon.png')},
        {'name': 'Work', 'route':'iwork','image_url':url_for('static', filename='assets/images/work.png')}
    ]
    return render_template('index.html', appList = appList)

@blp.route('/favicon.ico')
def favicon():
    return url_for('static', filename='assets/favicon.ico') 