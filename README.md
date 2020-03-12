# Summary
This is a lite and fast facial analyze SDK can be used in face recognition application.  

# Description
As a facial recognition services, it includes some facial analyze process such as face detect, face search and face comparison. face_recoginition_backend, which is running on a backend server, collects the face samples upload from user, manage it in the face dataset. face_recoginition_frontend, which is running on a client such as andorid and ios, detects and verifies the faces from its live camera. 
Built using dlib's state-of-the-art face recognition built with deep learning. 
provides a simple face_recognition command line tool to let you do a face recognition by a live carema.

# Features
* facial recognition from a video camera of a android device.
* offline facial recognition on android device
* facial sample collecting by a image url.
* facial sample management in backend.
* provides a tool to syncronize facial samples automatically between frontend and backend.
* provides a simple face recognition command line tool.

# Installations

1. Run `docker-compose up`

## Requirements
* Python 3.8.0
* Docker 19.03.4

## Frontend Installation

## Backend Installation

# Usage

1. `POST /face` uploads face to server, it gives you the face encodings and an uniq face id.
   1. required param: image-url (string)
   2. optional param: face-id (number) , used to update face.

See Also
https://github.com/ageitgey/face_recognition

# Lisence
MIT License


