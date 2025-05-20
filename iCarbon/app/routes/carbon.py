
from flask import render_template, request
from flask_smorest import Blueprint

blp = Blueprint('carbon','carbon','calculate carbon sequestration')

@blp.route('/', methods=['GET','POST'])
def carbon():
    
    if request.method=='POST':
        diameter = request.form.get('diameter_of_tree')
        height = request.form.get('height_of_tree')
        age = request.form.get('age_of_tree')
        trees = request.form.get('number_of_trees')
        above_ground_mass = 0.25 * float(diameter) * float(diameter) * float(height)
        below_ground_mass = 0.2 * above_ground_mass
        total_biomass = above_ground_mass + below_ground_mass
        total_dry_weight = total_biomass * 0.725
        total_carbon = total_dry_weight * 0.5
        carbon_sequestered = total_carbon * 3.67
        annual_cs = carbon_sequestered/float(age)
        return render_template('carbon.html', 
                               annual_cs = round(annual_cs,2), 
                               carbon_sequestered= round(carbon_sequestered,2),
                               show_calc=False)
        
    return render_template('carbon.html', show_calc=True)

# To accurately determine the amount of CO2 absorbed by trees, two critical measurements are taken directly from the tree: its diameter, measured in cm, and its height, measured in meters. These measurements are essential for calculating both the Above-Ground Biomass (AGB) and Below-Ground Biomass (BGB). The calculation of these biomass values is based on a specific formula that incorporates these two parameters 9 [3].

# AGB = 0.25 x D2 x H

# Where:

# AGB: Above-Ground Biomass (pounds).
# D: tree diameter measured at 1.37 meters from the ground (inches). This measurement is globally used as a standard to get a better result. However, if your tree is below 1.37 meters, you can still use the formula.
# H: tree height (feet).
# The overall green weight of the biomass is estimated to be 120% of the AGB value, based on the assumption that the BGB, which comprises the tree’s root system, accounts for approximately 20% of the AGB [3]. Therefore, BGB can be calculated as follows:

# BGB = 0.2 × AGB

# From these formulas, we can calculate the total biomass from a tree:

# Total Biomass (TB) = AGB + BGB = AGB + 0.2 x AGB = 1.2 × AGB

# On average, a tree consists of 72.5% dry matter and 27.5% moisture content. To calculate the tree’s dry weight, we could multiply the total weight of the tree by 72.5%.

# Total Dry Weight (TDW) = TB × 0.725

# Carbon occupies 50% of the total dry weight. Therefore,

# Total Carbon (TC) = TDW × 0.5

# With the value of total carbon, we can calculate the value of CO2 equivalent sequestered on a tree. CO2 has one molecule of Carbon and two molecules of Oxygen. The atomic weight of Carbon is 12u, and the atomic weight of Oxygen is 16u. The weight of CO2 in trees is determined by the ratio of CO2 to C is 44/12 = 3.67. Therefore, to determine the weight of carbon dioxide sequestered in the tree, multiply the weight of carbon in the tree by 3.67.

# CO2 weight = TC × 3.67

# It is worth noting that the CO2 weight above represents the CO2 sequestered in the entire lifetime of the tree. To ascertain the annual or yearly rate of CO2 sequestration, divide the total weight of CO2 absorbed by the tree’s age