"""add unique plant_type

Revision ID: fc7043867e46
Revises: 7f61f38938d7
Create Date: 2024-10-16 13:07:30.631385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc7043867e46'
down_revision = '7f61f38938d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plant_types', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###

    # Grant permissions
    op.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO zeidwhrc;")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plant_types', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###

    # Revoke permissions if necessary
    op.execute("REVOKE ALL PRIVILEGES ON SCHEMA public FROM zeidwhrc;")
