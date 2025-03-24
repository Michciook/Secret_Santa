from . import db


class Affiliation(db.Model):
    __tablename__ = 'affiliations'

    affiliation_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'), nullable=False)

    user = db.relationship('User', back_populates='affiliations')
    room = db.relationship('Room', back_populates='affiliations')

    def __repr__(self):
        return f'Affiliation id: {self.affiliation_id}, User: {self.user_id}, Room: {self.room_id}'


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    affiliations = db.relationship('Affiliation', back_populates='user', lazy=True)
    rooms = db.relationship('Room', secondary='affiliations', viewonly=True, back_populates='users')

    def __repr__(self):
        return f'User id: {self.user_id}'


class Room(db.Model):
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    creator = db.relationship('User', backref=db.backref('created_rooms', lazy=True))
    affiliations = db.relationship('Affiliation', back_populates='room', lazy=True)
    users = db.relationship('User', secondary='affiliations', viewonly=True, back_populates='rooms')

    def __repr__(self):
        return f'Room id: {self.room_id}, Creator: {self.creator_id}'
