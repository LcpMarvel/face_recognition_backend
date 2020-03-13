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
Simply install backend by:
```
$ cd /PATH/TO/face_recognition_backend
$ docker-compose up`
```

# APIs
Backend is a container running on docker which can be used as a web service client in any codebase.

## 1. face
Add a face to face dataset. It generates a image encoding for that face with a given face id.
### Request
http://0.0.0.0/face
### Method
POST
### Parameters
image_url | String | URL of a face image
### Return
JSON Object
#### Success
face_encoding : image encoding data for face dataset and face analyze
face_id: identity for this face image 
#### Failure
error_type: error number
error_message: message for this error
### Sample 
```
#!/usr/bin/env python3
import requests
import json
import sys

payload = { 'image-url': URI/TO/FACE/IMAGE }
result = requests.post('http://backend_url/face', data=payload).json()
```
## 2. face_dataset
Get a set of face data from backend according a specific timestamp range.
### Request
http://0.0.0.0/face_dataset
### Method
POST
### Parameters
timestamp_begin | number 
timestamp_end | number 
### Return
JOSN Object
#### Success
face_set | Array | a set of face encodings and face_id
#### Failure
error_type: error number
error_message: message for this error
### Sample
```
```
# Data Flow
![Data Flow](/doc/FacialRecognitionDataFlow.png)

# See Also
https://github.com/ageitgey/face_recognition

# Lisence
MIT License
