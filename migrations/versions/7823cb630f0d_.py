"""empty message

Revision ID: 7823cb630f0d
Revises: 9a3a2baf5f4f
Create Date: 2021-04-27 21:41:28.109753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7823cb630f0d'
down_revision = '9a3a2baf5f4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.add_column('Shows', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.drop_constraint('Shows_venue_fkey', 'Shows', type_='foreignkey')
    op.drop_constraint('Shows_artist_fkey', 'Shows', type_='foreignkey')
    op.create_foreign_key(None, 'Shows', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'Shows', 'Artist', ['artist_id'], ['id'])
    op.drop_column('Shows', 'artist')
    op.drop_column('Shows', 'venue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('venue', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Shows', sa.Column('artist', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.create_foreign_key('Shows_artist_fkey', 'Shows', 'Artist', ['artist'], ['id'])
    op.create_foreign_key('Shows_venue_fkey', 'Shows', 'Venue', ['venue'], ['id'])
    op.drop_column('Shows', 'venue_id')
    op.drop_column('Shows', 'artist_id')
    # ### end Alembic commands ###