import numpy as np
import mediapipe as mp
import cv2
import time
import os
from os import listdir, path
import math
from PIL import Image,ImageEnhance
from tensorflow.keras.preprocessing.image import load_img, save_img, img_to_array
import pandas as pd
import pickle





def load_image(img):  # To Load an image whatever its type 

    exact_image = False
    if type(img).__module__ == np.__name__:
        exact_image = True

    base64_img = False
    if len(img) > 11 and img[0:11] == "data:image/":
        base64_img = True

    #---------------------------

    if base64_img == True:
        img = loadBase64Img(img)

    elif exact_image != True: #image path passed as input
        if os.path.isfile(img) != True:
            raise ValueError("make sure that ",img," exists")

        img = cv2.imread(img)

    return img


def preprocess_image_with_mediaPipe(faceDetection,image_path):  # Face Detection and alignment for DB Creation
    img = load_image(image_path)
    ih, iw, _ = img.shape
    results = faceDetection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.detections: 
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box

            right_eye_center=(int (detection.location_data.relative_keypoints[1].x * iw) , int(detection.location_data.relative_keypoints[1].y * ih))
            left_eye_center=(int(detection.location_data.relative_keypoints[0].x * iw) , int(detection.location_data.relative_keypoints[0].y * ih))



            x=int(bboxC.xmin * iw)
            y=int(bboxC.ymin * ih)
            w =int(bboxC.width * iw)
            h =int(bboxC.height * ih)
            detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face 

        img = detected_face


        left_eye_x = left_eye_center[0]; left_eye_y = left_eye_center[1]
        right_eye_x = right_eye_center[0]; right_eye_y = right_eye_center[1]


        if left_eye_y > right_eye_y:

            point_3rd = (right_eye_x, left_eye_y)
            direction = -1 #rotate same direction to clock
            #print("rotate to clock direction")
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

        cos_a = (b*b + c*c - a*a)/(2*b*c)
        #print("cos(a) = ", cos_a)

        angle = np.arccos(cos_a)
        #print("angle: ", angle," in radian")

        angle = (angle * 180) / math.pi
       # print("angle: ", angle," in degree")
        if direction == -1:
            angle = 90 - angle


        new_img = Image.fromarray(img)
        new_img = np.array(new_img.rotate(direction * angle))
        #cv2.imshow("Face After enhancement and rotating",new_img)
        #cv2.waitKey(1)
        img = img_to_array(new_img)
        img = cv2.resize(img, (160, 160))
        img = np.expand_dims(img, axis=0)  

        mean, std = img.mean(), img.std()
        img = (img-mean)/std
        return img
    else : 
        raise Exception("Make sure that face in image with path ",image_path, " has a face ! ")


def findEuclideanDistance(source_representation, test_representation):  
    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance





def Create_DB(employees,db_path,interpreter, input_details, output_details):  #Create representation for face in DB
    file_name = "representations.pkl"
    St =time.time()
    HomeownerPath=db_path+"/"+"HomeOwners"
    if path.exists(HomeownerPath+"/"+file_name):

        print("WARNING: Representations for images in ",HomeownerPath," folder were previously stored in ", file_name, )
        print( "Thus, if you added new instances after this file creation, then please delete this file and call find function again. It will create it again.")
        print(HomeownerPath+"/"+file_name, 'rb')
        f = open(HomeownerPath+"/"+file_name, 'rb')
        representations = pickle.load(f)

        print("There are ", len(representations)," representations found in ",file_name)
        #print(representations)
        return representations
    
    elif(len(listdir(HomeownerPath))):
        faceDetection = mp.solutions.face_detection.FaceDetection(0.8)

        for employee in listdir(HomeownerPath):
            if(employee != file_name):
                for img in listdir(HomeownerPath +"/"+employee):
                    #employee, extension = file.split(".")
                    #TmpPath= HomeownerPath + "\%s.jpg"
                    img = preprocess_image_with_mediaPipe(faceDetection, HomeownerPath +"/"+employee+"/"+img )
                    img_pixels= np.array(img, dtype=np.float32)
                    interpreter.set_tensor(input_details[0]['index'],img_pixels )
                    interpreter.invoke()
                    representation = interpreter.get_tensor(output_details[0]['index'])
                    employees.append((employee,representation))

                #-------------------------------

                

        print("Faces In DB representations retrieved successfully")
        file_name = "representations.pkl"
        f = open(HomeownerPath+"/"+file_name, "wb")
        pickle.dump(employees, f)
        f.close()
        #print (employees)
        print("it takes " , round(time.time() -St , 2)," seconds To Create DB From Scratch")
        print("Representations stored in ",HomeownerPath+"/"+file_name," file. Please delete this file when you add new identities in your database.")
        return employees
    else:
        raise ValueError("There is no images in ", db_path," folder! Validate .jpg or .png files exist in this path.")