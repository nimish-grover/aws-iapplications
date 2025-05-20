from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from iWork.app.models import InputAndPermissible, InputParameter, PermissibleWork, FieldData


blp = Blueprint('admin','admin')

@blp.route('/parameters', methods=['POST', 'GET'])
@login_required
def parameters():
    if request.method=='POST':
        permissible_work_id = request.json
        input_parameters = InputAndPermissible.get_parameters_by_permissible_work_id(permissible_work_id=permissible_work_id['permissible_work_id'])
        return input_parameters
    else:
        permissible_works = PermissibleWork.get_all()
        return render_template('parameters.html', permissible_works=permissible_works)

@blp.route('/update_parameter/<int:parameter_id>', methods=['POST','GET'])
@login_required
def update_parameter(parameter_id):
    input_parameter = InputParameter.get_parameter_by_id(parameter_id)
    if request.method=='POST':
        for key,value in input_parameter.items():
            if key!='id':
                input_parameter[key] = request.form.get(key)
        input_parameter['id'] = parameter_id
        result = InputParameter.update_db(input_parameter, parameter_id)
        if result:
            flash('Record updated successfully')
            return redirect(url_for('.parameters'))
        else:
            return {'message': 'There was an error'}
    else:        
        return render_template('edit_parameter.html', input_parameter=input_parameter)
@login_required
@blp.route('/delete_parameter/<int:input_permissible_id>', methods=['POST','GET'])
def delete_parameter(input_permissible_id):
    if request.method=='POST':
        # for key,value in input_parameter.items():
        #     if key!='id':
        #         input_parameter[key] = request.form.get(key)
        # input_parameter['id'] = parameter_id
        result = InputAndPermissible.delete_db(input_permissible_id)
        if result:
            flash('Record deleted successfully')
            return redirect(url_for('.parameters'))
        else:
            return {'message': 'There was an error'}
    else:
        input_permissible = InputAndPermissible.get_by_id(input_permissible_id)
        if input_permissible:
            input_parameter = InputParameter.get_parameter_by_id(input_permissible.input_parameter_id)
        return render_template('delete_parameter.html', input_parameter=input_parameter, input_permissible=input_permissible)
@blp.route('/set_order', methods=['POST'])
@login_required   
def set_order():
    json_data = request.json
    # json_array = json.loads(json_data)
    for element in json_data:
        input_permissible_id = element['input_id'].split('_')[1]
        parameter_order = element['input_value']
        success = InputAndPermissible.update_db(parameter_order,input_permissible_id)
    if success:
        return {'message': 'Record updated successfully'}
    if success:
        return {'message': 'There was an error'}
    
@blp.route('/field_data',defaults={'page_number': 1})
@blp.route('/field_data/<int:page_number>')
@login_required
def field_data(page_number):
    field_data = FieldData.get_field_data(page=page_number, per_page=10)
    return render_template('field_data.html', field_data=field_data.items, pagination=field_data )

@blp.route('/all_parameters',defaults={'page_number': 1})
@blp.route('/all_parameters/<int:page_number>')
@login_required
def all_parameters(page_number):
    input_parameters = InputParameter.get_all_parameters(page=page_number, per_page=10)
    return render_template('all_parameters.html', input_parameters=input_parameters.items, pagination=input_parameters)