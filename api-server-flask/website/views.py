from flask import Blueprint, jsonify


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