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

## 1. face (Create & Update)
Add a face to face dataset. It generates an image encoding for that face with a given face id.

### Method
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image-url | string | URL of a face image
face-id | number | identity for this face image, for updating an existed face data (optional)

#### Return
Return | Type | Description
------ | ---- | -----------
faceId | number | identity for this face image 
faceEncoding | string | image encoding data for face dataset and face analyze
updateAt | number | timestamp for adding face 

### ex. 
```
{
	"faceId" :
	"faceEncoding" : [
				{
					"engineId" :
					"encoding" : 
				}，
				...
			]
	"updateAt" :
}
```

## 2. face/[face-id-to-get]
Get a face data from backend according to a specific face id.

### Method
GET

#### Return
Return | Type | Description
------ | ---- | -----------
faceId | number | identity for this face
faceEncoding | string | encoding for the face

### ex. 
```
{
	"faceId" :
	"faceEncoding" : [
				{
					"engineId" :
					"encoding" : 
				}，
				...
			]
}
```

## 3. face/[face-id-to-delete]/delete
Remove a face from the face data set.

### Method 
POST
  
#### Success
Return | Type | Description
------ | ---- | -----------

## 4. face/sync （deprecated）
Get a set of face data from backend according to a specific timestamp range.

### Method
GET

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
last-updated-at | number | latest update timestamp （optional），eitherwise return all faces.

#### Return
Return | Type | Description
------ | ---- | -----------
faces | Array | a set of face encodings and face ids

### ex.
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
image-url | String | face image to campare
engine-id | Number | face recognition engine id
  
#### Return
Return | Type | Description
------ | ---- | -----------
faces | Array | a set of face encodings and face id

#### Object of faces:
Return | Type | Description
------ | ---- | -----------
faceId | number | identity for this face
trust | number | match ranking, 0-100
position | Object | found face locations in css (top, right, bottom, left) order
timeSpent | Number | millisecond of recognizing time

#### ex.
```
{
	“faces” : [
		 {
			“faceId”:
			“faceEncoding” :
			“position” :
				{	
					“top” :
					“left” :
					“bottom” :
					“right” :
				}
		},
		…
	]
	"timeSpent" :
}
```

## 5. face/detect
Detect faces from the image.

### Method 
POST

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
image-url | String | face image to campare
engine-id | Number | face recognition engine id
  
#### Success
Return | Type | Description
------ | ---- | -----------
faces | Array | a set of face encodings and face_id
timeSpent | Number | millisecond of recognizing time

#### ex.
```
{
	“faces” : [
		  {
			“faceId” :
			“faceEncoding” :
			“position” :
				{	
					“top” :
					“left” :
					“bottom” :
					“right”:
				}
		},
		…
	]，
	“timeSpent” :
}
```

## 6. face/engines
get all face recognition engines supported in this system.

### Method 
GET

### Parameters
Parameters | Type | Description
---------- | ---- | -----------
  
#### Success
Return an array of engines with following data:

Return | Type | Description
------ | ---- | -----------
id | Number | face engine id
name | String | face engine name

#### ex.
```
[
	{
		"id" : 1
		“name” : "face recognition"
	},
	{
		"id" : 2
		"name" : "face++"
	},
	…
]

```

## How to deploy

### How to add user for deploy
1. Connect to server `ssh root@server_ip_address`
2. Run `adduser ubuntu` to add a user
3. Run `usermod -aG sudo ubuntu` to add user to to sudo group
4. Run `update-alternatives --config editor` to update default editor, vim is better
5. Run `visudo` and append `ubuntu ALL=(ALL) NOPASSWD:ALL` to the end of the file
6. Run `su - ubuntu` to switch to that user
7. Clone this repo
8. `cd /PATH/TO/face_recognition_backend`
9. Run `./init-docker.sh` to install docker
10. Run `docker-compose up -d`
11. Run `docker-compose logs -f web`
12. Kill this log when everything is ready
13. Run `docker-compose exec web bash -c 'flask db upgrade'`

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
