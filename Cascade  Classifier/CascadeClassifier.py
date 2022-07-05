import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
eye_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')

def face_detector(image,size=0.5):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    
    if faces is ():
        return image
    #face
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        
        #eye
        eye_gray = gray[y:y+h, x:x+w]
        eye_color = image[y:y+h, x:x+w]
        eyes = eye_classifier.detectMultiScale(eye_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(eye_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
           
    eye_color = cv2.flip(eye_color,1)
    return image
    
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    cv2.imshow("face detector", face_detector(frame))
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
        
cap.release()
cv2.destroyAllWindows()