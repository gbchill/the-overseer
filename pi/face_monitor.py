#!/usr/bin/env python3
import cv2 as cv #camera
import threading #two threads
import os  #audio commandd
import time #sleep
import subprocess

face_detected = threading.Event() #shared flag
camera_ready = threading.Event() 

def alarm_loop():
    camera_ready.wait()
    plays = 0
    while not face_detected.is_set():
        proc = subprocess.Popen(['pw-play', '/home/george/the-overseer/pi/audio/alarm_time.wav'])
        plays+=1
        while not face_detected.is_set() and proc.poll() is None:
            time.sleep(0.1)
        if face_detected.is_set():
            proc.kill()
            break
        if plays >= 2:
            face_detected.set()
            break
    print("alarm stopped")

def camera_loop():
    cap = cv.VideoCapture(0)
    face_cascade = cv.CascadeClassifier('/home/george/the-overseer/pi/models/haarcascade_frontalface_default.xml')

    print("Warming up camera...")
    for i in range(5):
        cap.read()
    camera_ready.set()

    print("Camera watching for face...")
    while not face_detected.is_set():
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        print(f"Faces detected: {len(faces) if faces is not None else 0}")
        if faces is not None and len(faces) > 0:
            print("Face confirmed! Stopping alarm...")
            face_detected.set()
            break


        time.sleep(0.5)
    
    cap.release()


if __name__ == "__main__":
    
    os.system('rfkill unblock bluetooth')
    os.system('bluetoothctl power on')
    SPEAKER_MAC = "88:92:CC:C4:AF:53"
    bt_status = os.popen(f'bluetoothctl info {SPEAKER_MAC}').read()
    if 'Connected: yes' not in bt_status:
        os.system(f'bluetoothctl connect {SPEAKER_MAC}')
        time.sleep(5)  # give PipeWire time to register


    alarm_thread = threading.Thread(target=alarm_loop, daemon=True)
    camera_thread = threading.Thread(target=camera_loop, daemon=True)

    alarm_thread.start()
    camera_thread.start()

    alarm_thread.join()
    camera_thread.join()




