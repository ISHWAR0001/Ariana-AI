import cv2

def TakeFaceSample():
    cam = cv2.VideoCapture(0, cv2.CAP_MSMF)
    cam.set(3, 640)
    cam.set(4, 480)

    detector = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')

    # 👇 Yeh line input lega user se
    username = input("Enter username: ")

    print(f"Capturing face samples for user: {username}")
    count = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            path = f"engine\\auth\\samples\\face.{username}.{count}.jpg"
            cv2.imwrite(path, gray[y:y + h, x:x + w])
            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff
        if k == 27 or count >= 100:
            break

    print("Samples captured successfully.")
    cam.release()
    cv2.destroyAllWindows()

TakeFaceSample()