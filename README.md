# Summary
This is a lite and fast facial analysis SDK that can be used in face recognition applications.  

# Description
As facial recognition services, it includes facial analysis processes such as face detect, face search and face comparison. face_recoginition_backend, which is running on a backend server, collects the face samples upload from a user, manages it in the face dataset. face_recoginition_frontend, which is running on a client such as android and ios, detects and verifies the faces from its live camera. 
It built using dlib's state-of-the-art face recognition built with deep learning. It also provides a simple face_recognition command-line tool to let you do a face recognition by a live camera.

# Features
* Facial recognition from a video camera of an android device.
* Offline facial recognition on android device
* Facial sample collecting by an image URL.
* Facial sample management in backend.
* Provides a tool to synchronize facial samples automatically between frontend and backend.
* Provides a simple face recognition command-line tool.

# Installations
## Requirements
* Python 3.8.0
* Docker 19.03.4

## Installation on Mac OSX
Simply install backend by:
```
$ cd /PATH/TO/face_recognition_backend
$ docker-compose up
```

# Data Flow
![Data Flow](/doc/FacialRecognitionDataFlow.png)

# APIs
Backend is a container running on docker which can be used as a web service client in any codebase.

## 1. face (Create)
Add a face to face dataset. It generates an image encoding for that face with a given face id.

### Method
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image_url | string | URL of a face image
unique_args | Object | customized attributes for this face, such as user id, user name, etc. (optional)

#### Success
Return | Type | Description
------ | ---- | -----------
face_encoding | string | image encoding data for face dataset and face analyze
face_id | number | identity for this face image 

#### Failure
Return | Type | Description
------ | ---- | -----------
error_type | number | error code
error_message | string | error message

### Sample 
```
#!/usr/bin/env python3
import requests
import json
import sys

payload = { 'image-url': URI/TO/FACE/IMAGE }
result = requests.post('http://backend_url/face', data=payload).json()
```

## 2. face (TODO)
Get a face data from backend according to a specific face_id.

### Method
GET

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
face_id | number | identity for this face


#### Success
Return | Type | Description
------ | ---- | -----------
face_encoding | string | encoding for the face
unique_args | Object | customized attributes for this face, such as user id, user name, etc.

#### Failure
Return | Type | Description
------ | ---- | -----------
error_message | string | error message

### Sample
```
```

## 3. faces/sync
Get a set of face data from backend according to a specific timestamp range.

### Method
GET

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
last_updated_at | number | latest update timestamp

#### Success
Return | Type | Description
------ | ---- | -----------
faces | Array | a set of face encodings and face ids

#### Failure
Return | Type | Description
------ | ---- | -----------
error_type | number | error code
error_message | string | error message

### Sample
```
[
    {
        "faceEncoding":
        "faceId": 
        "updatedAt":
    },
    ...
]
```

## 4. face/match
Detect the face from the image and compare all the detected face with the face data set.

### Method 
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image_url | String | face image to campare
  
#### Success
Return | Type | Description
------ | ---- | -----------
faces | Array | a set of face encodings and face_id

#### Failure
Return | Type | Description
------ | ---- | -----------
error_type | number | error code
error_message | string | error message

#### faces:
Return | Type | Description
------ | ---- | -----------
face_id | number | error code
trust | number | match ranking, 0-100
unique_args | Object | customized attributes for this face, such as user id, user name, etc.
position| Object | a rectangle position of this face

#### ex.
```
{
	“faces”:[
		{
			“face_id”:
			“trust”：
			“unique_args”:
			{
				"user_id":
				"user_name":
			}
			“position”:
			{	
				“top”:
				“left”
				“bottom”:
				“right”:
			}
		
		},
		…
	]
}
```

## 5. face/detect
Detect faces from the image.

### Method 
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image_url | String | face image to campare
  
#### Success
Return | Type | Description
------ | ---- | -----------
faces | Array | a set of face encodings and face_id

#### Failure
Return | Type | Description
------ | ---- | -----------
error_type | number | error code
error_message | string | error message

#### faces:
Return | Type | Description
------ | ---- | -----------
face_id | number | error code
face_encoding | string | encoding for the face
position| Object | a rectangle position of this face

#### ex.
```
{
	“faces”:[
		{
			“face_id”:
			“face_encoding”:
			“position”:
				{	
					“top”:
					“left”
					“bottom”:
					“right”:
				}
		},
		…
	]
	“error_message”:
}
```

## 6. face/update
Update a face image with an existed face id.

### Method 
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image_url | String | face image to update
face_id | number | identity for this face
unique_args | Object | customized attributes for this face, such as user id, user name, etc. (optional)
  
#### Success
Return | Type | Description
------ | ---- | -----------
faces | Array | a set of face encodings and face_id
face_encoding | string | encoding for the face

#### Failure
Return | Type | Description
------ | ---- | -----------
error_type | number | error code
error_message | string | error message

## 7. face/delete
Remove a face from the face data set.

### Method 
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
face_id | number | identity for this face
  
#### Success
Return | Type | Description
------ | ---- | -----------

#### Failure
Return | Type | Description
------ | ---- | -----------
error_type | number | error code
error_message | string | error message

## How to deploy

1. Install `docker` and `docker-compose` on you server
2. git clone this repo
3. `cd /PATH/TO/face_recognition_backend`
4. Run `docker-compose up -d`
5. Run `docker-compose logs -f web`
6. Kill this log when everything is ready
7. Run `docker-compose exec web bash -c 'flask db upgrade'`

### SSH forward
1. Add config to your `~/.ssh/config`
```
Host *
 ForwardAgent yes
```
2. Run `ssh-add ~/.ssh/id_rsa`
3. You can clone private repo on server by your `id_rsa` now

# See Also
https://github.com/ageitgey/face_recognition

# License
MIT License
