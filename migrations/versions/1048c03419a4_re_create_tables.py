"""re_create_tables

Revision ID: 1048c03419a4
Revises: 
Create Date: 2022-01-12 19:58:35.446509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1048c03419a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('age_ranges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age_range_type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('age_range_type')
    )
    op.create_table('game_levels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_level_type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('game_level_type')
    )
    op.create_table('game_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('game_type')
    )
    op.create_table('sport_grounds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_id', sa.Integer(), nullable=True),
    sa.Column('ground_type', sa.String(length=120), nullable=True),
    sa.Column('ground_title', sa.String(length=120), nullable=True),
    sa.Column('location_title', sa.String(length=120), nullable=True),
    sa.Column('district', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('start_working_hours', sa.Integer(), nullable=True),
    sa.Column('close_working_hours', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('original_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('telegram', sa.String(length=120), nullable=True),
    sa.Column('role', sa.Enum('admin', 'user', name='usersrolesenum'), server_default='user', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('telegram')
    )
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sport_ground_id', sa.Integer(), nullable=False),
    sa.Column('user_creation_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('max_players', sa.Integer(), nullable=True),
    sa.Column('age_range_id', sa.Integer(), nullable=False),
    sa.Column('game_level_id', sa.Integer(), nullable=False),
    sa.Column('type_game', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['age_range_id'], ['age_ranges.id'], ),
    sa.ForeignKeyConstraint(['game_level_id'], ['game_levels.id'], ),
    sa.ForeignKeyConstraint(['sport_ground_id'], ['sport_grounds.id'], ),
    sa.ForeignKeyConstraint(['user_creation_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_games_age_range_id'), 'games', ['age_range_id'], unique=False)
    op.create_index(op.f('ix_games_game_level_id'), 'games', ['game_level_id'], unique=False)
    op.create_index(op.f('ix_games_sport_ground_id'), 'games', ['sport_ground_id'], unique=False)
    op.create_index(op.f('ix_games_user_creation_id'), 'games', ['user_creation_id'], unique=False)
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=120), nullable=True),
    sa.Column('uploaded_user_id', sa.Integer(), nullable=False),
    sa.Column('sport_ground_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['sport_ground_id'], ['sport_grounds.id'], ),
    sa.ForeignKeyConstraint(['uploaded_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_index(op.f('ix_photos_game_id'), 'photos', ['game_id'], unique=False)
    op.create_index(op.f('ix_photos_sport_ground_id'), 'photos', ['sport_ground_id'], unique=False)
    op.create_index(op.f('ix_photos_uploaded_user_id'), 'photos', ['uploaded_user_id'], unique=False)
    op.create_table('users_games',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('game_id', 'user_id')
    )
    op.create_index(op.f('ix_users_games_game_id'), 'users_games', ['game_id'], unique=False)
    op.create_index(op.f('ix_users_games_user_id'), 'users_games', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_games_user_id'), table_name='users_games')
    op.drop_index(op.f('ix_users_games_game_id'), table_name='users_games')
    op.drop_table('users_games')
    op.drop_index(op.f('ix_photos_uploaded_user_id'), table_name='photos')
    op.drop_index(op.f('ix_photos_sport_ground_id'), table_name='photos')
    op.drop_index(op.f('ix_photos_game_id'), table_name='photos')
    op.drop_table('photos')
    op.drop_index(op.f('ix_games_user_creation_id'), table_name='games')
    op.drop_index(op.f('ix_games_sport_ground_id'), table_name='games')
    op.drop_index(op.f('ix_games_game_level_id'), table_name='games')
    op.drop_index(op.f('ix_games_age_range_id'), table_name='games')
    op.drop_table('games')
    op.drop_table('users')
    op.drop_table('sport_grounds')
    op.drop_table('game_types')
    op.drop_table('game_levels')
    op.drop_table('age_ranges')
    # ### end Alembic commands ###