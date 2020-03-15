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

# Data Flow
![Data Flow](/doc/FacialRecognitionDataFlow.png)

# APIs
Backend is a container running on docker which can be used as a web service client in any codebase.

## 1. face (Create)
Add a face to face dataset. It generates a image encoding for that face with a given face id.

### Request
http://0.0.0.0/face

### Method
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image_url | string | URL of a face image

### Return
JSON Object

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

## 2. face (Get)
Get a face data from backend according to a specific face_id.

### Request
http://0.0.0.0/face

### Method
GET

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
face_id | number | identity for this face

### Return
JOSN Object

#### Success
Return | Type | Description
------ | ---- | -----------
face_encoding | string | encoding for the face

#### Failure
Return | Type | Description
------ | ---- | -----------
error_message | string | error message

### Sample
```
```

## 3. face_dataset
Get a set of face data from backend according to a specific timestamp range.

### Request
http://0.0.0.0/face_dataset

### Method
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
timestamp_begin | number | time range begin
timestamp_end | number | time range end
faceset_id | Number | id for the face data set, optional

### Return
JOSN Object

#### Success
Return | Type | Description
------ | ---- | -----------
face_set | Array | a set of face encodings and face_id

#### Failure
Return | Type | Description
------ | ---- | -----------
error_type | number | error code
error_message | string | error message

### Sample
```
```

## 4. face/match
detect the face from the image and compare all the detected face with the face data set.
### Method 
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image_url | String | face image to campare
faceset_id | Number | id for the face data set, optional
  
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
	face_id Number
	face_attributes Object
	trust Number  0-100
#### ex.
```
{
	“faces”:[
	{
			“face_id”:
			“trust”：
			“face_attributes”:
			 {
				“user_id”:
				“user_name”:
				“face_position”:
				{	
					“top”:
					“left”
					“bottom”:
					“right”:
				}
			}
		},
		…
	]
  "error_type"
	"error_message":
}
```

## 5. face/detect
detect faces from the image.

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
	face_id Number
	face_position Object
#### ex.
```
{
	“faces”:[
		{
			“face_id”:
			“face_encoding”:
			“face_position”:
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
update a face image with a existed face id
### Method 
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image_url | String | face image to update
face_id | number | identity for this face
  
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
remove a face from face data set
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

# See Also
https://github.com/ageitgey/face_recognition

# Lisence
MIT License
