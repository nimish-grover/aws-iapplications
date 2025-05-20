from marshmallow import Schema, fields

class projectDataSchema(Schema):
    id = fields.Int()
    shortname = fields.Str()
    fullname =fields.Str()
    germanname = fields.Str()
    project_number = fields.Str()
    from_date = fields.Str()
    to_date =fields.Str()
    comm_value = fields.Float()
    av = fields.Str()
    dv = fields.Str()
    fm = fields.Str()
    vgk = fields.Str()

class pywfSchema(Schema):
    id = fields.Int()
    year = fields.Str()
    fullname =fields.Str()
    tag = fields.Str()
    budget = fields.Str()
    allocated = fields.Str()
    planned =fields.Str()

class FinancialDataSchema(Schema):
    id = fields.Int()
    month_year = fields.Str()
    minor_head = fields.Str()
    planned = fields.Str()
    actuals = fields.Str()