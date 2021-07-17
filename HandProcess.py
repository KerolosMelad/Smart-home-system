import mediapipe as mp
import mediapipe
import os
import cv2
import time
import math
import pandas as pd
print("Imported Successfully")

def get_Euclidean_DistanceAB(a_x,  a_y,  b_x,  b_y) :
    
    dist = (a_x - b_x) ** 2  + (a_y - b_y)** 2;
    return math.sqrt(dist)


def getAngleABC( a_x,  a_y,  b_x,  b_y,  c_x,  c_y) :
    
    ab_x = b_x - a_x
    ab_y = b_y - a_y
    cb_x = b_x - c_x
    cb_y = b_y - c_y

    dot = ab_x * cb_x+ ab_y * cb_y 
    cross = ab_x * cb_y - ab_y * cb_x 

    alpha = math.atan2(cross, dot)

    return alpha
    
    

class Hand_Process :  
    previous_x_center =-1000
    previous_y_center = -1000
    FramTHreshold =2
    Gestures_T =[] 
    move = False
    StarAT=-1
    prev_Gesture=""
    Real_data=[]

    Startreco = -1
    makeFDsleep=False
    frameCounter=0
    
    handsModule = mediapipe.solutions.hands
    drawingModule = mediapipe.solutions.drawing_utils
    
    
    def __init__(self):
        pass
    
    def GetLastMovementTime(self):
        if(len(self.Real_data) != 0):
            return  self.Real_data[len(self.Real_data)-1][1]
        else :
            return -1 

    def Hand(self,frame): #
         
        timeToRecognition = 1.7

        if(self.move == True and (time.time() - self.StarAT >=timeToRecognition) and  self.StarAT !=-1 ): # Takes 2 seconds to recognize movment 
            pivot = 0 
            while pivot < len(self.Gestures_T):
                if(self.Gestures_T[pivot][1] >=  self.StarAT):
                    break 
                pivot =pivot+1
            tempdf= self.Gestures_T[ pivot : len(self.Gestures_T)]
            self.Gestures_T =[]
                    
            
            right=0
            left =0 
            NonDeFinedgestureflag=False
            for (gesture, _) in tempdf :
                if (gesture == 'right'):
                    right =right+1
                elif  (gesture == 'left'):
                    left=left+1

            if(right >= 0.8 *len(tempdf) ):
                self.prev_Gesture="Swiping Right"
            elif(left >= 0.8 * len(tempdf)):
                self.prev_Gesture="Swiping Left"
            else:
                self.prev_Gesture="NOT a predifiend Gesture"
                NonDeFinedgestureflag =True


            self.Real_data.append((self.prev_Gesture, time.time()))

            self.Startreco = time.time()
            self.sleep =True 


            self.StarAT = -1
            self.move= False
            self.previous_x_center= -1000
            self.previous_y_center =-1000

        else :
            frameHeight,frameWidth,_=frame.shape 
            mouvementDistanceFactor = 0.02
            mouvementDistanceThreshold =-1


            with self.handsModule.Hands(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.7, max_num_hands=1) as hands:

                    STime = time.time()

                    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    if results.multi_hand_landmarks != None:
                        for handLandmarks in results.multi_hand_landmarks:

                            for point in self.handsModule.HandLandmark:
                                normalizedLandmark = handLandmarks.landmark[point]
                                pixelCoordinatesLandmark = self.drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, frameWidth, frameHeight)
                                cv2.circle(frame, pixelCoordinatesLandmark, 5, (255, 255, 255), -1)


                            thumbIsOpen = False
                            firstFingerIsOpen = False
                            secondFingerIsOpen = False
                            thirdFingerIsOpen = False
                            fourthFingerIsOpen = False

                            pseudoFixKeyPoint = handLandmarks.landmark[2].x *frameWidth
                            if(pseudoFixKeyPoint<handLandmarks.landmark[17].x *frameWidth):
                                if (handLandmarks.landmark[3].x*frameWidth < pseudoFixKeyPoint and handLandmarks.landmark[4].x*frameWidth < pseudoFixKeyPoint):
                                    thumbIsOpen = True
                            elif (handLandmarks.landmark[3].x*frameWidth > pseudoFixKeyPoint and handLandmarks.landmark[4].x*frameWidth > pseudoFixKeyPoint):
                                thumbIsOpen = True


                            pseudoFixKeyPoint =handLandmarks.landmark[6].y*frameHeight
                            if (handLandmarks.landmark[7].y*frameHeight < pseudoFixKeyPoint and handLandmarks.landmark[8].y*frameHeight< pseudoFixKeyPoint):
                                firstFingerIsOpen = True


                            pseudoFixKeyPoint = handLandmarks.landmark[10].y*frameHeight
                            if (handLandmarks.landmark[11].y*frameHeight < pseudoFixKeyPoint and handLandmarks.landmark[12].y*frameHeight < pseudoFixKeyPoint):
                                secondFingerIsOpen = True

                            pseudoFixKeyPoint = handLandmarks.landmark[14].y*frameHeight
                            if (handLandmarks.landmark[15].y*frameHeight < pseudoFixKeyPoint and handLandmarks.landmark[16].y*frameHeight< pseudoFixKeyPoint):
                                thirdFingerIsOpen = True


                            pseudoFixKeyPoint = handLandmarks.landmark[18].y*frameHeight
                            if (handLandmarks.landmark[19].y*frameHeight< pseudoFixKeyPoint and handLandmarks.landmark[20].y*frameHeight < pseudoFixKeyPoint):
                                fourthFingerIsOpen = True



                            sp =(int(handLandmarks.landmark[20].x*frameWidth) , int(handLandmarks.landmark[12].y * frameHeight))
                            ep =(int(handLandmarks.landmark[4].x *frameWidth),int(handLandmarks.landmark[0].y *frameHeight))
                            temp = ep[1]-sp[1]

                            mouvementDistanceThreshold = mouvementDistanceFactor * (temp)*3 # Big Threshold to neglect small movement


                            cv2.rectangle(frame, sp,ep ,(67, 67, 67) , 2)

                            if (thumbIsOpen and  firstFingerIsOpen and secondFingerIsOpen and thirdFingerIsOpen and fourthFingerIsOpen):

                                if(self.frameCounter %self.FramTHreshold == 0  ):

                                    x_center = int((handLandmarks.landmark[5].x +handLandmarks.landmark[9].x+handLandmarks.landmark[13].x+handLandmarks.landmark[17].x ) *frameWidth)/4
                                    y_center =int((handLandmarks.landmark[5].y+handLandmarks.landmark[9].y+handLandmarks.landmark[13].y+handLandmarks.landmark[17].y ) *frameHeight)/4
                                    cv2.circle(frame, (int(x_center),int(y_center)), 5, (0, 0, 255), -1)
                                    if (self.previous_x_center != -1000) :
                                        mouvementDistance = get_Euclidean_DistanceAB(x_center, y_center,self.previous_x_center, self.previous_y_center)
                                        if (mouvementDistance > mouvementDistanceThreshold):
                                            angle  =math.degrees(getAngleABC(x_center, y_center, self.previous_x_center, self.previous_y_center, self.previous_x_center + 0.1, self.previous_y_center))

                                            if (angle >= -45 and  angle < 45 and  angle != 0 ):

                                                at=time.time()
                                                self.Gestures_T.append(('left', at))
                                                if(self.move!= True):
                                                    self.StarAT=at
                                                    self.move= True




                                            elif (angle >= 135 or angle < -135):
                                                #print("right")
                                                at=time.time()
                                                self.Gestures_T.append(('right', at))
                                                if(self.move!= True):
                                                    self.StarAT=at
                                                    self.move= True







                                    self.previous_x_center = x_center;
                                    self.previous_y_center = y_center;



                    self.frameCounter = self.frameCounter +1
                    #print("here final")

