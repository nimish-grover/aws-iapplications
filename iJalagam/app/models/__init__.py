# Master Tables
from iJalagam.app.models.states import State
from iJalagam.app.models.districts import District
from iJalagam.app.models.blocks import Block
from iJalagam.app.models.villages import Village

from iJalagam.app.models.territory import TerritoryJoin

# Census Masters
from iJalagam.app.models.population import Population
from iJalagam.app.models.livestocks import Livestock
from iJalagam.app.models.lulc import LULC
from iJalagam.app.models.crops import Crop
from iJalagam.app.models.waterbody import WaterbodyType
from iJalagam.app.models.industries import Industry

# Census Data Tables
from iJalagam.app.models.livestocks_census import LivestockCensus
from iJalagam.app.models.crop_census import CropCensus
from iJalagam.app.models.population_census import PopulationCensus
from iJalagam.app.models.waterbody_census import WaterbodyCensus
from iJalagam.app.models.lulc_census import LULCCensus
from iJalagam.app.models.groundwater_extraction import GroundwaterExtraction
from iJalagam.app.models.rainfall import Rainfall
from iJalagam.app.models.strange_table import StrangeTable


# Block Data Tables
from iJalagam.app.models.block_territory import BlockTerritory
from iJalagam.app.models.block_livestocks import BlockLivestock
from iJalagam.app.models.block_pop import BlockPop
from iJalagam.app.models.block_crops import BlockCrop
from iJalagam.app.models.block_industries import BlockIndustry
from iJalagam.app.models.block_ground import BlockGround
from iJalagam.app.models.block_lulc import BlockLULC


from iJalagam.app.models.block_rainfall import BlockRainfall
from iJalagam.app.models.block_transfer_type import BlockTransferType
from iJalagam.app.models.block_transfer_sector import BlockTransferSector
from iJalagam.app.models.block_transfer import BlockWaterTransfer



# Auth Tables
from iJalagam.app.models.users import User