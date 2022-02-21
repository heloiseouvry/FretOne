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
        f.save(os.path.join('/tmp', filename))

        s3 = boto3.client(
            "s3",
            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
        )
        S3_BUCKET = app.config['S3_BUCKET_NAME']

        try:
            s3.upload_file(os.path.join('/tmp', filename), S3_BUCKET, filename)
        except ClientError as e:
            logging.error(e)

        if not s3:
            f_db = Upload(filename=filename)
            db.session.add(f_db)
            db.session.commit()

        [translated_file, translated_filename] = translate(os.path.join('/tmp', filename), os.path.join('/tmp'))
        print(f"Translated file: {translated_file} | type: {type(translated_file)}")

        try:
            s3.Object(S3_BUCKET, translated_filename).put(Body=translated_file,ContentType='image/JPG')
            # s3.upload_file(os.path.join('/tmp', translated_filename), S3_BUCKET, translated_filename)
        except ClientError as e:
            logging.error(e)

        return render_template('upload.html', form=form, os=os, S3_BUCKET=S3_BUCKET)

    return render_template('upload.html', form=form, os=os, S3_BUCKET=None)

@app.route('/upload_db')
def upload_db():
    uploads = Upload.query.all()
    return render_template('upload_db.html', uploads=uploads, os=os)