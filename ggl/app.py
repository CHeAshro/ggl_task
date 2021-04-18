
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(type=None):
    flask_app = Flask(__name__)
    flask_app.debug = True

    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if type == 'test':
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        flask_app.config['TESTING'] = True
    else:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ggl:1234@127.0.0.1:3306/ggl'

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    from views import bp as task_bp
    flask_app.register_blueprint(task_bp)

    return flask_app


app = create_app()
