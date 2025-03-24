from flask import Blueprint, jsonify, session, request
from . import db
from .models import Room

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return 'secret santa'

@views.route('/test', methods=['GET'])
def test():
    try:
        return jsonify({'test': 'this is a test data'}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
@views.route('/get_rooms/', methods=['GET'])
def get_rooms():
    try:
        room_rows = db.session.query(Room).all()
        data = [{'id': row.room_id, 'roomname': row.roomname, 'creator_id': row.creator_id } for row in room_rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
@views.route('/add_room/', methods=['POST'])
def add_room():
    try:
        if session.get("uid", False):
            roomDetails = request.json

            if not roomDetails or 'roomname' not in roomDetails or 'password' not in roomDetails:
                return jsonify({'error': f'Roomname and password is required!'}), 401
            
            existingRoom = db.session.query(Room).filter_by(roomname=roomDetails['roomname']).first()

            if existingRoom:
                return jsonify({'error': f'Room with this name already exists!'}), 408
            
            try:
                new_room = Room(roomname=roomDetails['roomname'], password=roomDetails['password'], creator_id=session['uid'])

                db.session.add(new_room)
                db.session.commit()

                return jsonify({'message': 'Room added successfully!'}), 201
            
            except Exception as e:
                return jsonify({'error': f'Database error: {str(e)}'}), 500
            
        return jsonify({'message' : 'Login first!'})


    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    

