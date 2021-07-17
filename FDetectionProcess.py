import mediapipe as mp
import mediapipe
import cv2
import time
import math
import pandas as pd
print("Imported Successfully")


class FDetection:
    startAt=-1
    flags = pd.DataFrame({'flag' : [],'time':[]})
    started =False
    Startreco=-1
    makeHPsleep = False
    outputs= [] 
    faceDetection = mp.solutions.face_detection.FaceDetection(0.8)
    

    def blazeface(self,img,HP):
  
 
        results = self.faceDetection.process(img)
        ih, iw, _ = img.shape
        
        


        if(self.started and time.time() - self.startAt >=10  and self.startAt != -1 ):
            Trues=0
            tempdf= self.flags[ time.time() -self.flags['time'] >=  15]
            self.flags= pd.DataFrame({'flag' : [],'time':[]})
            for index, row in tempdf.iterrows():
                if (row['flag'] ==True):
                    Trues =Trues+1

            if(Trues >= 0.85 * len(tempdf)  ):


                if(time.time() - HP.GetLastMovementTime()>=15):
                    self.Startreco= time.time()
                    HP.Real_data=[]
   
                    self.makeHPsleep =True 


            self.started= False
            self.startAt = -1



        else:        


            if results.detections:

                if(self.started == False):
                    self.startAt=time.time()
                    self.started = True

                for id, detection in enumerate(results.detections): 
                    bboxC = detection.location_data.relative_bounding_box
                    x=int(bboxC.xmin * iw)
                    y=int(bboxC.ymin * ih)
                    w =int(bboxC.width * iw)
                    h =int(bboxC.height * ih)

                    if(x<0):
                        x= 0 
                    if(y<0):
                        y=0 
                    #cv2.rectangle(img, (x,y), (x+w,y+h), (67, 67, 67), 1) #draw rectangle in displayed fram
                    self.outputs.append((x,y,w,h))
                self.flags= self.flags.append({'flag':True,'time':time.time()}, ignore_index=True)
            else:
                self.flags= self.flags.append({'flag':False,'time':time.time()}, ignore_index=True)
                



