# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 01:30:24 2023

@author: 90539
"""

import cvzone
import cv2
import math
import numpy as np
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4, 720)

#detectionCon : algılama güveni, maxHands : aynı anda tespit edeceği el sayısı
detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = [] # Yılanın tüm noktaları
        self.lengths = [] #her nokta arasındaki mesafe
        self.currentLength = 0 # yılanın toplam uzunluğu
        self.allowedLength = 150 # izin verilen toplam Uzunluk
        self.previousHead = 0, 0 # önceki kafa noktası
        
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood,_ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False
        
    def randomFoodLocation(self):
        self.foodPoint = np.random.randint(100,1000),np.random.randint(100,600)
        
    def update(self, imgMain, currentHead):
        
        if self.gameOver:
            cvzone.putTextRect(imgMain, "GameOver", [300,400], scale= 7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f"Your Score: {self.score}", [50,80], scale= 7, thickness=5, offset=10)
            
        else:
            
            px, py = self.previousHead
            cx, cy = currentHead
            
            self.points.append([cx, cy])
            distance = math.hypot(cx- px, cy- py)
            self.lengths.append(distance)
            self.currentLength +=  distance
            self.previousHead = cx, cy
            
            # Boy Azaltma
            if self.currentLength >self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break
            
            
            # yılanın Yiyeceği yiyip yemediğini kontrol edin
            rx , ry = self.foodPoint
            if rx- self.wFood//2 < cx < rx + self.wFood//2 and ry - self.hFood//2 < cy < ry +self.hFood//2:
                self.randomFoodLocation()
                self.allowedLength +=50
                self.score +=1 
                print(self.score)
            
            
            #Draw snake
            if self.points:
                for i,point in enumerate(self.points):
                    if i!=0:
                        cv2.line(imgMain, tuple(self.points[i-1]), tuple(self.points[i]), (0,0,255), 15)
                # img, kordinat, dairenin yarıçapı, renk, daire tipi(içi dolu olsun dedik)
                cv2.circle(imgMain, tuple(self.points[-1]), 20, (200,0,200),cv2.FILLED)
                        
            #cv2.circle(img, tuple(pointIndex), 20, (200,0,200),cv2.FILLED)
            
            #♠Draw Food
            
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,  (rx-self.wFood//2, ry-self.hFood//2))
            cvzone.putTextRect(imgMain, f"Score: {self.score}", [50,80], scale= 3, thickness=5, offset=10)
            
            # check for ceollision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts],False, (0,200,0),3)
            minDist = cv2.pointPolygonTest(pts, (cx,cy), True)
            
            if -1<= minDist<= 1:
                  print("Hit")
                  self.gameOver = True  
                  self.points = [] # all points of the snake
                  self.lengths = [] #distance between each point
                  self.currentLength = 0 # total length of the snake
                  self.allowedLength = 150 # total allowed Length
                  self.previousHead = 0, 0 # previous head point
                  self.randomFoodLocation()
                  
              
              
        return imgMain  
        
        
game =   SnakeGameClass(r"C:\Users\90539\Desktop\cupcake game\cupcake2.png")    

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img, flipType=False)
    
    #ekranda gözüken ilk eli tespit edeceğiz
    #ve tepsit edilen elin işaret parmağına ihtiyacımız var
    # hands[0] : ilk el oluyor
    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
        
    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    cv2.imshow("image",img)
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
       # game.gameOver = False
        break
    
cap.release()
cv2.destroyAllWindows()