"""empty message

Revision ID: f5e416419b75
Revises: cb73376fdbea
Create Date: 2024-04-26 09:58:48.095977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5e416419b75'
down_revision = 'cb73376fdbea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=250), nullable=False),
    sa.Column('created', sa.String(length=250), nullable=False),
    sa.Column('diameter', sa.String(length=250), nullable=False),
    sa.Column('edited', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('properties', sa.String(length=250), nullable=False),
    sa.Column('cargo_capacity', sa.String(length=250), nullable=False),
    sa.Column('consumables', sa.String(length=250), nullable=False),
    sa.Column('cost_in_credits', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('planets')
    op.drop_table('vehicles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('properties', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('cargo_capacity', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('consumables', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('cost_in_credits', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='vehicles_pkey')
    )
    op.create_table('planets',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('climate', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('created', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('diameter', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('edited', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='planets_pkey')
    )
    op.drop_table('vehicle')
    op.drop_table('planet')
    # ### end Alembic commands ###
