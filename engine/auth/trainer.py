import cv2
import numpy as np 
from PIL import Image #import pillow package
import os

def trainFaceSamples():
    path = "engine\\auth\\samples" #Path for samples already taken

    recocgnizer = cv2.face.LBPHFaceRecognizer_create() #Local Binary Patterns Histogram
    detector = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")

    def Images_And_Labels(path): #function to fetch the images and labels 
        ImagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        FaceSamples = []
        ids = []
    
        for ImagePath in ImagePaths: #To iterate particular image path
            gray_img = Image.open(ImagePath).convert('L') #Convert it to grayscale
            img_arr = np.array(gray_img, 'uint8') #Creating an array
        
            id = int(os.path.split(ImagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_arr)
        
            for (x,y,w,h) in faces:
                FaceSamples.append(img_arr[y:y+h, x:x+w])
                ids.append(id)
            
        return FaceSamples, ids

    print("Training Faces, It Will Take Few Seconds, Wait....")

    faces,ids = Images_And_Labels(path)
    recocgnizer.train(faces, np.array(ids))

    recocgnizer.write('engine\\auth\\trainer\\trainer.yml')

    print("Model Trained, Now We Cam Recognize Your Face.")