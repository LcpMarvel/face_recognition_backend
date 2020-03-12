# Summary
This is a lite and fast facial analyze SDK can be used in face recognition application.  

# Description
As a facial recognition services, it includes some facial analyze process such as face detect, face search and face comparison. face_recoginition_backend, which is running on a backend server, collects the face samples upload from user, manage it in the face dataset. face_recoginition_frontend, which is running on a client such as andorid and ios, detects and verifies the faces from its live camera. 
It built using dlib's state-of-the-art face recognition built with deep learning. It also provides a simple face_recognition command line tool to let you do a face recognition by a live carema.

# Features
* Facial recognition from a video camera of a android device.
* Offline facial recognition on android device
* Facial sample collecting by a image url.
* Facial sample management in backend.
* Provides a tool to syncronize facial samples automatically between frontend and backend.
* Provides a simple face recognition command line tool.

# Installations
## Requirements
* Python 3.8.0
* Docker 19.03.4

## Installation on Mac OSX
Simply install backend service at the root of this project by:
```
$ cd /PATH/TO/face_recognition_backend
$ docker-compose up`
```

# Usage
Backend tool can be used as a web api by web service client or codebase.All you need is to create a http post with an image-url as a parameter. It returns a image encoding with a given face id. 
Here is a sample call this service in Python 
```
#!/usr/bin/env python3
import requests
import json
import sys

payload = { 'image-url': URI/TO/FACE/IMAGE }
result = requests.post('http://backend_url/face', data=payload).json()

```
See Also
https://github.com/ageitgey/face_recognition

# Lisence
MIT License
