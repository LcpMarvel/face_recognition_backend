from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm.exc import NoResultFound
from time import time

from ..config import app, db, FACE_ENGINES

class Face(db.Model):
  __tablename__ = 'face'

  id = db.Column(db.Integer, primary_key=True)
  encoding = db.Column(JSON)
  face_pp_set = db.Column(db.String)
  face_pp_token = db.Column(db.String, index=True)
  updated_at = db.Column(db.Integer, default=time, onupdate=time, index=True)

  @staticmethod
  def last():
    return Face.query.order_by(-Face.id).first()

  @staticmethod
  def find(id):
    # raise NoResultFound
    return Face.query.get(id)

  def __init__(self, encoding, face_pp_set, face_pp_token):
    self.encoding = encoding
    self.face_pp_set = face_pp_set
    self.face_pp_token = face_pp_token

  def __repr__(self):
    return f"<Face id={self.id} \
    updated_at={self.updated_at} \
    face_pp_set={self.face_pp_set} \
    face_pp_token={self.face_pp_token}>"

  def encodings(self):
    return [
      {
        'engineId': FACE_ENGINES['face_recognition'],
        'faceEncoding': self.encoding
      },
      {
        'engineId': FACE_ENGINES['face_pp'],
        'faceEncoding': self.face_pp_token,
      }
    ]
