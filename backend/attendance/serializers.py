from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
# attendance/utils.py

import cv2

def detect_face(username):
    cam = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    captured = False

    while True:
        ret, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow('Face Detection', frame)

        if len(faces) > 0:
            cv2.imwrite(f'media/attendance_faces/{username}.jpg', frame)
            captured = True
            break

        if cv2.waitKey(1) == 13:
            break

    cam.release()
    cv2.destroyAllWindows()

    return captured