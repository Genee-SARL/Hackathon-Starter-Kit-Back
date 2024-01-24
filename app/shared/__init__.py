import logging
import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    print(f"Using {app.config['DB_NAME']}")

    db.init_app(app)
    if app.config['MIGRATION'] == "1":
        migrate.init_app(app, db)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    url_prefix = "/api"

    from data.hello_world.controllers import hello_world_blueprint
    app.register_blueprint(hello_world_blueprint, url_prefix=url_prefix)

    import data.trader.models
    from data.trader.models.trader_model import TraderModel
    @app.errorhandler(ValidationError)
    def handle_custom_error(error):
        return str(error), 400

    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()
        trader1 = TraderModel(id_trader='1904259',
                              trader_url='https://www.mql5.com/en/signals/1904259?source=Site+Signals+Subscriptions',
                              valid=True)
        trader2 = TraderModel(id_trader='2068879',
                              trader_url='https://www.mql5.com/en/signals/2068879?source=Site+Signals+Subscriptions',
                              valid=True)

        db.session.add(trader1)
        db.session.add(trader2)
        db.session.commit()



    return app
