from flask import Blueprint, render_template


blp = Blueprint('routes', __name__)

@blp.route('/')
def home():
    carousel_images = [{'source':'https://images.pexels.com/photos/2166711/pexels-photo-2166711.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Support to Water Vision 2047', 'index':0},
                       {'source':'https://images.pexels.com/photos/709552/pexels-photo-709552.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Catchment area treatment', 'index':1},
                       {'source':'https://images.pexels.com/photos/206359/pexels-photo-206359.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Water Governance​', 'index':2},
                       {'source':'https://images.pexels.com/photos/158063/bellingrath-gardens-alabama-landscape-scenic-158063.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Water Use Efficiency​', 'index':3},
                       {'source':'https://images.pexels.com/photos/247599/pexels-photo-247599.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Water Storage & Management', 'index':4},
                       {'source':'https://images.pexels.com/photos/388415/pexels-photo-388415.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Jan Bhagidari​', 'index':5},
                       {'source':'https://images.pexels.com/photos/1144176/pexels-photo-1144176.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Climate Resilience & River Health', 'index':6},
                       {'source':'https://images.pexels.com/photos/268533/pexels-photo-268533.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Source Sustainability - Surface Water​', 'index':7},
                       {'source':'https://images.pexels.com/photos/259280/pexels-photo-259280.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                        'title':'Source Sustainability - Ground Water', 'index':8}]
    return render_template('index.html', carousel_images=carousel_images)

@blp.route('/contactus')
def contact_us():
    return render_template('contact_us.html')

@blp.route('/what_we_do')
def what_we_do():
    return render_template('what_we_do.html')

@blp.route('/who_we_are')
def who_we_are():
    return render_template('who_we_are.html')