import os
from flask import Flask
from whitenoise import WhiteNoise
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, static_url_path='/static')
try:
    from config import Config
    app.config.from_object(Config)
except ModuleNotFoundError as err:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['S3_BUCKET_NAME'] = os.environ.get('S3_BUCKET_NAME')
    app.config['AWS_ACCESS_KEY_ID'] = os.environ.get('AWS_ACCESS_KEY_ID')
    app.config['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY')
    print(err)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models