import threading
import imutils
import time
import cv2
import numpy as np

from PIL import Image
from kafka import KafkaConsumer
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from io import BytesIO
from flask import render_template

out_frame = None
lock = threading.Lock()

app = Flask(__name__)

time.sleep(2.0)

### Complete the assignment

consumer = KafkaConsumer('video_stream',
                         group_id='web_consumer',
                         bootstrap_servers=['192.168.100.23:9092'])

@app.route('/')
def index():
    return render_template('index.html')

def get_frames():
    global out_frame, lock, consumer

    for message in consumer:
        stream = BytesIO(message.value)
        frame = np.asarray(Image.open(stream))

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = imutils.resize(frame, width=400)

        with lock:
            out_frame = frame.copy()

def generate():
    global out_frame, lock

    while True:
        with lock:
            if out_frame is None:
                continue
            
            (flag, encoded_image) = cv2.imencode(".jpg", out_frame)

            if not flag:
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

####

if __name__ == '__main__':
    t = threading.Thread(target=get_frames)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port='9000', debug=True, threaded=True, use_reloader=False)
