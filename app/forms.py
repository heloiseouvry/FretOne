from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
import os
from app import app

class SheetForm(FlaskForm):
    sheet = FileField(validators=[FileRequired()])