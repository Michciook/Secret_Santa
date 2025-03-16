from flask import Flask
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secretsanta_database.db'
db.init_app(app)


@app.route('/')
def index():
    return "Hello Santa!"


if __name__ == '__main__':
    app.run()