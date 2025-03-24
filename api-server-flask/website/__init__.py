from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, urandom

db = SQLAlchemy()
DB_NAME = 'secretsanta_database.db'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = urandom(12).hex()
    db.init_app(app)

    from website.views import views
    from website.auth import auth

    app.register_blueprint(views, url_prefix='/api/', name='views_blueprint')
    app.register_blueprint(auth, url_prefix='/api/auth/', name='auth_blueprint')

    from .models import Affiliation, User, Room

    create_database(app)


    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created successfully!')

