from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# from config import DevConfig, ProdConfig

# db variable initialization
db = SQLAlchemy()

exo_app = Flask(__name__, instance_relative_config=True)
exo_app.config.from_object('config.DevConfig')
db.init_app(exo_app)


from . import views
