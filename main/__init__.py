from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import models

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevConfig')

# db variable initialization
db = SQLAlchemy(app)

from . import views
