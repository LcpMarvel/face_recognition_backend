import os
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
  face_id = db.Column(db.Integer)
  encoding = db.Column(JSON)

  def __init__(self, face_id, encoding):
    self.face_id = face_id
    self.encoding = encoding

  def __repr__(self):
    return f"<Face id={self.id}> face_id={self.face_id}"

@app.route('/face', methods=['POST'])
def upload_face():
  face_id = request.form['face-id']
  image_url = request.form['image-url']

  image_path = download(image_url)

  file = face_recognition.load_image_file(image_path)
  encoding = face_recognition.face_encodings(file)[0]

  list = encoding.tolist()

  save_face_record(face_id, list)

  delteFile(image_path)

  return jsonify(faceId=face_id, encoding=list)

def save_face_record(face_id, list):
  face = Face.query.filter_by(face_id = face_id).first()

  if face:
    face.encoding = list
    db.session.commit()
  else:
    face = Face(face_id, list)
    db.session.add(face)
    db.session.commit()

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

def delteFile(path):
  if os.path.exists(path):
    os.remove(path)
  else:
    print("The file does not exist!")

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
