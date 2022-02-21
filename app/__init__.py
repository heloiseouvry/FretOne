from flask import Flask
from whitenoise import WhiteNoise
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
try:
    from config import Config
except ModuleNotFoundError as err:
    print(err)

app = Flask(__name__, static_url_path='/static')
if app.config:
    app.config.from_object(Config)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models