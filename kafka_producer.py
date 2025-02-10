import time
import cv2

from kafka import KafkaProducer, producer
from imutils.video import VideoStream

vs = VideoStream(src=0).start()
time.sleep(2.0)

producer = KafkaProducer(bootstrap_servers=['192.168.100.23:9092'])
cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    frame = vs.read()




    #gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) # FILTRO Detector Facial

    #objects = cascade.detectMultiScale(gray, 1.1, 4)#  FILTRO Detector Facial

    #for (x, y, w, h) in objects:  #FILTRO Detector Facial
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # FILTRO Detector Facial


    #frame = cv2.Canny(frame, 100, 250)  #frame es la imagen , 100 el valor minimo y 250 el maximo  FILTRO CANNY


    #_, frame = cv2.threshold(frame, 100, 250, cv2.THRESH_BINARY_INV) # FILTROThresholding


    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # FILTRO HSV

    ret, buffer = cv2.imencode(".jpg", frame)

    producer.send('video_stream', buffer.tobytes())
    producer.flush()

vs.close()