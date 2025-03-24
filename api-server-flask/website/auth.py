from flask import Blueprint, jsonify, request, session
from . import db
from .models import User


auth = Blueprint('views', __name__)

@auth.route('/login/', methods=['POST'])
def login():
    try:
        creds = request.json

        if not creds or 'username' not in creds or 'password' not in creds:
            return jsonify({'error': f'Username and password is required!'}), 401

        user = db.session.query(User).filter_by(username=creds['username']).first()

        if user is None:
            return jsonify({'error': f'No user found'}), 401
        
        if creds['password'] != user.password:
            return jsonify({'error': f'Wrong password'}), 401
        
        session['uid'] = user.user_id

        return jsonify({'id' : user.user_id, 'name': user.username})

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    

@auth.route('/logout/', methods=['POST'])
def logout():
    if session.get("uid", False):
        session.clear()
        return jsonify({'message' : 'Logged out'})
    return jsonify({'message' : 'Login first!'})


@auth.route('/register/', methods=['POST'])
def register():
    try:
        creds = request.json
        
        if not creds or 'username' not in creds or 'password' not in creds or 'email' not in creds:
            return jsonify({'error': f'Username and password is required!'}), 401
        
        existing_user = db.session.query(User).filter((
            User.username == creds['username']) | (User.email == creds['email'])
            ).first()
        
        if existing_user:
            return jsonify({'error': f'User with this username or email already exists!'}), 408
        
        try:
            new_user = User(username=creds['username'], email=creds['email'], password=creds['password'])

            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User registered successfully!'}), 201
        
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500