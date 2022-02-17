from flask import Flask
from whitenoise import WhiteNoise
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models