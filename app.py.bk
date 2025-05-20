# app.py

from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from iTraining import app as Training
from iWater import app as Water
from iCore import app as Core
from iFinance import app as Finance

application = DispatcherMiddleware(Core, {
    '/iwater': Water,
    '/itraining': Training,
    '/ifinance': Finance,
})

# application = iCore