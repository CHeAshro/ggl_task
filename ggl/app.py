
import tempfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(type=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if type == 'test':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ggl:1234@127.0.0.1:3306/ggl'

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import bp as task_bp
    app.register_blueprint(task_bp)

    return app


app = create_app()
