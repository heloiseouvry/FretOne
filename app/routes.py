from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import os
from app import app
from app import db
from app.forms import SheetForm
from app.models import Upload
from tab2notes.src.f1 import translate

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = SheetForm()
    if form.validate_on_submit():
        f = form.fileloader.data
        filename = secure_filename(f.filename)
        Path("/uploads").mkdir(parents=True, exist_ok=True)
        Path("/translated").mkdir(parents=True, exist_ok=True)
        f.save(os.path.join(
            app.root_path, '/uploads', filename
        ))
        f_db = Upload(filename=filename)
        db.session.add(f_db)
        db.session.commit()
        translate(os.path.join(app.root_path, '/uploads', filename), os.path.join(app.root_path, '/translated/'))
        # return redirect(url_for('upload_db'))
        return render_template('upload.html', form=form, os=os)

    return render_template('upload.html', form=form, os=os)

@app.route('/upload_db')
def upload_db():
    uploads = Upload.query.all()
    return render_template('upload_db.html', uploads=uploads, os=os)