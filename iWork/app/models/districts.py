from sqlalchemy import func
from iWork.app.classes.helper_methods import Helper
from iWork.app.db import db


class District(db.Model):
    __tablename__ = 'nrega_districts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    nrega_id = db.Column(db.Integer, nullable=False, unique=True)
    state_id = db.Column(db.ForeignKey('nrega_states.id'), nullable=False)

    state = db.relationship('State')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nrega_id': self.nrega_id,
            'state_id': self.state_id
        }


    @classmethod
    def get_districts_by_state_id(cls, state_id):
        return cls.query.filter_by(state_id = state_id).order_by(cls.name).all()
    
    @classmethod
    def get_districts_by_completed_work(cls, state_id):
        from sqlalchemy.dialects import postgresql
        from iWork.app.models.field_data import FieldData
        from iWork.app.models.blocks import Block
        from iWork.app.models.states import State
        from iWork.app.models.panchayats import Panchayat
        from iWork.app.models.completed_works import CompletedWork
        query = (
                db.session.query(
                    District.id.label('district_id'),  # Select district ID
                    District.name.label('district_name')  # Select district name
                )
                .join(Block, Block.district_id == District.id)  # INNER JOIN nrega_blocks nb on nb.district_id = nd.id
                .join(Panchayat, Panchayat.block_id == Block.id)  # INNER JOIN nrega_panchayats np on np.block_id = nb.id
                .join(CompletedWork, CompletedWork.panchayat_id == Panchayat.id)  # INNER JOIN nrega_completed_works ncw on ncw.panchayat_id = np.id
                .outerjoin(FieldData, FieldData.completed_work_id == CompletedWork.id)  # LEFT JOIN field_data fd on fd.completed_work_id = ncw.id
                .filter(District.state_id == state_id)  # WHERE nd.state_id = 18
                .group_by(District.id, District.name)  # GROUP BY nd.id, nd.name
                .having(func.count(CompletedWork.id) > func.count(FieldData.completed_work_id))  # HAVING count(ncw.id) > count(fd.completed_work_id)
            )
        sql_query = query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
        print(str(sql_query))
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[0], 'name': result[1]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data