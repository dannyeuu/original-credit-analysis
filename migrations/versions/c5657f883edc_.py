"""empty message

Revision ID: c5657f883edc
Revises: 74f12526ad6c
Create Date: 2017-12-03 04:40:55.556063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5657f883edc'
down_revision = '74f12526ad6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('integration', sa.Column('client_id', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'integration', ['client_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'integration', type_='unique')
    op.drop_column('integration', 'client_id')
    # ### end Alembic commands ###
