import time
import cv2
import os
import json
import pyautogui as p

# Safe for environments without GUI
os.environ["DISPLAY"] = ":99"
p.FAILSAFE = False

def AuthenticateFace():
    flag = 0

    # Load the trained recognizer model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("engine\\auth\\trainer\\trainer.yml")

    # Load face detection Haar Cascade
    cascadePath = "engine\\auth\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    # Load user mapping (ID to username)
    with open("engine\\auth\\trainer\\user_map.json", "r") as f:
        id_to_username = {int(v): k for k, v in json.load(f).items()}

    cam = cv2.VideoCapture(0, cv2.CAP_MSMF)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 100:
                username = id_to_username.get(face_id, "Unknown")
                confidence_display = f"  {round(100 - confidence)}%"
                flag = 1
            else:
                username = "Unknown"
                confidence_display = f"  {round(100 - confidence)}%"
                flag = 0

            cv2.putText(img, str(username), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence_display), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

        if flag == 1:
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag

AuthenticateFace()