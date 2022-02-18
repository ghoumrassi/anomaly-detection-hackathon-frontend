from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import os
import json
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from helpers import validate_file
from random import randint


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'


with open('keys/anomaly-detection-hackathon-a1de2720418b.json', 'r') as f:
    credentials_dict = json.load(f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)

@app.route("/")
def homepage():
    if 'sessionid' not in session:
        session['sessionid'] = str(randint(1, 1e9)).zfill(9)
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/sample_text')
def sampletext():
    return 'Lorem ipsum...'

@app.route('/test')
def test_env():
    return render_template('test.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(session.items())
        sess_id = session['sessionid']
        file = request.files['fileupload']
        file_content = file.read()
        val_outcome, val_error = validate_file(file_content, file.filename)
        if val_outcome:
            pass
        else:
            return render_template('index.html', error=val_error)

        bucket_name = 'anomaly-bucket-data-3'
        storage_client = storage.Client.from_service_account_json(
            'keys/anomaly-detection-hackathon-a1de2720418b.json')
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob('upload/' + str(sess_id) + '.csv')
        blob.upload_from_string(file_content)

        return redirect('/dashboard')


if __name__ == "__main__":
    app.run(debug=True)
