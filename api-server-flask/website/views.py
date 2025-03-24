from flask import Blueprint, jsonify
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
    

