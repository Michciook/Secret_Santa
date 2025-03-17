from flask import Flask
from models import db
from os import path

app = Flask(__name__)
DB_NAME = 'secretsanta_database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


@app.route('/')
def index():
    return "Hello Santa!"


def init_db():
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created successfully!')

if __name__ == '__main__':
    init_db()
    app.run()