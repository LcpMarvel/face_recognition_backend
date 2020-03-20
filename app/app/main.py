import os
import numpy as np
from time import time
from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_migrate import Migrate
import requests
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import face_recognition
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# face recognition config
app.config['FACE_ENCODING_NUM_JITTERS'] = 10
app.config['FACE_ENCODING_MODEL'] = "large"
app.config['FACE_LOCATION_NUM_UNSAMPLE'] = 1
app.config['FACE_COMPARE_TOLERANCE'] = 0.5
tolerance=app.config['FACE_COMPARE_BY_TOLERANCE'] = 1

# OSS config
app.config['OSS_HOST'] = os.environ['ALIYUN_OSS_HOST']
app.config['OSS_ACCESS_KEY_ID'] = os.environ['ALIYUN_OSS_ACCESS_KEY_ID']
app.config['OSS_ACCESS_KEY_SECRET'] = os.environ['ALIYUN_OSS_ACCESS_KEY_SECRET']
app.config['OSS_BUCKET_NAME'] = os.environ['ALIYUN_OSS_BUCKET_NAME']
app.config['OSS_ROLE_ARN'] = os.environ['ALIYUN_OSS_ROLE_ARN']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Face(db.Model):
  __tablename__ = 'face'

  id = db.Column(db.Integer, primary_key=True)
  encoding = db.Column(JSON)
  updated_at = db.Column(db.Integer, default=time, onupdate=time, index=True)

  def __init__(self, encoding):
    self.encoding = encoding

  def __repr__(self):
    return f"<Face id={self.id}> updated_at={self.updated_at}"

class InvalidImageException(Exception): pass
class ImageNotFoundException(Exception): pass

# ----------------- Error handler -----------------
@app.errorhandler(ImageNotFoundException)
def handle_image_not_found(e):
  return jsonify(error='Image not found or unsupported!'), 400

@app.errorhandler(InvalidImageException)
def handle_bad_image(e):
  return jsonify(error='Image URL is invalid'), 400

@app.errorhandler(requests.exceptions.RequestException)
def handle_bad_request(e):
    return jsonify(error='bad request!'), 400

# ----------------- Routers -----------------
@app.route('/face', methods=['POST'])
def upload_face():
  face_id = request.form.get('face-id')
  image_path = get_image_from_request(request)

  file = face_recognition.load_image_file(image_path)
  encoding = face_recognition.face_encodings(file, num_jitters=app.config['FACE_ENCODING_NUM_JITTERS'], model=app.config['FACE_ENCODING_MODEL'])[0]

  list = encoding.tolist()

  face = save_face(list, face_id = face_id)

  delete_file(image_path)

  return jsonify(faceId=face.id, faceEncoding=list, updatedAt=face.updated_at)

@app.route('/face/<face_id>')
def query_face(face_id):
  face = load_face(face_id)

  if face:
    return jsonify(faceId=face.id, faceEncoding=face.encoding, updatedAt=face.updated_at)
  else:
    return jsonify(error="Face Not Found!"), 404

@app.route('/face/<face_id>/delete', methods=['POST'])
def delete_face(face_id):
  if face_id:
    delete_face(face_id)

  return jsonify(faceId=face_id)

@app.route('/face/sync')
def sync_faces():
  last_updated_at = request.args.get('last-updated-at')

  faces = []
  if last_updated_at:
    faces = Face.query.filter(Face.updated_at >= last_updated_at)
  else:
    faces = Face.query.all()

  return jsonify(list(map(serialize_face, faces)))

@app.route('/face/detect', methods=['POST'])
def detect_face():
  image_path = get_image_from_request(request)

  face_image = face_recognition.load_image_file(image_path)
  face_locations = face_recognition.face_locations(face_image, number_of_times_to_upsample=app.config['FACE_LOCATION_NUM_UNSAMPLE'])
  face_num =len(face_locations)

  delete_file(image_path)

  return jsonify(num=face_num, locations=face_locations)

@app.route('/face/match', methods=['POST'])
def search_face():
  image_path = get_image_from_request(request)
  face_image = face_recognition.load_image_file(image_path)

  face_locations = face_recognition.face_locations(face_image, number_of_times_to_upsample=app.config['FACE_LOCATION_NUM_UNSAMPLE'])
  face_encodings = face_recognition.face_encodings(face_image, face_locations)
  known_encodings = load_all_face_encodings()
  known_ids = load_all_face_ids()

  face_array = []
  for index in range(len(face_encodings)):
    face_id = -1
    trust = 0
    face_to_check=face_encodings[index]
    position = face_locations[index]
    matches = face_recognition.compare_faces(known_encodings, face_to_check, tolerance=app.config['FACE_COMPARE_TOLERANCE'])

    if app.config['FACE_COMPARE_BY_TOLERANCE']:

      if True in matches:
        first_match_index = matches.index(True)
        face_id = known_ids[first_match_index]
        trust = 100
    else:
        face_distances = face_recognition.face_distance(known_encodings, face_to_check)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
          face_id = known_ids[best_match_index]
          trust = 1 - face_distances[best_match_index]
    
    face = {"face_id": face_id, "trust": trust, "position": position}
    face_array.append(face)
  
  delete_file(image_path)

  return jsonify(faces=face_array)

@app.route('/oss-auth', methods=['POST'])
def oss_auth():
  access_key_id = app.config['OSS_ACCESS_KEY_ID']
  access_key_secret = app.config['OSS_ACCESS_KEY_SECRET']
  bucket_name = app.config['OSS_BUCKET_NAME']
  role_arn = app.config['OSS_ROLE_ARN']

  clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hongkong')
  req = AssumeRoleRequest.AssumeRoleRequest()

  req.set_accept_format('json')
  req.set_RoleArn(role_arn)
  req.set_RoleSessionName('python-face-recognition')
  body = clt.do_action(req)

  return Response(body, mimetype='application/json')

# ----------------- Helpers -----------------
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_from_request(request):
  image_url = request.form.get('image-url')

  if image_url:
    return download_image(image_url)

  file = request.files.get('image')
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(image_path)

    return image_path

  image_key = request.form.get('image-key')
  if image_key:
    return download_image(f"{app.config['OSS_HOST']}/{image_key}")

  raise ImageNotFoundException()

def download_image(url):
  local_filename = url.split('/')[-1]
  path = '/tmp/' + local_filename

  try:
    with requests.get(url, stream=True) as r:
      r.raise_for_status()

      with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
          if chunk:
            f.write(chunk)
  except requests.exceptions.RequestException:
    raise InvalidImageException()

  return path

def delete_file(path):
  if os.path.exists(path):
    os.remove(path)
  else:
    print("The file %s does not exist!", path)

def serialize_face(face):
  return {
    'faceId': face.id,
    'faceEncoding': face.encoding,
    'updatedAt': face.updated_at,
  }

def load_face(face_id=None):
  if face_id:
    faces = Face.query.get(face_id)
  else:
    faces = Face.query.all()

  return faces

def load_all_face_encodings():
  faces = load_face()
  return list(map(lambda face: face.encoding, faces))

def load_all_face_ids():
  faces = load_face()
  return list(map(lambda face: face.id, faces))

def save_face(list, face_id=None):
  if face_id:
    face = load_face(face_id)

    if face:
      face.encoding = list
      db.session.commit()
      return face
  else:
    face = Face(list)
    db.session.add(face)
    db.session.commit()
    return face

def delete_face(face_id):
  face = load_face(face_id)
  if face:
    db.session.delete(face)
    db.session.commit()

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
