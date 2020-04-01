import os
from werkzeug.utils import secure_filename
import requests

from ..errors import InvalidImageException, ImageNotFoundException
from ..config import app, db
from ..model.face import Face

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class ImageInfo:
  path = None
  url = None

  def __init__(self, request):
    self.path = self._get_image_file_from_request(request)
    self.url = self._get_image_url_from_request(request)

    if (self.url is None) and (self.path is None):
      raise ImageNotFoundException()

  def image_url(self):
    return self.url

  def image_path(self):
    if self.path:
      return self.path
    else:
      self.path = download_image(self.url)
      return self.path

  def delete_file(self):
    if self.path:
      delete_file(self.path)

  def _get_image_url_from_request(self, request):
    image_url = request.form.get('image-url')

    if image_url:
      return image_url

    image_key = request.form.get('image-key')

    if image_key:
      return f"{app.config['OSS_HOST']}/{image_key}"

  def _get_image_file_from_request(self, request):
    file = request.files.get('image')

    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(image_path)

      return image_path

def image_info_from_request(request):
  return ImageInfo(request)

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
