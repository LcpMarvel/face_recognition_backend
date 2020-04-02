import os
import requests
import json
from multiprocessing.dummy import Pool as ThreadPool

from .face_interface import FaceInterface, FaceNotFoundException
from ..config import app, FACE_ENGINES
from ..model.face import Face

class FacePP(FaceInterface):
  def encode(self, image_info):
    faces = self._detect(image_info)

    if len(faces) == 0:
      raise FaceNotFoundException

    return self._add_face(faces[0]['face_token'])

  def delete(self, face):
    data = self._api_key()
    data['faceset_token'] = face.face_pp_set
    data['face_tokens'] = face.face_pp_token

    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface'

    r = requests.post(url, data=data)
    r.raise_for_status()

  def detect(self, image_info):
    faces = self._detect(image_info)
    face_locations = list(map(lambda face: face['face_rectangle'], faces))

    face_num =len(face_locations)

    return face_num, face_locations

  def search(self, image_info):
    face = Face.last()
    if not face:
      return []

    faces = self._detect(image_info)
    face_tokens = list(map(lambda face: face['face_token'], faces))
    pool = ThreadPool(4)
    face_pp_set = face.face_pp_set

    def search_face(face):
      token = face['face_token']
      position = face['face_rectangle']
      result = self._search(face_pp_set, token)

      if result:
        face = Face.query.filter(Face.face_pp_token == result['face_token']).one()
        meta_data = json.loads(face.meta_data) if face.meta_data else None

        return {
          'faceId': face.id,
          'faceMetaData': meta_data,
          'position': position,
          'trust': result['confidence'] / 100
        }

    results = pool.map(lambda face: search_face(face), faces)
    pool.close()
    pool.join()

    return results

  def _search(self, face_pp_set, face_token):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    data = self._api_key()
    data['face_token'] = face_token
    data['faceset_token'] = face_pp_set

    r = requests.post(url, data=data)
    r.raise_for_status()
    results = r.json()['results']

    if len(results):
      return results[0]

  def _api_key(self):
    return {
      'api_key': os.environ['FACE_PP_KEY'],
      'api_secret': os.environ['FACE_PP_SECRET']
    }

  def _detect(self, image_info):
    data = self._api_key()

    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'

    if image_info.image_url():
      data['image_url'] = image_info.image_url()
      r = requests.post(url, data=data)
    else:
      files = { 'image_file': open(image_info.path, 'rb') }
      r = requests.post(url, data=data, files=files)

    r.raise_for_status()
    result = r.json()

    return result['faces']

  def _add_face(self, face_token):
    face = Face.last()

    if face and face.face_pp_set:
      try:
        self._add_face_by_face_set(face.face_pp_set, face_token)
        return face.face_pp_set, face_token
      except requests.exceptions.RequestException as e:
        r = e.json()

        if r['error_message'] == 'error_message':
          return self._create_face_set_and_add_face(face_token)
        else:
          raise e
    else:
      return self._create_face_set_and_add_face(face_token)

  def _add_face_by_face_set(self, face_set, face_token):
    data = self._api_key()
    data['faceset_token'] = face_set
    data['face_tokens'] = face_token

    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'

    with requests.post(url, data=data) as r:
      r.raise_for_status()
      result = r.json()

  def _create_face_set_and_add_face(self, face_token=None):
    data = self._api_key()
    if face_token:
      data['face_tokens'] = face_token

    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'

    with requests.post(url, data=data) as r:
      r.raise_for_status()

      result = r.json()
      return result['faceset_token'], face_token
