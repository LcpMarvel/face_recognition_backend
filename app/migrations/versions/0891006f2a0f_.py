"""empty message

Revision ID: 0891006f2a0f
Revises: 9f58d65a2011
Create Date: 2020-04-01 03:03:50.722834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0891006f2a0f'
down_revision = '9f58d65a2011'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('face', sa.Column('face_pp_set', sa.String(), nullable=True))
    op.add_column('face', sa.Column('face_pp_token', sa.String(), nullable=True))
    op.create_index(op.f('ix_face_face_pp_token'), 'face', ['face_pp_token'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_face_face_pp_token'), table_name='face')
    op.drop_column('face', 'face_pp_token')
    op.drop_column('face', 'face_pp_set')
    # ### end Alembic commands ###
