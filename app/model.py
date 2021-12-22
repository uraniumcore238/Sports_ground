from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Games(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    sports_grounds_id = db.Column(db.Integer, nullable=False)
    creator_user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Text, nullable=False)
    end_time = db.Column(db.Text, nullable=False)
    max_players = db.Column(db.Integer, nullable=False)
    age_range_id = db.Column(db.Integer, nullable=False)
    game_level_id = db.Column(db.Integer, nullable=False)
    type_of_game_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Games {} {}>'.format(self.id, self.sports_grounds_id)


class AgeRange(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    type = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<AgeRange {} {}>'.format(self.id, self.type)


class GameLevel(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    type = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<GameLevel {} {}>'.format(self.id, self.type)


class TypeOfGame(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    type = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<TypeOfGame {} {}>'.format(self.id, self.type)

