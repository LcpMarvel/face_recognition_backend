import os
import time
import numpy as np
import requests
import json
from flask import jsonify, request, Response

from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import face_recognition

from .config import app, db, FACE_ENGINES
from .model.face import Face
from .helper.image_info import allowed_file, image_info_from_request, delete_file
from .errors import InvalidImageException, ImageNotFoundException, InvalidEngineException
from .service.face_service import face_engines, add_face, update_face, \
  remove_face, detect_face, search_face
from .service.face_pp import FacePP

# ----------------- Error handler -----------------
@app.errorhandler(ImageNotFoundException)
def handle_image_not_found(e):
  return jsonify(error='Image not found or unsupported!'), 400

@app.errorhandler(InvalidEngineException)
def handle_engine_error(e):
  return jsonify(error='You have to set correct engine!'), 400

@app.errorhandler(InvalidImageException)
def handle_bad_image(e):
  return jsonify(error='Image URL is invalid'), 400

@app.errorhandler(requests.exceptions.RequestException)
def handle_bad_request(e):
  return jsonify(error=e.response.text), 400

# ----------------- Routers -----------------
@app.route('/ping', methods=['GET', 'POST'])
def ping():
  return jsonify(pong='pong')

@app.route('/engines')
def engines():
  return jsonify(face_engines())

@app.route('/faces', methods=['GET'])
def all_faces():
  faces = Face.query.all()

  def serialize_face(face):
    return {
      'faceId': face.id,
      'metaData': json.loads(face.meta_data) if face.meta_data else None,
      'updatedAt': face.updated_at
    }

  return jsonify(list(map(serialize_face, faces)))

@app.route('/face', methods=['POST'])
def upload_face():
  face_id = request.form.get('face-id')
  image_info = image_info_from_request(request)
  meta_data = request.form.get('meta-data')

  if face_id:
    face = update_face(face_id, image_info, meta_data)
  else:
    face = add_face(image_info, meta_data)

  image_info.delete_file()

  meta_data = json.loads(face.meta_data) if face.meta_data else None
  return jsonify(faceId=face.id, faceEncodings=face.encodings(), updatedAt=face.updated_at, metaData=meta_data)

@app.route('/face/<face_id>')
def query_face(face_id):
  face = Face.find(face_id)

  if face:
    meta_data = json.loads(face.meta_data) if face.meta_data else None

    return jsonify(faceId=face.id, faceEncodings=face.encodings(), updatedAt=face.updated_at, metaData=meta_data)
  else:
    return jsonify(error="Face Not Found!"), 404

@app.route('/face/<face_id>/delete', methods=['POST'])
def delete_face(face_id):
  remove_face(face_id)

  return jsonify(faceId=face_id)

# @app.route('/face/sync')
# def sync_faces():
#   last_updated_at = request.args.get('last-updated-at')
#
#   faces = []
#   if last_updated_at:
#     faces = Face.query.filter(Face.updated_at >= last_updated_at)
#   else:
#     faces = Face.query.all()
#
#   return jsonify(list(map(serialize_face, faces)))

@app.route('/face/detect', methods=['POST'])
def face_detect():
  image_info = image_info_from_request(request)
  engine_id = request.form.get('engine-id')

  face_num, face_locations = detect_face(engine_id, image_info)

  image_info.delete_file()

  return jsonify(num=face_num, locations=face_locations)

@app.route('/face/detect-age-and-gender', methods=['POST'])
def face_detect_age_and_gender():
  image_info = image_info_from_request(request)
  engine_id = request.form.get('engine-id')

  if int(engine_id) == FACE_ENGINES['face_pp']:
    face_num, face_locations, age_and_genders = FacePP().age_and_gender(image_info)

    return jsonify(num=face_num, locations=face_locations, attributes=age_and_genders)
  else:
    return jsonify(error="Not Support!"), 400

@app.route('/face/match', methods=['POST'])
def face_search():
  image_info = image_info_from_request(request)
  engine_id = request.form.get('engine-id')

  start_time = time.time()
  results = search_face(engine_id, image_info)

  time_spent = (time.time() - start_time) * 1000

  image_info.delete_file()

  return jsonify(faces=results, timeSpent=time_spent)

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

@app.route('/reset', methods=['POST'])
def reset():
  for face_pp_set in Face.query.distinct(Face.face_pp_set):
    FacePP().delete_set(face_pp_set, force=True)

  Face.query.delete()
  db.session.commit()

  return jsonify(result="ok")

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
