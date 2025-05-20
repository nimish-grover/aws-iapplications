from iWork.app.db import db
from iWork.app.models import InputParameter, PermissibleWork

class InputAndPermissible(db.Model):
    ''' 
    table to map two tables - Input parameters table with Proposed Status (also referred as work type sometimes) table
    '''
    __tablename__ = "inputs_and_permissibles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parameter_order = db.Column(db.Integer, nullable=True)
    input_parameter_id = db.Column(db.ForeignKey('input_parameters.id'), nullable=False)
    permissible_work_id = db.Column(db.ForeignKey('nrega_permissible_works.id'), nullable=False)

    input = db.relationship("InputParameter")
    permissible_work = db.relationship("PermissibleWork")

    def __init__(self, name, description):
        self.name = name,
        self.descrition = description

    def json(self):
        return {
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_parameters_by_permissible_work_id(cls, permissible_work_id):
        results = db.session.query(
            cls.id.label("id"),
            cls.parameter_order.label('parameter_order'),
            InputParameter.id.label('input_parameter_id'),
            InputParameter.name.label('input_parameter_name'),
            InputParameter.description.label('input_parameter_description'),
            InputParameter.label.label('input_parameter_label'),
            InputParameter.unit.label('input_parameter_unit'),
            InputParameter.element_type.label('element_type'),
            PermissibleWork.id.label('permissible_work_id'),
            PermissibleWork.permissible_work.label('permissible_work')
        ).join(InputParameter, InputParameter.id == cls.input_parameter_id
        ).join(PermissibleWork, PermissibleWork.id == cls.permissible_work_id
        ).filter(PermissibleWork.id == permissible_work_id).all()

        if results:
            parameters = [
                {
                    'input_permissible_id': result.id,
                    'id': result.input_parameter_id,
                    'parameter_order': result.parameter_order,
                    'name': result.input_parameter_name,
                    'description': result.input_parameter_description,
                    'label':result.input_parameter_label,
                    'unit':result.input_parameter_unit,
                    'element_type':result.element_type,
                    'permissible_work_id': result.permissible_work_id,
                    'permissible_work': result.permissible_work
                }
                for result in results
            ]
            return parameters
        else:
            return None
           
    @classmethod
    def update_db(cls, parameter_order, input_permissible_id):
        try:
        # Retrieve the object first
            input_permissible = cls.query.get(input_permissible_id)
            if not input_permissible:
                return False  # Return False if no record with that ID

            # Update the fields in the object
            input_permissible.parameter_order = parameter_order
            # for key, value in data.items():
            #     setattr(input_permissible, key, value)

            db.session.commit()
            return True  # Success

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error updating record: {e}")
            return False
        
    @classmethod
    def delete_db(cls, input_permissible_id):
        try:
            input_permissible = cls.query.get(input_permissible_id)
            if not input_permissible:
                return False
            db.session.delete(input_permissible)
            # db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error deleting record: {e}")
            return False