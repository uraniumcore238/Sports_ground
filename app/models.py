from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey

from app import db


class AgeRange(db.Model):
    __tablename__ = 'age_ranges'

    id = db.Column(db.Integer, primary_key=True)
    age_range_type = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f'<Age Range type {self.age_range_type}>'


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    sport_ground_id = db.Column(db.Integer, ForeignKey('sport_grounds.id'), index=True, nullable=False)
    creator_user_id = db.Column(db.Integer, ForeignKey('users.id'), index=True, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    max_players = db.Column(db.Integer)
    age_range_id = db.Column(db.Integer, ForeignKey('age_ranges.id'), index=True, nullable=False)
    game_level_id = db.Column(db.Integer, ForeignKey('game_levels.id'), index=True, nullable=False)
    type_game = db.Column(db.String(64))

    sport_ground = db.relationship('SportGround', backref='games', lazy="joined")
    creator_user = db.relationship('User', backref='games', lazy="joined")
    age_range = db.relationship('AgeRange', backref='games', lazy="joined")
    game_level = db.relationship('GameLevel', backref='games', lazy="joined")

    def __repr__(self):
        return f'<Game ID {self.id}, sport ground id {self.sport_ground_id} >'


class GameLevel(db.Model):
    __tablename__ = 'game_levels'

    id = db.Column(db.Integer, primary_key=True)
    game_level_type = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f'<Game levels {self.game_level_type}>'


class GameType(db.Model):
    __tablename__ = 'game_types'

    id = db.Column(db.Integer, primary_key=True)
    game_type = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f'<Game types {self.game_type}>'


class SportGround(db.Model):
    __tablename__ = 'sport_grounds'

    id = db.Column(db.Integer, primary_key=True)
    ground_type = db.Column(db.String(120))
    ground_title = db.Column(db.String(120))
    location_title = db.Column(db.String(120))
    district = db.Column(db.String(120))
    address = db.Column(db.String(120))
    start_working_hours = db.Column(db.Integer)
    close_working_hours = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f'<Sport Ground {self.ground_title}, location_title {self.location_title}>'


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), unique=True)
    uploaded_user_id = db.Column(db.Integer, ForeignKey('users.id'), index=True, nullable=False)
    sport_ground_id = db.Column(db.Integer, ForeignKey('sport_grounds.id'), index=True, nullable=False)
    game_id = db.Column(db.Integer, ForeignKey('games.id'), index=True, nullable=False)

    uploaded_user = db.relationship('User', backref='photos')
    sport_ground = db.relationship('SportGround', backref='photos')
    game = db.relationship('Game', backref='photos')

    def __repr__(self):
        return f'<Photo id {self.id}, photos path {self.path}>'


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f'<User role {self.role_name}>'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))
    telegram = db.Column(db.String(120), unique=True)
    role_id = db.Column(db.Integer, ForeignKey('user_roles.id'), index=True, nullable=False)

    role = db.relationship('UserRole', backref='users')
    games = db.relationship('Game', secondary="users_games", backref='users')

    def __repr__(self):
        return f'<User id {self.id}, email {self.email}>'


class UserGame(db.Model):
    __tablename__ = 'users_games'

    game_id = db.Column(db.Integer, ForeignKey('games.id'), primary_key=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True,  index=True, nullable=False)

    def __repr__(self):
        return f'<Game id {self.game_id}, User id {self.user_id}>'
