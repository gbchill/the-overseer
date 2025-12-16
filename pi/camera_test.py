#!/usr/bin/env python3
import cv2 as cv
import time

# open the camera - 0 means the first camera connected (/dev/video0)
cap = cv.VideoCapture(0)

# load the pre-trained face detection model
# this file contains patterns that help recognize faces
face_cascade = cv.CascadeClassifier('models/haarcascade_frontalface_default.xml')

# make sure the camera actually opened
if not cap.isOpened():
    print("ERROR: Cannot open camera")
    exit()

# let the camera warm up by discarding the first few frames
# cameras need time to adjust exposure and focus
print("Warming up camera...")
for i in range(5):
    cap.read()

print("Starting live face detection. Press Ctrl+C to stop.")
print("-" * 50)

try:
    while True:
        # grab a frame from the camera
        ret, frame = cap.read()

        # if we couldn't get a frame, skip this iteration
        if not ret:
            print("WARNING: Failed to read frame")
            continue

        # convert the color frame to grayscale
        # faces are easier to detect in black and white
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # run face detection on the grayscale image
        # scaleFactor: how much to shrink the image at each scale (1.1 = good balance)
        # minNeighbors: how many nearby detections needed to confirm a face (1 = sensitive)
        # minSize: smallest face size to look for in pixels (30x30 = reasonable minimum)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(30, 30))

        # check if we found any faces
        # faces is a list of coordinates, empty if no faces found
        if faces is not None and len(faces) > 0:
            print(f"[{time.strftime('%H:%M:%S')}] Face detected!")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] No face detected.")

        # small delay to avoid overwhelming the output
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n" + "-" * 50)
    print("Stopping face detection...")

# always close the camera when done to free up the resource
cap.release()
print("Camera released. Done!")
