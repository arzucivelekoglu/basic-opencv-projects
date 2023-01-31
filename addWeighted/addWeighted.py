import cv2
import time


cap = cv2.VideoCapture("walking.avi")

image = cv2.imread("space5.jpg")
image = cv2.resize(image, (768,576))

w = int(cap.get(3)) # 768.0
h = int(cap.get(4)) # 576.0

alpha = 0.4

while True:
    ret, frame = cap.read()
    if ret == True:
        time.sleep(0.02)
        weightedSum = cv2.addWeighted(frame, alpha, image, 1-alpha, 0)
        
        cv2.putText(weightedSum,'alpha:{}'.format(alpha),(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        
        cv2.imshow("Video", weightedSum)
        
    else:
        break
    
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
   
    if k == ord('a'):
        alpha +=0.1
        if alpha >=1.0:
            alpha = 1.0
   
    elif k== ord('d'):
        alpha -= 0.1
        if alpha <=0.0:
            alpha = 0.0

cap.release()
cv2.destroyAllWindows()
