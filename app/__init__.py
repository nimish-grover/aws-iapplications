# app.py

from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from iTraining import app as Training
from iWater import app as Water
from iCore import app as Core
from iFinance import app as Finance
from iBot import app as Waterbot
from iLand import app as Land
from iCarbon import app as Carbon
from iSaksham import app as Saksham
from eSaksham import app as eSaksham
from iWork import app as Work
from iJalagam import app as Jalagam
from iJal import app as Jal
from iSchool import app as School

application = DispatcherMiddleware(Core, {
    '/iwater': Water,
    '/itraining': Training,
    '/ifinance': Finance,
    '/ibot': Waterbot,
    '/iland': Land,
    '/icarbon':Carbon,
    '/isaksham':Saksham,
    '/esaksham':eSaksham,
    '/iwork':Work,
    '/ijal': Jalagam,
    '/ijalagam': Jal,
    '/talent':School
})

# application = iCore