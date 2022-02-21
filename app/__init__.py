from flask import Flask
from whitenoise import WhiteNoise
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, static_url_path='/static')
try:
    from config import Config
    app.config.from_object(Config)
except ModuleNotFoundError as err:
    print(err)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models