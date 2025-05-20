from collections import Counter
from datetime import date
from datetime import datetime
from flask import render_template, request, session,url_for,redirect,flash
from flask_smorest import Blueprint, abort
from iFinance.app.db_extensions import *
from iFinance.app.models.project import projectDataModel, pywfModel
from iFinance.app.models.financial import  FinancialDataModel
from iFinance.app.schemas import FinancialDataSchema
from flask_login import login_required, current_user


blp = Blueprint("dashboard", "dashboards",
                description="html pages for financial dashboard")



@blp.route("/", methods=['GET', 'POST'])
@blp.route("/dashboard", methods=['GET', 'POST'])
@login_required
def financials():
    global years,projectlist
    pywf = pywfModel.get_all_projects()
    years=[]
    project_ids = []
    for project in pywf:
        if project.year not in years:
            years.append(project.year)
        if project.projects_id not in project_ids:
            project_ids.append(project.projects_id)

    years.sort()
    current_year = datetime.now().year
    # Get all projects of NRMAe
    projects = projectDataModel.get_all_projects()
    # create a list of projects to display on dashboard
    projectlist=[]

    for project in projects:
        if project.id in project_ids:
            projectlist.append(project.shortname)
    projectdict={}
    yeardict={}

    for year in years:
        dict_project=create_dict(projectlist)
        project_data=()
        sel_year = year
        selected_year = '2023'
        if projectdict:
            projectdict.clear()
        if project_data:
            project_data.clear()
    # iterate over list and perform fuctions 
        for project_item in projects:
            if project_item.shortname in projectlist:
                #projectdict['name'] = project_item['shortname']
                selected_project = project_item.id

                # get specific project requirement
                project = projectDataModel.find_by_id(int(selected_project))
                # get project financials - month wise planned and actual expenses of the project
                project_financials = FinancialDataModel.find_by_project_id_and_year(
                    selected_year, selected_project)

                # make the financial data table with cummulatives and gaps
                month_on_month = []
                twelve_months = get_calendar_months()
                for row in project_financials:
                    monthly_expenses = {}
                    for mon in twelve_months:
                        if (row.month_year.strftime('%b') == mon['short_month']):
                            monthly_expenses['month_only'] = mon['short_month']
                            monthly_expenses['month_year'] = row.month_year
                            monthly_expenses['planned'] = round(row.planned, 2)
                            monthly_expenses['actuals'] = round(row.actuals, 2)
                            monthly_expenses['gap'] = monthly_expenses['actuals'] - \
                                monthly_expenses['planned']
                            monthly_expenses['percent'] = monthly_expenses['gap'] / \
                                monthly_expenses['planned']
                            if (len(month_on_month) == 0):
                                monthly_expenses['cumm_planned'] = monthly_expenses['planned']
                                monthly_expenses['cumm_actuals'] = monthly_expenses['actuals']
                            else:
                                monthly_expenses['cumm_planned'] = month_on_month[len(
                                    month_on_month)-1]['cumm_planned']+monthly_expenses['planned']
                                monthly_expenses['cumm_actuals'] = month_on_month[len(
                                    month_on_month)-1]['cumm_actuals'] + monthly_expenses['actuals']
                            monthly_expenses['cumm_gap'] = monthly_expenses['cumm_actuals'] - \
                                monthly_expenses['cumm_planned']
                            monthly_expenses['cumm_percent'] = monthly_expenses['cumm_gap'] / \
                                monthly_expenses['cumm_planned']
                            break
                    if monthly_expenses:
                        month_on_month.append(monthly_expenses)
                # prepare mixed chart labels and dataset]
                # arrays to store data for the whole calendar year
                labels_month, planned, actuals, cumm_planned, cumm_actuals = [], [], [], [], []
                # arrays to store data till date (hence td)
                labels_td, planned_td, actuals_td, cumm_planned_td, cumm_actuals_td = [], [], [], [], []
                for idx, row in enumerate(month_on_month):
                    # fill the dataset and labels for the whole calendar year
                    labels_month.append(row['month_only'])
                    planned.append(row['planned'])
                    actuals.append(row['actuals'])
                    cumm_planned.append(row['cumm_planned'])
                    cumm_actuals.append(row['cumm_actuals'])
                    # fill the dataset and labels array till the current month
                    if idx == 0:
                        labels_td.append(row['month_only'])
                        planned_td.append(row['planned'])
                        actuals_td.append(row['actuals'])
                        cumm_planned_td.append(row['cumm_planned'])
                        cumm_actuals_td.append(row['cumm_actuals'])
                    elif (month_on_month[idx-1]['cumm_actuals'] < row['cumm_actuals']):
                        labels_td.append(row['month_only'])
                        planned_td.append(row['planned'])
                        actuals_td.append(row['actuals'])
                        cumm_planned_td.append(row['cumm_planned'])
                        cumm_actuals_td.append(row['cumm_actuals'])
                
                total_planned = round(sum(planned_td), 2)
                total_actuals = round(sum(actuals_td), 2)
                total_gap = total_actuals - total_planned
                spent_percent = 'Overspent' if total_gap > 0 else 'Underspent'

                if total_planned and total_actuals:
                    percentage = (total_actuals/total_planned)*100
                else:
                    percentage = 0
                #project_data={"name":project_item['shortname'],"total_planned":'{:,.0f}'.format(total_planned),"total_gap": '{:,.0f}'.format(total_gap),
                           # "total_actuals":'{:,.0f}'.format(total_actuals),"percentage": '{:,.0f}'.format(percentage),"year":sel_year}
                project_data=(project_item.shortname,'{:,.0f}'.format(total_planned),'{:,.0f}'.format(total_gap),'{:,.0f}'.format(total_actuals),'{:,.0f}'.format(percentage),sel_year)
                dict_project[project_item.shortname]=project_data
                project_data=()
                
                yeardict[year] = dict_project[project_item.shortname]
            
    return render_template('finance_dashboard.html',
                           years=years,current_year=current_year,
                           name = current_user.name
                           )


@blp.route("/all_projects/<project>")
@login_required
def projects(project):
    # Get all projects of NRMAe
    if project == "All":
        projects = projectDataModel.get_all_projects()
    else:
        projects = projectDataModel.find_by_type(project)
    # datetime.today().strftime('%Y-%m-%d')
    
    today_date = datetime.strptime(date.today().strftime('%b-%y'),'%b-%y')
    new_projects = []
    
    for idx, row in enumerate(projects):
        project_end_date = datetime.strptime(row.to_date,'%b-%y')
        project_start_date = datetime.strptime(row.from_date,'%b-%y')
        if project_end_date >= today_date and project_start_date <= today_date:
            new_projects.append(row)

    unique_types=[]
    for p in projects:
        if p.project_type not in unique_types:
            unique_types.append(p.project_type)

    if len(new_projects) != 0:
        return render_template('nrmae_projects.html', projects=new_projects,name=current_user.name,project = project)
    else:
        flash("There are no projects in "+project+" category")
        return render_template('nrmae_projects.html', projects=new_projects,name=current_user.name,project = project)
     

@blp.route("/projects", methods=['GET', 'POST'])
@login_required
def projects():
    # Get all projects of NRMAe
    projects = projectDataModel.get_all_projects()
    # datetime.today().strftime('%Y-%m-%d')
    today_date = datetime.strptime(date.today().strftime('%b-%y'),'%b-%y')
    new_projects = []
    volume = 0
    bilateral_volume = 0
    sewoh_volume = 0
    dpp_volume = 0
    sewoh_numbers = 0    
    bilateral_numbers = 0
    dpp_numbers = 0
    for idx, row in enumerate(projects):
        project_end_date = datetime.strptime(row.to_date,'%b-%y')
        project_start_date = datetime.strptime(row.from_date,'%b-%y')
        if project_end_date >= today_date and project_start_date <= today_date:
            new_projects.append(row)
            volume = volume + float(row.comm_value)
            # number_of_projects = number_of_projects + 1
            if row.project_type.lower() == 'sewoh':
                sewoh_volume = sewoh_volume + float(row.comm_value)
                sewoh_numbers = sewoh_numbers + 1
            elif row.project_type.lower()=='bilateral':
                bilateral_volume = bilateral_volume + float(row.comm_value)
                bilateral_numbers = bilateral_numbers + 1

    unique_types=[]
    for p in projects:
        if p.project_type not in unique_types:
            unique_types.append(p.project_type)

    project_types = []
    for type in unique_types:
        project_type={}
        project_type['project_type']=type.upper()
        project_type['volume'] = 0
        project_type['numbers'] = 0
        for p in new_projects:
            if type.lower() == p.project_type.lower():
                project_type['volume'] = project_type['volume'] + float(p.comm_value)
                project_type['numbers'] = project_type['numbers'] + 1
        project_types.append(project_type)
    
    chartdata = {}
    chartdata['types'] = list_to_array('project_type', project_types)
    chartdata['comm_values'] = list_to_array('volume', project_types)
    chartdata['project_numbers'] = list_to_array('numbers', project_types)

    if request.method=='POST':            
        # set the selected project in session
        if "filter_project" in session:
            selected_project = session["filter_project"]
        if "projectName" in request.form:
            selected_project = int(request.form['projectName'])
            session["filter_project"] = selected_project
    else:  # else initiatize the session values
        selected_project = 1
        session["filter_project"] = selected_project
    project_desc = projectDataModel.find_by_id(int(selected_project))

    return render_template('project_dashboard.html', projects=new_projects,name=current_user.name,
                           total_commission=volume/1000000,
                           total_bilateral = bilateral_volume/1000000,
                           total_sewoh = sewoh_volume/1000000,
                           chartdata = chartdata,
                           project_desc = project_desc,
                           filter_project = selected_project)

def list_to_array(column_name, object_list):
    column_list =[]
    for row in object_list:
        column_list.append(row[column_name])
    return column_list

def get_calendar_months():
    twelve_months = []
    for i in range(1, 13):
        year = date.today().year
        temp_date = date(year, i, 1)
        single_month = {}
        single_month['int_month'] = temp_date.strftime('%m')
        single_month['short_month'] = temp_date.strftime('%b')
        single_month['long_month'] = temp_date.strftime('%B')
        twelve_months.append(single_month)
    return twelve_months

def convert_date_format(date_string):
    # Parse the input date string
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    # Format the date as '%b-%y'
    formatted_date = date_object.strftime('%b-%y')
    return formatted_date

def revert_date(date_string):
    # Parse the input date string
    date_object = datetime.strptime(date_string, '%b-%y')
    # Format the date as '%b-%y'
    formatted_date = date_object.strftime('%Y-%m-%d')
    return formatted_date

def change_date_format(date_str):
    try:
        # Parse the input date string to a datetime object
        date_obj = datetime.strptime(date_str, "%B %Y")

        # Format the datetime object to the desired format
        formatted_date = date_obj.strftime("%Y-%m-%d")

        return formatted_date
    except ValueError:
        # Handle the case where the input date string is not in the expected format
        return "Invalid Date Format"

def get_year_month(date_str):
    try:
        # Parse the input date string to a datetime object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # Extract month and year from the datetime object
        month = date_obj.strftime("%B")
        year = date_obj.strftime("%Y")

        return int(year), month
    except ValueError:
        # Handle the case where the input date string is not in the expected format
        return None

def create_dict(projects):
    dict_project = {}
    for project in projects:
       dict_project[project]={}
    return dict_project

def format_labels(data):
    formatted_labels = []
    for value in data:
        if value < 0:
            formatted_labels.append('0K')
        elif value < 1000:
            formatted_labels.append('0.0K')
        else:
            formatted_labels.append(f'{value / 1000:.1f}K')
    return formatted_labels

def get_tag(pywf,project_id,year):
    data=[]
    for project in pywf:
        if project.id==project_id:
            data.append(project)

    for project in data:
        if year == project.year:
            return project['tag']
    
    return "year"+str(len(data)+1)

@blp.route('/get_finance/<project_id>/<cost_type>/<month>/<year>')
def get_finance(project_id,cost_type,month,year):
    json_data={}
    date = month +' '+year
    month_year=change_date_format(date)
    project = FinancialDataModel.find_by_project_id_minor_head_and_month(project_id,month_year,cost_type)
    if project:
        json_data['actual']=project['actuals']
        json_data['planned']=project['planned']
        return json_data
    else:
        return 'False'

@blp.route("/project/<name>/<year>", methods=['GET', 'POST'])
@login_required
def project(name,year):

    # Get all projects of NRMAe
    projects = projectDataModel.get_all_projects()
    # create a list of projects to display on dashboard
    
    projectdict={}
    selected_year=year
    projectfinance={}
    labels={'Fixed Cost':'fc','Running Cost':'rc','Obligos Cost':'ob','Activities Cost':'ac','Cummulative':'cumm'}

    # iterate over list and perform fuctions 
    for project_item in projects:
        if project_item.shortname == name:
            #projectdict['name'] = project_item['shortname']
            selected_project = project_item.id

            # get specific project requirement
            project = projectDataModel.find_by_id(int(selected_project))
            # get project financials - month wise planned and actual expenses of the project
            project_financials = FinancialDataModel.find_by_project_id_and_year(
                selected_year, selected_project)

            # make the financial data table with cummulatives and gaps
            month_on_month = []
            twelve_months = get_calendar_months()
            for row in project_financials:
                monthly_expenses = {}
                for mon in twelve_months:
                    if (row.month_year.strftime('%b') == mon['short_month']):
                        monthly_expenses['month_only'] = mon['short_month']
                        monthly_expenses['month_year'] = row.month_year
                        monthly_expenses['planned'] = round(row.planned, 2)
                        monthly_expenses['actuals'] = round(row.actuals, 2)
                        total_gap=monthly_expenses['actuals']-monthly_expenses['planned']
                        monthly_expenses['gap'] = total_gap
                        monthly_expenses['percent'] = monthly_expenses['gap'] / \
                            monthly_expenses['planned']
                        monthly_expenses['spent']='Overspent' if total_gap > 0 else 'Underspent'
                        if (len(month_on_month) == 0):
                            monthly_expenses['cumm_planned'] = monthly_expenses['planned']
                            monthly_expenses['cumm_actuals'] = monthly_expenses['actuals']
                        else:
                            monthly_expenses['cumm_planned'] = month_on_month[len(
                                month_on_month)-1]['cumm_planned']+monthly_expenses['planned']
                            monthly_expenses['cumm_actuals'] = month_on_month[len(
                                month_on_month)-1]['cumm_actuals'] + monthly_expenses['actuals']
                        monthly_expenses['cumm_gap'] = monthly_expenses['cumm_actuals'] - \
                            monthly_expenses['cumm_planned']
                        monthly_expenses['cumm_percent'] = monthly_expenses['cumm_gap'] / \
                            monthly_expenses['cumm_planned']
                        break
                if monthly_expenses and monthly_expenses['actuals']>0:
                    month_on_month.append(monthly_expenses)
            # prepare mixed chart labels and dataset]
            # arrays to store data for the whole calendar year
            labels_month, planned, actuals, cumm_planned, cumm_actuals = [], [], [], [], []
            # arrays to store data till date (hence td)
            labels_td, planned_td, actuals_td, cumm_planned_td, cumm_actuals_td = [], [], [], [], []
            for idx, row in enumerate(month_on_month):
                # fill the dataset and labels for the whole calendar year
                labels_month.append(row['month_only'])
                planned.append(row['planned'])
                actuals.append(row['actuals'])
                cumm_planned.append(row['cumm_planned'])
                cumm_actuals.append(row['cumm_actuals'])
                # fill the dataset and labels array till the current month
                if idx == 0:
                    labels_td.append(row['month_only'])
                    planned_td.append(row['planned'])
                    actuals_td.append(row['actuals'])
                    cumm_planned_td.append(row['cumm_planned'])
                    cumm_actuals_td.append(row['cumm_actuals'])
                elif (month_on_month[idx-1]['cumm_actuals'] < row['cumm_actuals']):
                    labels_td.append(row['month_only'])
                    planned_td.append(row['planned'])
                    actuals_td.append(row['actuals'])
                    cumm_planned_td.append(row['cumm_planned'])
                    cumm_actuals_td.append(row['cumm_actuals'])
            # get project year on year data and transpose it for display
            pywf = pywfModel.find_by_projects_id(selected_project)
            year_on_year = []
            hasYoyData = False
            if len(pywf) > 0:
                column_names = pywf[0].__table__.columns.keys()
                if len(column_names) > 0:
                    hasYoyData = True
                    for i in range(len(column_names)):
                        if(i > 2):
                            if(column_names[i] != 'projects_id'):
                                row = {}
                                row['description'] = column_names[i]
                                for j in range(len(pywf)):
                                    row[str(getattr(pywf[j], 'year'))] = getattr(
                                        pywf[j], column_names[i])
                                year_on_year.append(row)
            # create an array with count project['projectType'] from the list of project
            # Using the Counter class from the collections module to count the project types
            project_type_count = Counter(
                project.project_type for project in projects)

            # Converting the counter to a dictionary, if needed
            project_type_count_dict = dict(project_type_count)
            # Colors for the Project_types doughnut chart
            project_type_colors = ["#116DEE", "#EE9211",
                                    "#6346B9", "#9CB946", "#B94653"]

            ### DOUGHNUT CHART ###
            # populate the labels and data for doughnut charts
            doughnutChart_labels, doughnutChart_data, doughnutChart_title = [], [], ""
            # extract key-value pair from dictionary
            for key, value in project_type_count_dict.items():
                doughnutChart_labels.append(str(key))
                doughnutChart_data.append(value)
            doughnutChart_title = "No. of Projects"
            # prepare the totals for landing page
            total_planned = round(sum(planned_td), 2)
            total_actuals = round(sum(actuals_td), 2)
            total_gap = total_actuals - total_planned
            

            profin = FinancialDataModel.find_by_project_id_and_minor_head(
                selected_year, selected_project)
            all_mom = []
            
            for month in twelve_months:
                flag = 0
                monthly_expense = {}
                monthly_expense['cumm_planned'] = 0
                monthly_expense['cumm_actuals'] = 0
                
                for row in profin:
                    if (row.month_year.strftime('%B') == month['long_month']):
                        flag = month['int_month']
                        monthly_expense['month_year'] = row.month_year.strftime('%b-%y')
                        if (row.minor_head.upper() == "FIXED COST"):
                            monthly_expense['fc_planned'] = row.planned
                            monthly_expense['fc_actuals'] = row.actuals
                            total_gap =row.actuals - row.planned
                            monthly_expense['fc'] = 'Overspent' if total_gap > 0 else 'Underspent'
                            monthly_expense['fc_gap']=total_gap
                        # else:
                        #     monthly_expense['fc_planned'] = 0
                        #     monthly_expense['fc_actuals'] = 0
                        #     monthly_expense['fc'] ='Underspent'
                        #     monthly_expense['fc_gap']=0

                        if (row.minor_head.upper() == "ACTIVITIES"):
                            monthly_expense['ac_planned'] = row.planned
                            monthly_expense['ac_actuals'] = row.actuals
                            total_gap =row.actuals - row.planned
                            monthly_expense['ac'] = 'Overspent' if total_gap > 0 else 'Underspent'
                            monthly_expense['ac_gap']=total_gap
                        # else:
                        #     monthly_expense['ac_planned'] = 0
                        #     monthly_expense['ac_actuals'] = 0
                        #     monthly_expense['ac'] ='Underspent'
                        #     monthly_expense['ac_gap']=0


                        if (row.minor_head.upper() == "OBLIGO"):
                            monthly_expense['ob_planned'] = row.planned
                            monthly_expense['ob_actuals'] = row.actuals
                            total_gap =row.actuals - row.planned
                            monthly_expense['ob'] = 'Overspent' if total_gap > 0 else 'Underspent'
                            monthly_expense['ob_gap']=total_gap

                        # else:
                        #     monthly_expense['ob_planned'] = 0
                        #     monthly_expense['ob_actuals'] = 0
                        #     monthly_expense['ob'] ='Underspent'
                        #     monthly_expense['ob_gap']=0
                        


                        if (row.minor_head.upper() == "RUNNING COST"):
                            monthly_expense['rc_planned'] = row.planned
                            monthly_expense['rc_actuals'] = row.actuals
                            total_gap =row.actuals - row.planned
                            monthly_expense['rc'] = 'Overspent' if total_gap > 0 else 'Underspent'
                            monthly_expense['rc_gap']=total_gap

                        # else:
                        #     monthly_expense['rc_planned'] = 0
                        #     monthly_expense['rc_actuals'] = 0
                        #     monthly_expense['rc'] ='Underspent'
                        #     monthly_expense['rc_gap']=0

                if flag == month['int_month']:
                    all_planned = monthly_expense['fc_planned'] \
                            + monthly_expense['ac_planned'] \
                            + monthly_expense['ob_planned'] \
                            + monthly_expense['rc_planned']
                    all_actuals= monthly_expense['fc_actuals'] \
                            + monthly_expense['ac_actuals'] \
                            + monthly_expense['ob_actuals'] \
                            + monthly_expense['rc_actuals']
                    total_gap = all_actuals-all_planned

                else:
                    all_planned = 0
                    all_actuals = 0
                    total_gap = 0
                
                if (len(all_mom) == 0):
                    monthly_expense['cumm_planned'] = all_planned
                    monthly_expense['cumm_actuals'] = all_actuals
                    monthly_expense['cumm'] = 'Overspent' if total_gap > 0 else 'Underspent'
                    monthly_expense['cumm_gap']=total_gap
                    
            
                if (len(all_mom)>0) and (month['int_month'] == flag):
                    monthly_expense['cumm_planned'] = all_mom[len(all_mom)-1]['cumm_planned'] \
                    + all_planned
                    monthly_expense['cumm_actuals'] = all_mom[len(all_mom)-1]['cumm_actuals'] \
                    + all_actuals
                    monthly_expense['cumm'] = 'Overspent' if total_gap > 0 else 'Underspent'
                    monthly_expense['cumm_gap']=total_gap

                if len(monthly_expense)>2:
                    all_mom.append(monthly_expense)

            # arrays to store data for the whole calendar year
            fixed_cost, running_cost, activities_cost, obligos_cost,\
                    total_cumm_planned, total_cumm_actuals = [], [], [], [], [], []

            for idx, row in enumerate(all_mom):
                if row['fc_actuals'] > 0:
                    fixed_cost.append(row['fc_actuals'])
                    running_cost.append(row['rc_actuals'])
                    activities_cost.append(row['ac_actuals'])
                    obligos_cost.append(row['ob_actuals'])
                    total_cumm_actuals.append(row['cumm_actuals'])
                    total_cumm_planned.append(row['cumm_planned'])
                else:
                    fixed_cost.append(row['fc_planned'])
                    running_cost.append(row['rc_planned'])
                    activities_cost.append(row['ac_planned'])
                    obligos_cost.append(row['ob_planned'])

            project_data={"name":project_item.shortname,"total_planned":'{:,.0f}'.format(total_planned),"total_gap": '{:,.0f}'.format(total_gap),
                          "total_actuals":'{:,.0f}'.format(total_actuals)}
            
            projectdict[project_item.shortname]=project_data

            projectfinance[project_item.shortname]=month_on_month
            y_mixed = format_labels(planned)
            y_all=format_labels(total_cumm_planned)            



    return render_template('charts_screen.html',
                           name=current_user.name,
                           y_mixed=y_mixed,
                           y_all=y_all,
                           labels=labels,
                           project_title=name,
                           labels_mixed_chart=labels_month,
                           cumm_planned_datalist=cumm_planned_td,
                           cumm_actuals_datalist=cumm_actuals_td,
                           planned_data=planned,
                           actuals_data=actuals,
                           pf=month_on_month, project_types=project_type_count_dict,
                           project_type_color=project_type_colors,
                           project_financials=all_mom,
                           fixed_cost=fixed_cost,
                           running_cost = running_cost,
                           activities_cost = activities_cost,
                           obligos_cost = obligos_cost,
                           total_cumm_actuals = total_cumm_actuals,
                           total_cumm_planned = total_cumm_planned,
                           projectdict = projectdict,
                           projectfinance = projectfinance
                           )

@blp.route("/finance_month/<name>", methods=['GET', 'POST'])
def finance_month(name):
    # if the page is submitted capture the project or year in the sesssion
    if request.method == 'POST':
        if "filter_project" in session:
            selected_project = session["filter_project"]
        if "filter_year" in session:
            selected_year = session["filter_year"]
        # Selected project function and methods
        if "projectName" in request.form:
            selected_project = int(request.form['projectName'])
            session["filter_project"] = selected_project
        # Selected year functions and methods
        if "projectYear" in request.form:
            selected_year = int(request.form['projectYear'])
            session["filter_year"] = selected_year
    else:  # else initiate the session values
        selected_project = 1
        session["filter_project"] = selected_project
        selected_year = date.today().year
        session["filter_year"] = selected_year



    # Get all projects of NRMAe
    projects = projectDataModel.get_all_projects()
    # create a list of projects to display on dashboard
    projectlist=['WASCA 2.0','ProSoil','ERADA']
    projectdict={}
    selected_year=2023
    projectfinance={}

    # iterate over list and perform fuctions 
    for project_item in projects:
        if project_item['shortname'] == name:
            #projectdict['name'] = project_item['shortname']
            selected_project = project_item['id']

            # get specific project requirement
            project = projectDataModel.find_by_id(int(selected_project))
            # get project financials - month wise planned and actual expenses of the project
            project_financials = FinancialDataModel.find_by_project_id_and_year(
                selected_year, selected_project)

            # make the financial data table with cummulatives and gaps
            month_on_month = []
            twelve_months = get_calendar_months()
            for row in project_financials:
                monthly_expenses = {}
                for mon in twelve_months:
                    if (row['month_year'].strftime('%b') == mon['short_month']):
                        monthly_expenses['month_only'] = mon['short_month']
                        monthly_expenses['month_year'] = row['month_year']
                        monthly_expenses['planned'] = round(row['planned'], 2)
                        monthly_expenses['actuals'] = round(row['actuals'], 2)
                        monthly_expenses['gap'] = monthly_expenses['actuals'] - \
                            monthly_expenses['planned']
                        monthly_expenses['percent'] = monthly_expenses['gap'] / \
                            monthly_expenses['planned']
                        if (len(month_on_month) == 0):
                            monthly_expenses['cumm_planned'] = monthly_expenses['planned']
                            monthly_expenses['cumm_actuals'] = monthly_expenses['actuals']
                        else:
                            monthly_expenses['cumm_planned'] = month_on_month[len(
                                month_on_month)-1]['cumm_planned']+monthly_expenses['planned']
                            monthly_expenses['cumm_actuals'] = month_on_month[len(
                                month_on_month)-1]['cumm_actuals'] + monthly_expenses['actuals']
                        monthly_expenses['cumm_gap'] = monthly_expenses['cumm_actuals'] - \
                            monthly_expenses['cumm_planned']
                        monthly_expenses['cumm_percent'] = monthly_expenses['cumm_gap'] / \
                            monthly_expenses['cumm_planned']
                        break
                if monthly_expenses:
                    month_on_month.append(monthly_expenses)
            # prepare mixed chart labels and dataset]
            # arrays to store data for the whole calendar year
            labels_month, planned, actuals, cumm_planned, cumm_actuals = [], [], [], [], []
            # arrays to store data till date (hence td)
            labels_td, planned_td, actuals_td, cumm_planned_td, cumm_actuals_td = [], [], [], [], []
            for idx, row in enumerate(month_on_month):
                # fill the dataset and labels for the whole calendar year
                labels_month.append(row['month_only'])
                planned.append(row['planned'])
                actuals.append(row['actuals'])
                cumm_planned.append(row.cumm_planned)
                cumm_actuals.append(row.cumm_actuals)
                # fill the dataset and labels array till the current month
                if idx == 0:
                    labels_td.append(row['month_only'])
                    planned_td.append(row['planned'])
                    actuals_td.append(row['actuals'])
                    cumm_planned_td.append(row.cumm_planned)
                    cumm_actuals_td.append(row.cumm_actuals)
                elif (month_on_month[idx-1]['cumm_actuals'] < row.cumm_actuals):
                    labels_td.append(row['month_only'])
                    planned_td.append(row['planned'])
                    actuals_td.append(row['actuals'])
                    cumm_planned_td.append(row.cumm_planned)
                    cumm_actuals_td.append(row.cumm_actuals)
            # get project year on year data and transpose it for display
            pywf = pywfModel.find_by_projects_id(selected_project)
            year_on_year = []
            hasYoyData = False
            if len(pywf) > 0:
                column_names = pywf[0].__table__.columns.keys()
                if len(column_names) > 0:
                    hasYoyData = True
                    for i in range(len(column_names)):
                        if(i > 2):
                            if(column_names[i] != 'projects_id'):
                                row = {}
                                row['description'] = column_names[i]
                                for j in range(len(pywf)):
                                    row[str(getattr(pywf[j], 'year'))] = getattr(
                                        pywf[j], column_names[i])
                                year_on_year.append(row)
            # create an array with count project['projectType'] from the list of project
            # Using the Counter class from the collections module to count the project types
            project_type_count = Counter(
                project['project_type'] for project in projects)

            # Converting the counter to a dictionary, if needed
            project_type_count_dict = dict(project_type_count)
            # Colors for the Project_types doughnut chart
            project_type_colors = ["#116DEE", "#EE9211",
                                    "#6346B9", "#9CB946", "#B94653"]

            ### DOUGHNUT CHART ###
            # populate the labels and data for doughnut charts
            doughnutChart_labels, doughnutChart_data, doughnutChart_title = [], [], ""
            # extract key-value pair from dictionary
            for key, value in project_type_count_dict.items():
                doughnutChart_labels.append(str(key))
                doughnutChart_data.append(value)
            doughnutChart_title = "No. of Projects"
            # prepare the totals for landing page
            total_planned = round(sum(planned_td), 2)
            total_actuals = round(sum(actuals_td), 2)
            total_gap = total_actuals - total_planned
            spent_percent = 'Overspent' if total_gap > 0 else 'Underspent'

            profin = FinancialDataModel.find_by_project_id_and_minor_head(
                selected_year, selected_project)
            all_mom = []
            for month in twelve_months:
                monthly_expense = {}
                monthly_expense['cumm_planned'] = 0
                monthly_expense['cumm_actuals'] = 0
                for row in profin:
                    if (row['month_year'].strftime('%b') == month['short_month']):
                        monthly_expense['month_year'] = row['month_year'].strftime('%b-%y')
                        if (row['minor_head'].upper() == "FIXED COST"):
                            monthly_expense['fc_planned'] = row['planned']
                            monthly_expense['fc_actuals'] = row['actuals']
                        if (row['minor_head'].upper() == "ACTIVITIES"):
                            monthly_expense['ac_planned'] = row['planned']
                            monthly_expense['ac_actuals'] = row['actuals']
                        if (row['minor_head'].upper() == "OBLIGO"):
                            monthly_expense['ob_planned'] = row['planned']
                            monthly_expense['ob_actuals'] = row['actuals']
                        if (row['minor_head'].upper() == "RUNNING COST"):
                            monthly_expense['rc_planned'] = row['planned']
                            monthly_expense['rc_actuals'] = row['actuals']
                all_planned = monthly_expense['fc_planned'] \
                        + monthly_expense['ac_planned'] \
                        + monthly_expense['ob_planned'] \
                        + monthly_expense['rc_planned']
                all_actuals= monthly_expense['fc_actuals'] \
                        + monthly_expense['ac_actuals'] \
                        + monthly_expense['ob_actuals'] \
                        + monthly_expense['rc_actuals']
                if (len(all_mom) == 0):
                    monthly_expense['cumm_planned'] = all_planned
                    monthly_expense['cumm_actuals'] = all_actuals
                else:
                    monthly_expense['cumm_planned'] = all_mom[len(all_mom)-1]['cumm_planned'] \
                    + all_planned
                    monthly_expense['cumm_actuals'] = all_mom[len(all_mom)-1]['cumm_actuals'] \
                    + all_actuals
                all_mom.append(monthly_expense)

            # arrays to store data for the whole calendar year
            fixed_cost, running_cost, activities_cost, obligos_cost,\
                    total_cumm_planned, total_cumm_actuals = [], [], [], [], [], []

            for idx, row in enumerate(all_mom):
                if row['fc_actuals'] > 0:
                    fixed_cost.append(row['fc_actuals'])
                    running_cost.append(row['rc_actuals'])
                    activities_cost.append(row['ac_actuals'])
                    obligos_cost.append(row['ob_actuals'])
                    total_cumm_actuals.append(row.cumm_actuals)
                    total_cumm_planned.append(row.cumm_planned)
                else:
                    fixed_cost.append(row['fc_planned'])
                    running_cost.append(row['rc_planned'])
                    activities_cost.append(row['ac_planned'])
                    obligos_cost.append(row['ob_planned'])

            project_data={"name":project_item['shortname'],"total_planned":'{:,.0f}'.format(total_planned),"total_gap": '{:,.0f}'.format(total_gap),
                          "total_actuals":'{:,.0f}'.format(total_actuals)}
            
            projectdict[project_item['shortname']]=project_data

            projectfinance[project_item['shortname']]=month_on_month
            



    return render_template('project_financials.html',
                           project_title=name,
                           projects=projectlist,
                           project=project,
                           financials=year_on_year,
                           filter_year=selected_year,
                           filter_project=selected_project,
                           doughnutChart_labels=doughnutChart_labels,
                           doughnutChart_data=doughnutChart_data,
                           doughnutChart_title=doughnutChart_title,
                           labels_mixed_chart=labels_month,
                           cumm_planned_datalist=cumm_planned_td,
                           cumm_actuals_datalist=cumm_actuals_td,
                           planned_data=planned,
                           actuals_data=actuals,
                           spent_percent=spent_percent,
                           pf=month_on_month, project_types=project_type_count_dict,
                           project_type_color=project_type_colors,
                           project_financials=all_mom,
                           fixed_cost=fixed_cost,
                           running_cost = running_cost,
                           activities_cost = activities_cost,
                           obligos_cost = obligos_cost,
                           total_cumm_actuals = total_cumm_actuals,
                           total_cumm_planned = total_cumm_planned,
                           projectdict = projectdict,
                           projectfinance = projectfinance
                           )

@blp.route('/projects/<year>',)
def projects_year(year):
        selected_year = year

        projects = projectDataModel.get_all_projects()
        json_data ={}
        for project_item in projects:
            if project_item.shortname in projectlist:
                #projectdict['name'] = project_item['shortname']
                selected_project = project_item.id

                # get specific project requirement
                project = projectDataModel.find_by_id(int(selected_project))
                # get project financials - month wise planned and actual expenses of the project
                project_financials = FinancialDataModel.find_by_project_id_and_year(
                    selected_year, selected_project)

                # make the financial data table with cummulatives and gaps
                month_on_month = []
                twelve_months = get_calendar_months()
                for row in project_financials:
                    monthly_expenses = {}
                    for mon in twelve_months:
                        if (row.month_year.strftime('%b') == mon['short_month']):
                            monthly_expenses['month_only'] = mon['short_month']
                            monthly_expenses['month_year'] = row.month_year
                            monthly_expenses['planned'] = round(row.planned, 2)
                            monthly_expenses['actuals'] = round(row.actuals, 2)
                            monthly_expenses['gap'] = monthly_expenses['actuals'] - \
                                monthly_expenses['planned']
                            monthly_expenses['percent'] = monthly_expenses['gap'] / \
                                monthly_expenses['planned']
                            if (len(month_on_month) == 0):
                                monthly_expenses['cumm_planned'] = monthly_expenses['planned']
                                monthly_expenses['cumm_actuals'] = monthly_expenses['actuals']
                            else:
                                monthly_expenses['cumm_planned'] = month_on_month[len(
                                    month_on_month)-1]['cumm_planned']+monthly_expenses['planned']
                                monthly_expenses['cumm_actuals'] = month_on_month[len(
                                    month_on_month)-1]['cumm_actuals'] + monthly_expenses['actuals']
                            monthly_expenses['cumm_gap'] = monthly_expenses['cumm_actuals'] - \
                                monthly_expenses['cumm_planned']
                            monthly_expenses['cumm_percent'] = monthly_expenses['cumm_gap'] / \
                                monthly_expenses['cumm_planned']
                            break
                    if monthly_expenses:
                        month_on_month.append(monthly_expenses)
                # prepare mixed chart labels and dataset]
                # arrays to store data for the whole calendar year
                labels_month, planned, actuals, cumm_planned, cumm_actuals = [], [], [], [], []
                # arrays to store data till date (hence td)
                labels_td, planned_td, actuals_td, cumm_planned_td, cumm_actuals_td = [], [], [], [], []
                for idx, row in enumerate(month_on_month):
                    # fill the dataset and labels for the whole calendar year
                    labels_month.append(row['month_only'])
                    planned.append(row['planned'])
                    actuals.append(row['actuals'])
                    cumm_planned.append(row['cumm_planned'])
                    cumm_actuals.append(row['cumm_actuals'])
                    # fill the dataset and labels array till the current month
                    if idx == 0:
                        labels_td.append(row['month_only'])
                        planned_td.append(row['planned'])
                        actuals_td.append(row['actuals'])
                        cumm_planned_td.append(row['cumm_planned'])
                        cumm_actuals_td.append(row['cumm_actuals'])
                    elif (month_on_month[idx-1]['cumm_actuals'] < row['cumm_actuals']):
                        labels_td.append(row['month_only'])
                        planned_td.append(row['planned'])
                        actuals_td.append(row['actuals'])
                        cumm_planned_td.append(row['cumm_planned'])
                        cumm_actuals_td.append(row['cumm_actuals'])
                
                total_planned = round(sum(planned_td), 2)
                total_actuals = round(sum(actuals_td), 2)
                total_gap = total_actuals - total_planned
                spent_percent = 'Overspent' if total_gap > 0 else 'Underspent'

                
                if total_planned and total_actuals:
                    percentage = (total_actuals/total_planned)*100
                else:
                    percentage=0

                
                project_data={"name":project_item.shortname,"total_planned":'{:,.0f}'.format(total_planned),"total_gap": '{:,.0f}'.format(total_gap),
                           "total_actuals":'{:,.0f}'.format(total_actuals),"percentage": '{:,.0f}'.format(percentage),"year":selected_year,"spent_percent":spent_percent}
                # project_data=(project_item['shortname'],'{:,.0f}'.format(total_planned),'{:,.0f}'.format(total_gap),'{:,.0f}'.format(total_actuals),'{:,.0f}'.format(percentage),selected_year)
                json_data[project_item.shortname]=project_data
                
                        
        return json_data 

@blp.route('/add_project',methods=["POST","GET"])
def add_project():
    projects=projectDataModel.get_project_type()
    if request.method == "POST":
             
        short_name = request.form.get('short_name')
        full_name = request.form.get('full_name')
        start_date = convert_date_format(request.form.get('start_date'))  
        end_date = convert_date_format(request.form.get('end_date'))
        objective = request.form.get('objective')
        states = request.form.get('states')
        number = request.form.get('number')
        type = request.form.get('type')
        commision = request.form.get('comm_val')
        partner = request.form.get('partner')

        data = projectDataModel(short_name,full_name,type,number,partner,states,objective,start_date,end_date,commision)
        data.save_to_db()


        return redirect(url_for('dashboard.projects'))
    return render_template('add_project.html',project_type=projects)

@blp.route('/update_project/<id>',methods=["POST","GET"])
def update_project(id):
    projects=projectDataModel.get_project_type()
    if request.method == "POST":
             
        short_name = request.form.get('short_name')
        full_name = request.form.get('full_name')
        start_date = convert_date_format(request.form.get('start_date'))  
        end_date = convert_date_format(request.form.get('end_date'))
        objective = request.form.get('objective')
        states = request.form.get('states')
        number = request.form.get('number')
        type = request.form.get('type')
        commision = request.form.get('comm_val')
        partner = request.form.get('partner')

        data = {"id":id,"shortname":short_name,"fullname":full_name,"project_type":type,
                "project_number":number,"implementing_partner":partner,"implementing_states":states,
                "project_objective":objective,"from_date":start_date,"to_date":end_date,"comm_value":commision}
        projectDataModel.update_db(data,id)


        return redirect(url_for('dashboard.projects'))
    
    if request.method == "GET":
        project = projectDataModel.find_by_id(id)
        project[0].to_date= revert_date(project[0].to_date)
        project[0].from_date=revert_date(project[0].from_date)
        return render_template('update_project.html',project=project,project_type=projects)

@blp.route('/delete_project/<id>')
def delete_project(id):
    projectDataModel.delete_from_db(id)

    return {"message": "record deleted"}

@blp.route('/view_finance',methods=["POST","GET"])
def view_finance():
    project_cost=FinancialDataModel.get_project_costs()
    projects = projectDataModel.get_all_projects()
    months = get_calendar_months()
    if request.method == "POST":
             
        project_id = request.form.get('project')
        month = request.form.get('month')
        year = request.form.get('year')
        cost = request.form.get('cost')
        actual = request.form.get('actual')
        planned = request.form.get('planned')

        date = month +' '+year
        month_year=change_date_format(date)


        data = FinancialDataModel(month_year,cost,planned,actual,project_id)
        data.save_to_db()

        return redirect(url_for('dashboard.financials'))

    return render_template('view_finance.html',project_cost=project_cost,projects=projects,months=months)

@blp.route('/add_finance',methods=["POST","GET"])
def add_finance():
    project_cost=FinancialDataModel.get_project_costs()
    projects = projectDataModel.get_all_projects()
    months = get_calendar_months()
    if request.method == "POST":
             
        project_id = request.form.get('project')
        month = request.form.get('month')
        year = request.form.get('year')
        cost = request.form.get('cost')
        actual = request.form.get('actual')
        planned = request.form.get('planned')

        date = month + ' ' + year
        month_year=change_date_format(date)


        data = FinancialDataModel(month_year,cost,planned,actual,project_id)
        data.save_to_db()

        return redirect(url_for('dashboard.financials'))
    return render_template('add_finance.html',project_cost=project_cost,projects=projects,months=months,years=years)

@blp.route('/update_finance',methods=["POST","GET"])
def update_finance():
    project_cost=FinancialDataModel.get_project_costs()
    projects = projectDataModel.get_all_projects()
    months = get_calendar_months()
    if request.method == "POST":
             
        project_id = request.form.get('project')
        month = request.form.get('month')
        year = request.form.get('year')
        cost = request.form.get('cost')
        actual = request.form.get('actual')
        planned = request.form.get('planned')

        date = month +' '+year
        month_year=change_date_format(date)


        data = FinancialDataModel(month_year,cost,planned,actual,project_id)
        data.save_to_db()

        return redirect(url_for('dashboard.financials'))
    
    # if request.method == "GET":
    #     records = FinancialDataModel.find_by_id(id)
    #     records[0].year ,records[0].month = get_year_month(str(records[0].month_year)) 
    #     return render_template('update_finance.html',records=records,project_cost=project_cost,projects=projects,months=months,years=years)

@blp.route('/delete_finance/<id>')
def delete_project(id):
    FinancialDataModel.delete_from_db(id)

    return {"message": "record deleted"}

@blp.route('/get_yearwise/<project>/<year>')
def get_yearwise(project,year):
    data={}
    record = pywfModel.find_by_project_id_year(project,year)
    data['budget']=record['budgeted']
    data['allocated']=record['allocated']
    data['planned']=record['planned']
    
    return data

@blp.route('/get_yearwise_year/<project_id>')
def get_yearwise_year(project_id):
    years=[]
    pywf=pywfModel.get_all_projects()
    for record in pywf:
        if int(project_id) == record.projects_id and record.year not in years:
            years.append(record.year)

    return years

@blp.route('/view_yearwise')
def view_yearwise():
    pywf=pywfModel.get_all_projects()
    projects = {}
    for record in pywf:
        if record.projects_id not in projects.keys():
            project = projectDataModel.find_by_id(record.projects_id)
            projects[record.projects_id]=project[0].shortname
    
    return render_template('view_yearwise.html',projects=projects)

@blp.route('/add_yearwise',methods=["POST","GET"])
def add_yearwise():
    # project_cost=FinancialDataModel.get_project_costs()
    projects = projectDataModel.get_all_projects()
    pywf=pywfModel.get_all_projects()

    # months = get_calendar_months()
    if request.method == "POST":
             
        project_id = request.form.get('project')
        year = request.form.get('year')
        budget = request.form.get('budget')
        planned = request.form.get('planned')
        allocated = request.form.get('allocated')
        tag = get_tag(pywf,project_id,year)

 
        data = pywfModel(year,tag,budget,allocated,planned,project_id)
        data.save_to_db()


        return redirect(url_for('dashboard.financials'))
    return render_template('add_yearwise.html',projects=projects)

@blp.route('/update_yearwise/<id>',methods=["POST","GET"])
def update_yearwise(id):
    pywf=pywfModel.get_all_projects()
    projects = projectDataModel.get_all_projects()    
    if request.method == "POST":
            
        project_id = request.form.get('project')
        year = request.form.get('year')
        budget = request.form.get('budget')
        planned = request.form.get('planned')
        allocated = request.form.get('allocated')
        tag = get_tag(pywf,project_id,year)

 
        data = {"year":year,"tag":tag,"budgeted":budget,"allocated":allocated,"planned":planned,"project_ids":project_id}
        pywfModel.update_db(data,id)   

        return redirect(url_for('dashboard.financials'))
    
    if request.method == "GET":
        pywf=pywfModel.find_by_id(id)
        return render_template('update_yearwise.html',projects=projects,pywf=pywf)

@blp.route('/delete_yearwise/<id>')
def delete_project(id):
    pywfModel.delete_from_db(id)

    return {"message": "record deleted"}