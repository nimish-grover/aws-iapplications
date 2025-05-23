"""add user_feedbacks

Revision ID: fcd5f7398242
Revises: 1af854534eb4
Create Date: 2024-10-01 16:00:26.913409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcd5f7398242'
down_revision = '1af854534eb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_feedbacks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('topic', sa.String(length=100), nullable=False),
    sa.Column('feedback', sa.String(length=500), nullable=False),
    sa.Column('created_on', sa.String(length=20), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    # Grant permissions
    op.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO zeidwhrc;")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_feedbacks')
    # ### end Alembic commands ###

    # Revoke permissions if necessary
    op.execute("REVOKE ALL PRIVILEGES ON SCHEMA public FROM zeidwhrc;")
