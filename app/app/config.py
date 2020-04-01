import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

FACE_ENGINES = {
  'face_recognition': 1,
  'face_pp': 2
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Face PP config
app.config['FACE_PP_OUTER_ID'] = 'FACE_RECOGNITION_BACKEND'

# face recognition config
app.config['FACE_ENCODING_NUM_JITTERS'] = 10
app.config['FACE_ENCODING_MODEL'] = "large"
app.config['FACE_LOCATION_NUM_UNSAMPLE'] = 1
app.config['FACE_COMPARE_TOLERANCE'] = 0.5
app.config['FACE_COMPARE_BY_TOLERANCE'] = 0

# OSS config
app.config['OSS_HOST'] = os.environ['ALIYUN_OSS_HOST']
app.config['OSS_ACCESS_KEY_ID'] = os.environ['ALIYUN_OSS_ACCESS_KEY_ID']
app.config['OSS_ACCESS_KEY_SECRET'] = os.environ['ALIYUN_OSS_ACCESS_KEY_SECRET']
app.config['OSS_BUCKET_NAME'] = os.environ['ALIYUN_OSS_BUCKET_NAME']
app.config['OSS_ROLE_ARN'] = os.environ['ALIYUN_OSS_ROLE_ARN']

db = SQLAlchemy(app)
migrate = Migrate(app, db)
