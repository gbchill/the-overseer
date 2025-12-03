#!/usr/bin/env python3
import cv2

# Open the camera (0 = /dev/video0)
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("ERROR: Cannot open camera")
    exit()

print("Camera opened successfully!")
print("Capturing frame...")

# Read one frame
ret, frame = cap.read()

# Check if frame was captured successfully
if ret:
    # Save the frame as an image
    cv2.imwrite('test.jpg', frame)
    print("SUCCESS! Image saved as test.jpg")
else:
    print("ERROR: Could not read frame")

# Close the camera
cap.release()
print("Camera released. Done!")