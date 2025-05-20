from iWork.app.db import db

class InputParameter(db.Model):
    __tablename__ = "input_parameters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100)) # unique name of the input parameter
    label= db.Column(db.String(80)) # label for the input paramter
    unit = db.Column(db.String(80)) # unit of measurement 
    description = db.Column(db.String(300)) # details description of input parameter for (i) tooltip
    element_type = db.Column(db.String(100)) # whether dropdown, textbox or datalist
    constraint = db.Column(db.String(100))

    def __init__(self, name, label, unit, description, element_type, constraint):
        self.name = name,
        self.label = label,
        self.unit = unit,
        self.description = description
        self.element_type = element_type
        self.constraint = constraint

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'label' : self.label,
            'unit' : self.unit,
            'description': self.description,
            'element_type': self.element_type,
            'constraint': self.constraint
        }
    @classmethod
    def get_parameter_by_id(cls, _id):
        result = cls.query.filter_by(id=_id).first()
        if result:
            return result.json()
        else:
            return None
        
    @classmethod
    def get_all_parameters(cls, page, per_page):
        results = cls.query.order_by(cls.id)
        # if results:
        #     results = [result.json() for result in results]
        # else:
        #     results = None
        pagination = results.paginate(page=page, per_page=per_page, error_out=False)
        return pagination
        # return results
    
    @classmethod
    def update_db(cls, data, _id):
        try:
        # Retrieve the object first
            parameter = cls.query.get(_id)
            if not parameter:
                return False  # Return False if no record with that ID

            # Update the fields in the object
            for key, value in data.items():
                setattr(parameter, key, value)

            db.session.commit()
            return True  # Success

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error updating record: {e}")
            return False
        
    @classmethod
    def delete_db(cls, data, _id):
        try:
        # Retrieve the object first
            parameter = cls.query.get(_id)
            if not parameter:
                return False  # Return False if no record with that ID

            # Update the fields in the object
            for key, value in data.items():
                setattr(parameter, key, value)

            db.session.delete(parameter)
            db.session.commit()
            return True  # Success

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error updating record: {e}")
            return False