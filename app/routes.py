from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from app import app
from app import db
from app.forms import SheetForm
from app.models import Upload


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
        f.save(os.path.join(
            app.root_path, 'static/uploads', filename
        ))
        f_db = Upload(filename=filename)
        db.session.add(f_db)
        db.session.commit()
        # return redirect(url_for('upload_db'))
        return render_template('upload.html', form=form, os=os)

    return render_template('upload.html', form=form, os=os)

@app.route('/upload_db')
def upload_db():
    uploads = Upload.query.all()
    return render_template('upload_db.html', uploads=uploads, os=os)