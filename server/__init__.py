from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# Read the configuration object and apply it to the Flask instance
app.config.from_object(Config)
# create a database instance to interact with the database
db = SQLAlchemy(app) 
migrate = Migreate(app, db)

from server import routes, models