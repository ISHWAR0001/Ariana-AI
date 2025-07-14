import cv2

def TakeFaceSample():
    #Create a video capture object which is helpful to capture video through webcam
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640) # Set video frame width
    cam.set(4, 480) #Set video frame height

    #Haar Cascade classifier is an effective object detection approach
    detector = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')

    #User integer id for every new face (0,1,2,3,4,5,6,7,8,9,.....)
    face_id = input("Enter a numeric user id here : ")

    print("Taking, Sample Look At Camera......")
    count = 0 #Initializing sampling face count 

    while True:
        #Read the frames using the above created object
        ret, img = cam.read()
        #The function converts an input image from one color space to another
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = detector.detectMultiScale(converted_image, 1.3,5)
    
        for(x,y,w,h) in faces:
            #Use to draw a rectangle on any image
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            count += 1
        
            #To capture and save images into the datasets folder 
            cv2.imwrite("engine\\auth\\samples\\face." + str(face_id) + '.' + str(count) + ".jpg", converted_image[y:y+h,x:x+w])
        
            #Used to dispaly image in a window
            cv2.imshow('image', img)
        
        #waits for a pressed key 
        k = cv2.waitKey(100) & 0xff
    
        #Press esc key to stop
        if k == 27:
            break
    
        #Take 50 sample (More sample --> More accuracy) 
        elif count >= 100:
            break
    
    print("Samples taken now closing the program....")
    cam.release()
    cv2.destroyAllWindows()
    
# TakeFaceSample()