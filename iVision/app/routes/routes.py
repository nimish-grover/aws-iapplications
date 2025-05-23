from flask import Blueprint, render_template


blp = Blueprint('routes', __name__)

@blp.route('/')
def home():
    carousel_images = [
    {
        'source': 'https://images.pexels.com/photos/2166711/pexels-photo-2166711.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Support to Water Vision 2047',
        'index': 0
    },
    {
        'source': 'https://images.pexels.com/photos/709552/pexels-photo-709552.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Catchment area treatment',
        'index': 1,
        'quote': "Water is the mother of the vine, the nurse and fountain of fecundity, the adorner and the refresher of the world.",
        'author': "Charles Mackay"
    },
    {
        'source': 'https://images.pexels.com/photos/206359/pexels-photo-206359.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Water Governance​',
        'index': 2,
        'quote': "The earth, the air, the land, and the water are not an inheritance from our forefathers but a loan from our children.",
        'author': "Mahatma Gandhi"
    },
    {
        'source': 'https://images.pexels.com/photos/158063/bellingrath-gardens-alabama-landscape-scenic-158063.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Water Use Efficiency​',
        'index': 3,
        'quote': "Rich or poor in water. It's the only currency that really matters.",
        'author': "The Dharma Trails"
    },
    {
        'source': 'https://images.pexels.com/photos/247599/pexels-photo-247599.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Water Storage & Management',
        'index': 4,
        'quote': "By means of water, we give life to everything.",
        'author': "The Quran"
    },
    {
        'source': 'https://images.pexels.com/photos/388415/pexels-photo-388415.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Jan Bhagidari​',
        'index': 5,
        'quote': '''We buy a bottle of water in the city, where clean water comes out of the taps. You know, back in 1965, 
        if someone said to the average person, ‘You know, in thirty years you're going to buy water in plastic bottles and pay more for that water than for gasoline,’ 
        everybody would look at you like you're completely out of your mind.''',
        'author': "Paul Watson"
    },
    {
        'source': 'https://images.pexels.com/photos/1144176/pexels-photo-1144176.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Climate Resilience & River Health',
        'index': 6,
        'quote': "Water seeks its own level, and water rises collectively.",
        'author': "Julia Cameron"
    },
    {
        'source': 'https://images.pexels.com/photos/268533/pexels-photo-268533.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Source Sustainability - Surface Water​',
        'index': 7,
        'quote': "Thousands have lived without love, not one without water.",
        'author': "W. H. Auden"
    },
    {
        'source': 'https://images.pexels.com/photos/259280/pexels-photo-259280.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'title': 'Source Sustainability - Ground Water',
        'index': 8,
        'quote': "When the well is dry, we know the worth of water.",
        'author': "Benjamin Franklin"
    }
]

    return render_template('index.html', carousel_images=carousel_images)

@blp.route('/contactus')
def contact_us():
    return render_template('contact_us.html')

@blp.route('/about_project')
def about_project():
    return render_template('about_project.html')

@blp.route('/who_we_are')
def who_we_are():
    return render_template('who_we_are.html')

@blp.route('/team')
def team():
    return render_template('team.html')

@blp.route('/mgnrega')
def mgnrega():
    return render_template('mgnrega.html')

@blp.route('/conservation')
def conservation():
    return render_template('conservation.html')

@blp.route('/partners')
def partners():
    return render_template('partners.html')
