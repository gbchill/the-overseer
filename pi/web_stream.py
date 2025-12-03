#!/usr/bin/env python3
from flask import Flask, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        # Yield frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return '''
    <html>
        <head>
            <title>Live Camera Feed</title>
        </head>
        <body>
            <h1>The Overseer - Live Feed</h1>
            <img src="/video_feed" width="1280" height="720">
        </body>
    </html>
    '''

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Starting web stream...")
    print("Open browser to: http://overseer.local:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)