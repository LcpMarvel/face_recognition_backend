import numpy as np
import json
import face_recognition
import math

from .face_interface import FaceInterface, FaceNotFoundException
from ..config import app
from ..model.face import Face

class FaceRecognition(FaceInterface):
  def encode(self, image_info):
    file = face_recognition.load_image_file(image_info.image_path())
    encodings = face_recognition.face_encodings(
      file,
      num_jitters=app.config['FACE_ENCODING_NUM_JITTERS'],
      model=app.config['FACE_ENCODING_MODEL']
    )

    if len(encodings) == 0:
      raise FaceNotFoundException

    return encodings[0].tolist()

  def detect(self, image_info):
    face_image = face_recognition.load_image_file(image_info.image_path())
    locations = self._face_locations(face_image)

    face_locations = list(
      map(lambda location: self._convert_location(location), locations)
    )

    face_num =len(face_locations)

    return face_num, face_locations

  def search(self, image_info):
    face_image = face_recognition.load_image_file(image_info.image_path())
    face_locations = self._face_locations(face_image)

    face_encodings = face_recognition.face_encodings(face_image, face_locations)

    faces = Face.query.all()
    known_encodings = []
    known_ids = []
    for face in faces:
      known_encodings.append(face.encoding)
      known_ids.append(face.id)

    face_array = []
    for index in range(len(face_encodings)):
      face_id = -1
      trust = 0
      face_to_check=face_encodings[index]
      position = face_locations[index]
      matches = face_recognition.compare_faces(
        known_encodings,
        face_to_check,
        tolerance=app.config['FACE_COMPARE_TOLERANCE']
      )

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
          trust = self.face_distance_to_conf(face_distances[best_match_index], app.config['FACE_COMPARE_TOLERANCE'])

      if face_id > 0:
        matched_face = Face.find(face_id)
        meta_data = json.loads(matched_face.meta_data) if matched_face.meta_data else None

        face_result = {"faceId": face_id, "faceMetaData": meta_data, "trust": trust, "position": self._convert_location(position)}
        face_array.append(face_result)

    return face_array

  def _face_locations(self, face_image):
    return face_recognition.face_locations(
      face_image,
      number_of_times_to_upsample=app.config['FACE_LOCATION_NUM_UNSAMPLE']
    )

  def _convert_location(self, location):
    [top, right, bottom, left] = location

    return {
      'top': top,
      'left': left,
      'width': right - left,
      'height': bottom - top
    }

  def face_distance_to_conf(self, face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
      range = (1.0 - face_match_threshold)
      linear_val = (1.0 - face_distance) / (range * 2.0)
      return linear_val
    else:
      range = face_match_threshold
      linear_val = 1.0 - (face_distance / (range * 2.0))
      return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
