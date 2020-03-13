"""empty message

Revision ID: 9f58d65a2011
Revises: 01faca18f168
Create Date: 2020-03-13 03:03:08.213995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f58d65a2011'
down_revision = '01faca18f168'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('face', sa.Column('updated_at', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_face_updated_at'), 'face', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_face_updated_at'), table_name='face')
    op.drop_column('face', 'updated_at')
    # ### end Alembic commands ###