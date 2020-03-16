import os
from time import time
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_migrate import Migrate
import requests
import face_recognition

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
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

@app.route('/face', methods=['POST'])
def upload_face():
  face_id = request.form.get('face-id')
  image_url = request.form['image-url']

  image_path = download(image_url)

  file = face_recognition.load_image_file(image_path)
  encoding = face_recognition.face_encodings(file, num_jitters=10, model="large")[0]

  list = encoding.tolist()

  face = save_face_record(list, face_id = face_id)

  delete_file(image_path)

  return jsonify(faceId=face.id, faceEncoding=list, updatedAt=face.updated_at)

@app.route('/faces/sync')
def sync_faces():
  last_updated_at = request.args.get('last_updated_at')

  faces = []
  if last_updated_at:
    faces = Face.query.filter(Face.updated_at >= last_updated_at)
  else:
    faces = Face.query.all()

  return jsonify(list(map(serialize_face, faces)))

def serialize_face(face):
  return {
    'faceId': face.id,
    'faceEncoding': face.encoding,
    'updatedAt': face.updated_at,
  }

def save_face_record(list, face_id=None):
  if face_id:
    face = Face.query.get(face_id)

    if face:
      face.encoding = list
      db.session.commit()

      return face
  else:
    face = Face(list)
    db.session.add(face)
    db.session.commit()

    return face

def download(url):
  local_filename = url.split('/')[-1]
  path = '/tmp/' + local_filename

  with requests.get(url, stream=True) as r:
    r.raise_for_status()

    with open(path, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192):
        if chunk:
          f.write(chunk)

  return path

def delete_file(path):
  if os.path.exists(path):
    os.remove(path)
  else:
    print("The file does not exist!")

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)

#
@app.route('/face/detect', methods=['POST'])
def detect_face():
  image_url = request.form['image-url']
  image_path = download(image_url)

  face_image = face_recognition.load_image_file(image_path)
  face_locations = face_recognition.face_locations(face_image)
  face_num =len(face_locations)
  
  delete_file(image_path)

  return jsonify(num=face_num, locations=face_locations, image_url=image_url)

@app.route('/face/match', methods=['POST'])
def search_face():
  image_url = request.form['image-url']
  image_path = download(image_url)
  
  face_image = face_recognition.load_image_file(image_path)
  face_locations = face_recognition.face_locations(face_image)
  face_encodings = face_recognition.face_encodings(face_image, face_locations)

  face_dataset = load_faceset()
  faceset = list(map(lambda face: face.encoding, face_dataset))
  face_array = []
  
  for index in range(len(face_encodings)):
    face_to_check=face_encodings[index]
    matches = face_recognition.compare_faces(faceset, face_to_check, tolerance=0.4)

    if True in matches:
      first_match_index = matches.index(True)
    
      face_id = face_dataset[first_match_index].id
      position = face_locations[index]
      trust = 100

      face = {"face_id": face_id, "trust": trust, "position": position}
      face_array.append(face)

  delete_file(image_path)

  return jsonify(faces=face_array)  

def load_faceset(face_id=None):
  if face_id:
    faces = Face.query.get(face_id)
  else:
    faces = Face.query.all()

  return faces

@app.route('/face/delete', methods=['POST'])
def delete_face():
  face_id = request.form.get('face-id')
  face = Face.query.get(face_id)
  if face:
    db.session.delete(face)
    db.session.commit()
  return jsonify(faceId=face_id)

    