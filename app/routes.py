from flask import render_template, redirect, url_for
from app import app
from app.forms import SheetForm
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = SheetForm()
    if form.validate_on_submit():
        f = form.sheet.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.root_path, 'uploads', filename
        ))
        return render_template('upload.html', form=form, uploaded=os.path.join('uploads', filename))

    return render_template('upload.html', form=form)