from .face_recognition import FaceRecognition
from .face_pp import FacePP
from ..model.face import Face
from ..config import db, FACE_ENGINES
from ..errors import InvalidEngineException

def face_engines():
  engines = []
  for name, id in FACE_ENGINES.items():
    engines.append({
      'id': id,
      'name': name
    })

  return engines

def generate_encodings(image_info):
  face_recognition = FaceRecognition()
  face_pp = FacePP()

  encoding = face_recognition.encode(image_info)
  face_pp_set, face_pp_encoding = face_pp.encode(image_info)

  return encoding, face_pp_set, face_pp_encoding

def add_face(image_info, meta_data):
  encoding, face_pp_set, face_pp_encoding = generate_encodings(image_info)

  face = Face(encoding, face_pp_set, face_pp_encoding)
  face.meta_data = meta_data

  db.session.add(face)
  db.session.commit()

  return face

def update_face(face_id, image_info, meta_data):
  face = Face.find(face_id)

  if face:
    encoding, face_pp_set, face_pp_encoding = generate_encodings(image_info)
    face.encoding = encoding
    face.face_pp_set = face_pp_set
    face.face_pp_encoding = face_pp_encoding
    face.meta_data = meta_data

    db.session.commit()

    return face

def detect_face(engine_id, image_info):
  id = int(engine_id)

  if id == FACE_ENGINES['face_recognition']:
    face_recognition = FaceRecognition()
    return face_recognition.detect(image_info)

  if id == FACE_ENGINES['face_pp']:
    face = FacePP()
    return face.detect(image_info)

  raise InvalidEngineException

def search_face(engine_id, image_info):
  id = int(engine_id)

  if id == FACE_ENGINES['face_recognition']:
    return FaceRecognition().search(image_info)
  if id == FACE_ENGINES['face_pp']:
    return FacePP().search(image_info)

  raise InvalidEngineException

def remove_face(face_id):
  face = Face.find(face_id)

  if face:
    FacePP().delete(face)

    db.session.delete(face)
    db.session.commit()
