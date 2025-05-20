# Master Tables
from iJal.app.models.states import State
from iJal.app.models.districts import District
from iJal.app.models.blocks import Block
from iJal.app.models.villages import Village

from iJal.app.models.territory import TerritoryJoin

# Census Masters
from iJal.app.models.population import Population
from iJal.app.models.livestocks import Livestock
from iJal.app.models.lulc import LULC
from iJal.app.models.crops import Crop
from iJal.app.models.waterbody import WaterbodyType
from iJal.app.models.industries import Industry

# Census Data Tables
from iJal.app.models.livestocks_census import LivestockCensus
from iJal.app.models.crop_census import CropCensus
from iJal.app.models.population_census import PopulationCensus
from iJal.app.models.waterbody_census import WaterbodyCensus
from iJal.app.models.lulc_census import LULCCensus
from iJal.app.models.groundwater_extraction import GroundwaterExtraction
from iJal.app.models.rainfall import Rainfall
from iJal.app.models.strange_table import StrangeTable


# Block Data Tables
from iJal.app.models.block_territory import BlockTerritory
from iJal.app.models.block_livestocks import BlockLivestock
from iJal.app.models.block_pop import BlockPop
from iJal.app.models.block_crops import BlockCrop
from iJal.app.models.block_industries import BlockIndustry
from iJal.app.models.block_ground import BlockGround
from iJal.app.models.block_lulc import BlockLULC


from iJal.app.models.block_rainfall import BlockRainfall
from iJal.app.models.block_transfer_type import BlockTransferType
from iJal.app.models.block_transfer_sector import BlockTransferSector
from iJal.app.models.block_transfer import BlockWaterTransfer



# Auth Tables
from iJal.app.models.users import User