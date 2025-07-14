import cv2
import numpy as np
from PIL import Image
import os
import json

def trainFaceSamples():
    path = "engine/auth/samples"
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("engine/auth/haarcascade_frontalface_default.xml")

    def Images_And_Labels(path):
        ImagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        FaceSamples = []
        ids = []

        # Load existing mappings if available
        if os.path.exists("engine/auth/user_ids.json"):
            with open("engine/auth/user_ids.json", "r") as f:
                names = json.load(f)
        else:
            names = {}

        max_id = max(names.values(), default=0)

        for ImagePath in ImagePaths:
            filename = os.path.split(ImagePath)[-1]
            parts = filename.split('.')
            if len(parts) < 3:
                continue

            username = parts[1]
            gray_img = Image.open(ImagePath).convert('L')
            img_arr = np.array(gray_img, 'uint8')

            # Assign new ID if user not already mapped
            if username not in names:
                max_id += 1
                names[username] = max_id

            user_id = names[username]
            faces = detector.detectMultiScale(img_arr)

            for (x, y, w, h) in faces:
                FaceSamples.append(img_arr[y:y + h, x:x + w])
                ids.append(user_id)

        # Save updated mapping
        with open("engine/auth/user_ids.json", "w") as f:
            json.dump(names, f, indent=4)

        return FaceSamples, ids

    print("Training Faces... Please wait...")
    faces, ids = Images_And_Labels(path)
    recognizer.train(faces, np.array(ids))
    recognizer.write('engine/auth/trainer/trainer.yml')
    print("✅ Model Trained Successfully.")

    delete_face_samples(path)

def delete_face_samples(path):
    count = 0
    for file in os.listdir(path):
        if file.startswith("face.") and file.endswith(".jpg"):
            try:
                os.remove(os.path.join(path, file))
                count += 1
            except Exception as e:
                print(f"Error deleting {file}: {e}")
    print(f"🧹 Deleted {count} face samples from {path}")

# Uncomment this to test
trainFaceSamples()
