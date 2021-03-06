from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from app import app
from app import db
from app.forms import SheetForm
from app.models import Upload
from tab2notes.src.f1 import translate
import boto3
from botocore.exceptions import ClientError
import logging

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
        f.save(os.path.join(os.path.sep, 'tmp', filename))

        s3 = boto3.client(
            "s3",
            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
        )
        S3_BUCKET = app.config['S3_BUCKET_NAME']

        try:
            s3.upload_file(os.path.join(os.path.sep, 'tmp', filename), S3_BUCKET, filename)
        except ClientError as e:
            logging.error(e)

        if not s3:
            f_db = Upload(filename=filename)
            db.session.add(f_db)
            db.session.commit()

        translation = translate(os.path.join(os.path.sep, 'tmp', filename), os.path.join(os.path.sep, 'tmp', os.path.sep))

        try:
            for translated_filename in translation:
                s3.upload_file(os.path.join(os.path.sep, 'tmp', translated_filename), S3_BUCKET, translated_filename)
        except ClientError as e:
            logging.error(e)

        return render_template('upload.html', form=form, os=os, S3_BUCKET=S3_BUCKET, translation=translation)

    return render_template('upload.html', form=form, os=os, S3_BUCKET=None, translation=None)

@app.route('/upload_db')
def upload_db():
    uploads = Upload.query.all()
    return render_template('upload_db.html', uploads=uploads, os=os)