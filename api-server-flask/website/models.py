from . import db


class Affiliation(db.Model):
    __tablename__ = 'affiliations'

    affiliation_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('affiliations', lazy=True))
    room = db.relationship('Room', backref=db.backref('affiliations', lazy=True))

    def __repr__(self):
        return f'Affiliation id: {self.affiliation_id}, User: {self.user_id}, Room: {self.room_id}'


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    rooms = db.relationship(
        'Room', secondary='affiliations', backref=db.backref('users', lazy='dynamic'), lazy='dynamic'
    )

    def __repr__(self):
        return f'User id: {self.user_id}'


class Room(db.Model):
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    creator = db.relationship('User', backref=db.backref('created_rooms', lazy=True))

    def __repr__(self):
        return f'Room id: {self.room_id}, Creator: {self.creator_id}'
