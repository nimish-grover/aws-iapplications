"""add category key

Revision ID: fcadd9edf022
Revises: fcd5f7398242
Create Date: 2024-10-09 17:26:10.159777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcadd9edf022'
down_revision = 'fcd5f7398242'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('nrega_permissible_works', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'nrega_categories', ['category_id'], ['id'])

    # ### end Alembic commands ###

    # Grant permissions
    op.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO zeidwhrc;")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('nrega_permissible_works', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###

    # Revoke permissions if necessary
    op.execute("REVOKE ALL PRIVILEGES ON SCHEMA public FROM zeidwhrc;")
