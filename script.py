def run(db_pathx):
    import numpy as np
    import mediapipe as mp
    import os
    from os import path,listdir
    import cv2
    import time
    import math
    from PIL import Image
    import pandas as pd
    import threading
    from datetime import datetime , date
    from statistics import mode
    import sys
    import tensorflow.keras.backend as K
    from tensorflow.keras.preprocessing.image import load_img, save_img, img_to_array
    print("packages loaded Successfully")
    
    db_path =db_pathx # Change it depends on your os and db 
    threshold =10 # from 9 ~ 10 
    
    import CreateFacenet
    interpreter , input_details ,output_details = CreateFacenet.GetTheModel(db_path)
    employees = []
    import CreateDB 
    employees =CreateDB.Create_DB(employees,db_path,interpreter , input_details ,output_details)

    #---------------------> Class For Face Recognition Process 

    class Face_Process :   # A class is used mainly for Face Recognition and checking if the person made a gesture within a time window
        #variables needed
        faces = [] # an array save the faces appeard in every frame for 1.5 seconds and then deleted
        Reco = False # a bool variable indicate if recognition process started
        StarAT=-1 # timing variable indicate when recognition process started
        ids=0 # int variable to contain how many person in the frame
        Who="" # String variable includes the names of the persons recognized and unkowns 
        AAction= False # means recognition process done 
        outputs=[] # contains boundind box dimensions and person's name/ unkown to be shown in output frame


        FlagHomeOwner =False
        FlagOpen = False
        FlagClose = False
        FlagNotPRed= False 
        MakeAgesture=False

        faceDetection = mp.solutions.face_detection.FaceDetection(0.8) # mediapipe_BlazeFace  

        #-------

        def findEuclideanDistance(self,source_representation, test_representation):  # get EuclideanDistance between source_representation, anotherrepresentation
            euclidean_distance = source_representation - test_representation
            euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
            euclidean_distance = np.sqrt(euclidean_distance)
            return euclidean_distance
        #--------

        def makeDecision(self):  # Check whether a home owner or guest that made the hand gesture
            pivot = 0 
            while pivot < len(self.faces):  
                if(self.faces[pivot][1] >=  self.StarAT):
                    break 
                pivot =pivot+1

            tempdf= self.faces[ pivot : len(self.faces)]  # Faces recognized in timeToRecognition seconds
            self.faces =[]
            TmpArr= [] 
            countunkowns =0 
            FoundOwner= False
            for id in range(self.ids) : 
                temp2df =[]
                for item in tempdf :
                    if(item[2]==id):
                        temp2df.append(item[0])


                The_real_person=mode(temp2df)
                TmpArr.append(The_real_person)
                if(The_real_person != "unknown"):
                    FoundOwner=True 
                else:
                    countunkowns = countunkowns+1


            if(self.ids!=0 ):
                self.AAction=True
            Gesture_Time_window = 3 
            if(FoundOwner):
                self.FlagHomeOwner = True 
                def listToString(s): 
                    str1 = s[0]
                    for ele in s[1:len(s)]: 
                        str1 =str1+ " and " +ele  
                    return str1 
                self.Who =  listToString(TmpArr)
                TmpArr =[] 
                if(len(HP.Real_data) != 0):
                    gesture_T = HP.Real_data[len(HP.Real_data)-1]
                    T = HP.Real_data[len(HP.Real_data)-1][1]
                    if(self.StarAT -T <= Gesture_Time_window):
                        gesture=gesture_T[0]
                        if (gesture == 'Sliding Right'):
                            self.FlagOpen = True 
                        elif  (gesture == 'Sliding Left'):
                            self.FlagClose = True 
                        elif(gesture == 'NOT a predifiend Gesture'):
                            self.FlagNotPRed =True

            else:
                self.Who =str(countunkowns)+ " unknown\s"
                if(len(HP.Real_data) != 0):
                    tempgestTime= HP.Real_data[len(HP.Real_data)-1][1]
                    if(self.StarAT-tempgestTime <=  Gesture_Time_window):
                        self.MakeAgesture =True
                    else :
                        self.MakeAgesture =False


            self.StarAT = -1
            self.Reco= False


        def FaceReco(self,img,HP): # recognition process
            timeToRecognition =1.5
            if(self.Reco == True and (time.time() - self.StarAT >=timeToRecognition) and  self.StarAT !=-1 ): #takes timeToRecognition seconds to make a perfect recognition
                self.makeDecision()

            else:
                #----- Face Detection 
                results = self.faceDetection.process(img)
                ih, iw, _ = img.shape


                if results.detections:
                    self.ids = len (results.detections)
                    for id, detection in enumerate(results.detections): 
                        bboxC = detection.location_data.relative_bounding_box
                        x=int(bboxC.xmin * iw)
                        y=int(bboxC.ymin * ih)
                        w =int(bboxC.width * iw)
                        h =int(bboxC.height * ih)
                        bboxC =0 
                        results =[] 
                        if(x<0):
                            x= 0 
                        if(y<0):
                            y=0 


                        left_eye_center=(int(detection.location_data.relative_keypoints[0].x * iw) , int(detection.location_data.relative_keypoints[0].y * ih))
                        right_eye_center=(int (detection.location_data.relative_keypoints[1].x * iw) , int(detection.location_data.relative_keypoints[1].y * ih))

                        detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face

                #-----------Face Alignment 
                        left_eye_x = left_eye_center[0]; left_eye_y = left_eye_center[1]
                        right_eye_x = right_eye_center[0]; right_eye_y = right_eye_center[1]



                        if left_eye_y > right_eye_y:

                            point_3rd = (right_eye_x, left_eye_y)
                            direction = -1 #rotate same direction to clock
                        else:

                            point_3rd = (left_eye_x, right_eye_y)
                            direction = 1 #rotate inverse direction of clock
                            #print("rotate to inverse clock direction")

                        def euclidean_distance(a, b):
                            x1 = a[0]; y1 = a[1]
                            x2 = b[0]; y2 = b[1]
                            return math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))
                        a = euclidean_distance(left_eye_center, point_3rd)
                        b = euclidean_distance(right_eye_center, left_eye_center)
                        c = euclidean_distance(right_eye_center, point_3rd)

                        if(b  !=0 and c !=0 ):
                            cos_a = (b*b + c*c - a*a)/(2*b*c)


                            angle = np.arccos(cos_a)


                            angle = (angle * 180) / math.pi

                            if direction == -1:
                                angle = 90 - angle
                            new_img = Image.fromarray(detected_face)
                            new_img = np.array(new_img.rotate(direction * angle))
                        else :
                            new_img = Image.fromarray(detected_face)
                            new_img = np.array(new_img)


                 #-----------Feature Extraction
                        detected_face =[] 
                        new_img = cv2.resize(new_img, (160, 160)) 
                        img_pixels = np.expand_dims(new_img, axis = 0)
                        new_img=[]
                        mean, std = img_pixels.mean(), img_pixels.std()
                        img_pixels = (img_pixels-mean)/std
                        img_pixels= np.array(img_pixels, dtype=np.float32)
                        interpreter.set_tensor(input_details[0]['index'],img_pixels )
                        interpreter.invoke()
                        captured_representation = interpreter.get_tensor(output_details[0]['index'])
                        K.clear_session()
                        img_pixels=[]
                        label_name = 'unknown'
                        for i in employees:
                            employee_name = i[0]
                            source_representation = i[1]
                            distance = self.findEuclideanDistance(captured_representation, source_representation)
                            if distance <= threshold:
                                label_name = employee_name
                                captured_representation =[] 
                                break

                        at = time.time()    

                        if(self.Reco!= True):
                            self.StarAT=at
                            self.Reco= True

                        self.faces.append((label_name,at,id))
                        self.outputs.append((x,y,w,h,label_name))





    # _Mobile App 
    import FCMManager as fcm


    import cloudstorage 
    storage,db  = cloudstorage.start()


    def DBHomeowners():
        db.child("homeowners").remove()
        HomeownerPath=db_path+"/"+"HomeOwners"
        for employee in listdir(HomeownerPath):
            if(employee != 'representations.pkl'):
                #print("upload",employee )
                db.child("homeowners").push({"name" :employee   })


    DBHomeowners()               



    def notify(msg,counterguest):
        token = ["dfUj_ISOQuaPzVvFychbyv:APA91bFKxA3ldNKHgA0W4c_yAZ1HFyZTfjUS8rtB_Xb-FbLyFWy7e3GS_iHmpJ9gHsAkmrm6ObTyOfTDpub5iPE2tgOr_M7kr4IRf6SVdyMRunQn7sbav87gXAP-b_e84HftSCgcVTz_"]
        fcm.sendPush("Door Notification",msg, token , "guest"+str(counterguest)+".jpg")
        db.child("notification").remove()
        db.child("notification").push({"notification" : "yes"})


    #-----------------------




    def upload_To_Cloud_AND_PC(imgname , frame,counterguest):
        cv2.imwrite(imgname, frame)
        storage.child("guest"+str(counterguest)+".jpg").put(imgname)
        #print("guest"+str(counterguest)+".jpg" , " uploaded")



    #-----------------





    def open():
        print("actuator open")


    def close():
        print("actuator close")

    class FireDB :
        systemOnFlag = True;
        counterguest = 1

        def checkdb(self):
            if(db.child("smartdoor").get().val()):
                action =db.child("smartdoor").get().val()
                db.child("smartdoor").remove()
                if(action == 'open'):
                    open()
                else:
                    close()
            if(db.child("appsystem").get().val()):
                system =db.child("appsystem").get().val()
                db.child("appsystem").remove()
                if(system == 'systemOff'):
                    #print("system of pushed")
                    self.systemOnFlag= False



    def goUpdateDB(who , action , time):

        db.child("log").push({"person" :who, "action" : action , "time": time})








    FP=Face_Process() 

    firedb =FireDB()

    import FDetectionProcess 
    FD  = FDetectionProcess.FDetection()

    import HandProcess
    HP=HandProcess.Hand_Process()


    def runsystem():
        timer= -1
        ended = -1
        Flag = False
        last_action = -1 

        DBchecker= -1 

        db.child("system").remove()
        db.child("system").push({"state" : "open"})



        capture = cv2.VideoCapture(0)
        firedb.systemOnFlag = True
        while(True):

            list_threads = []
            LOG = pd.DataFrame({'person\s' : [],'Action':[],'time':[]})
            FD.outputs =[]
            FP.outputs =[]


            ret, img = capture.read()
            frame = img .copy()
            STime = time.time()  

        #----------------------- Multi-Threading part   


            t2= threading.Thread(target=FP.FaceReco, args = (img,HP,))
            t1 = threading.Thread(target= HP.Hand, args = (frame,))
            t3 = threading.Thread(target= FD.blazeface, args = (img,HP,))


            if( time.time() - DBchecker>=1):
                t5 = threading.Thread(target= firedb.checkdb, args = ())
                t5.start()
                DBchecker = time.time()



            if( (time.time() - HP.Startreco <2) and HP.Startreco !=-1 and t2.is_alive()==False ): 
                HP.makeFDsleep =True 
                FD.makeHPsleep =True 
                t2.start()
                list_threads.append(t2)



            elif((time.time() - HP.Startreco >2) and HP.Startreco !=-1 ):
                HP.Startreco=-1
                FP.StarAT = -1
                FP.Reco= False
                HP.makeFDsleep =False    
                FD.makeHPsleep =False 


            if(FD.Startreco != -1 and time.time() - FD.Startreco <=2 and t2.is_alive()==False ):
                FD.makeHPsleep =True 
                HP.makeFDsleep= True
                t2.start()
                list_threads.append(t2)

            elif (FD.Startreco != -1 and time.time() - FD.Startreco >= 2):
                FP.StarAT = -1
                FP.Reco= False
                FD.Startreco = -1
                FD.makeHPsleep =False
                HP.makeFDsleep= False


            if(timer != -1 and time.time() -timer<=1.5 and HP.makeFDsleep== False  ):
                t3.start()
                list_threads.append(t3)
            elif (time.time() -timer>1.5 and Flag ==False ):
                ended =time.time()
                Flag= True
            if(HP.makeFDsleep== False and time.time() -ended >=5 and Flag and time.time()-last_action >=15 ):
                timer = time.time()
                Flag= False




            if(FD.makeHPsleep== False ):
                t1.start()
                list_threads.append(t1)


            for thread in list_threads:   
                thread.join() 



        #------------------------------ Visualize the output

            ETime =time.time()  
            minus =ETime-STime
            Fps = 100
            if(minus != 0):
                Fps = math.floor(1/(ETime-STime))
            if(len(FD.outputs) !=0 ):
                for (x,y,w,h) in FD.outputs:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (67, 67, 67), 1)

            if(len(FP.outputs) !=0 ):
                for (x,y,w,h,label_name) in FP.outputs:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (67, 67, 67), 1)
                    cv2.rectangle(frame, (x,y+h+20), (x+w,y+h), (67, 67, 67), -1)
                    cv2.putText(frame, label_name, (x,y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)


        #------------------------ acessing and handling info------------------------------------




            today = date.today()
            d4 = today.strftime("%b-%d-%Y")
            directory= db_path+ "\LOGs" +"/"+d4

            if path.exists(directory) == False:
                os.mkdir(directory)



            if(FP.AAction): 
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                tmpName=directory+"/"+"guest"+str(firedb.counterguest)+".jpg"
                if(FP.FlagHomeOwner):
                    if(FP.FlagOpen):


                        print(FP.Who+" Opened the door")
                        open()
                        LOG =LOG.append({'person\s' :FP.Who ,'Action':" Opened the door",'time':dt_string } ,ignore_index=True)
                        t6 = threading.Thread(target= goUpdateDB , args = (FP.Who , " Opened the door",dt_string,))
                        t6.start()

                    elif(FP.FlagClose):


                        print(FP.Who+" Closed the door")
                        close()
                        LOG =LOG.append({'person\s' :FP.Who ,'Action':" Closed the door",'time':dt_string },ignore_index=True)
                        t6 = threading.Thread(target=goUpdateDB , args = (FP.Who , " Closed the door",dt_string,))
                        t6.start()




                    elif(FP.FlagNotPRed):


                        print(FP.Who+" Made Not A Predifined gesture ! ")
                        LOG =LOG.append({'person\s' :FP.Who ,'Action':" Made Not A Predifined gesture !",'time':dt_string },ignore_index=True)
                        t6 = threading.Thread(target= goUpdateDB , args = (FP.Who , " Made Not A Predifined gesture !",dt_string,))
                        t6.start()              


            #-------------------------------------------Mobile app  conditions ------------------------------------------------------------------               
                    else :     
                        print(FP.Who+" Waiting for a while and Made no gestures")  


                        t5 = threading.Thread(target= upload_To_Cloud_AND_PC , args = (tmpName , frame,firedb.counterguest,))
                        t5.start()


                       #--------------send notification to app 

                        msg=FP.Who +" Waiting for a while and Made no gestures"
                        t4 = threading.Thread(target= notify , args = (msg,firedb.counterguest , ))
                        t4.start()
                        firedb.counterguest =firedb.counterguest+1


                        #------------ updata log
                        LOG =LOG.append({'person\s' :FP.Who ,'Action':" Made no gestures",'time':dt_string },ignore_index=True)
                        t6 = threading.Thread(target=goUpdateDB , args = (FP.Who , " Made no gestures",dt_string,))
                        t6.start()   



                else :
                    if(FP.MakeAgesture):
                        print(FP.Who+" Waiting and Tried to Acess !! ")

                         #------------ save guests' faces


                        t5 = threading.Thread(target= upload_To_Cloud_AND_PC , args = (tmpName , frame,firedb.counterguest,))
                        t5.start()


                        #-------------- send notification to app 
                        msg=FP.Who +" Waiting and Tried to Acess !! "

                        t4 = threading.Thread(target= notify , args = (msg,firedb.counterguest,))
                        t4.start()


                        firedb.counterguest =firedb.counterguest+1


                        LOG =LOG.append({'person\s' :FP.Who ,'Action':" Waiting and Tried to Acess !!",'time':dt_string },ignore_index=True)

                        t6 = threading.Thread(target= goUpdateDB , args = (FP.Who , "  Waiting and Tried to Acess !!",dt_string,))
                        t6.start()   



                    else :
                        print(FP.Who+" Waiting Out Side")
                        #------------ save guests' faces



                        t5 = threading.Thread(target= upload_To_Cloud_AND_PC , args = (tmpName , frame,firedb.counterguest,))
                        t5.start()


                        #-------------- send notification to app 

                        msg=FP.Who +" Waiting"
                        t4 = threading.Thread(target= notify , args = (msg,firedb.counterguest,))
                        t4.start()

                        firedb.counterguest =firedb.counterguest+1

                        #------------ updata log


                        LOG =LOG.append({'person\s' :FP.Who ,'Action':" Waiting",'time':dt_string },ignore_index=True)
                        db.child("log").push({"person" :FP.Who, "action" : " Waiting " , "time": dt_string})
                        t6 = threading.Thread(target= goUpdateDB , args = (FP.Who , " Waiting ",dt_string,))
                        t6.start()   








                def resetVar():
                    FP.FlagHomeOwner =False
                    FP.FlagOpen = False
                    FP.FlagClose = False
                    FP.FlagNotPRed= False 
                    FP.MakeAgesture=False
                    FP.faces=[]

                resetVar()



        #----------------------------------- write on csv file
                FP.AAction= False  
                last_action = time.time() # <==
                #today = date.today()
                #d4 = today.strftime("%b-%d-%Y")
                #tmp = db_path+"/"+ "LOGs" +"\LOG--"+d4+".csv"

                #directory= db_path+ "\LOGs" +"/"+d4
                tmpcsv = directory +"/"+"log.csv"
                if path.exists(tmpcsv):
                    a = pd.read_csv(tmpcsv)
                    LOG = a.append(LOG ,ignore_index=True)
                LOG.to_csv(tmpcsv, index = False)



        #--------------------------------------


            cv2.putText(frame, "FPS: "+str(Fps), (0,25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (67, 67, 67), 2)
            cv2.putText(frame, "Previous Gesture: " +HP.prev_Gesture, (0,47), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (67, 67, 67), 2)
            cv2.imshow('Computer Vision System', frame)   

            if (cv2.waitKey(1) & 0xFF == ord('q')) or firedb.systemOnFlag == False :
                db.child("system").remove()
                db.child("system").push({"state" : "close"})
                break

        cv2.destroyAllWindows()
        capture.release()

    DBCHECKER=-1
    
    runsystem()

