"""empty message

Revision ID: 3f5bfc79d9da
Revises: 48d515870a7f
Create Date: 2021-06-02 23:19:00.359886

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3f5bfc79d9da'
down_revision = '48d515870a7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shows',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Shows_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], name='Shows_artist_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='Shows_venue_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='Shows_pkey')
    )
    op.drop_table('Show')
    # ### end Alembic commands ###
