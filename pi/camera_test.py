#!/usr/bin/env python3
import cv2 as cv

# open the camera - 0 means the first camera connected (/dev/video0)
cap = cv.VideoCapture(0)

# load the pre-trained face detection model
# this file contains patterns that help recognize faces
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# make sure the camera actually opened
if not cap.isOpened():
    print("ERROR: Cannot open camera")
    exit()

# grab a single frame from the camera
ret, frame = cap.read()

# ret is True if we got a frame, False if something went wrong
if not ret:
    print("ERROR: Cannot read frame from camera")
    cap.release()
    exit()

# convert the color frame to grayscale
# faces are easier to detect in black and white
gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

# run face detection on the grayscale image
# scaleFactor: how much to shrink the image at each scale (1.3 = pretty relaxed)
# minNeighbors: how many nearby detections needed to confirm a face (3 = not too strict)
# minSize: smallest face size to look for in pixels (20x20 = pretty small)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(20, 20))

# check if we found any faces
# faces is a list of coordinates, empty if no faces found
if faces is not None and len(faces) > 0:
    print("Face detected!")
else:
    print("No face detected.")

# always close the camera when done to free up the resource
cap.release()
print("Camera released. Done!")
