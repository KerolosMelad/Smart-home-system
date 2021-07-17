
import tensorflow as tf
import time
from os import listdir,path


def GetTheModel(db_path):
    ST = time.time()
    interpreter = tf.lite.Interpreter(model_path=db_path+"/"+"Model/model.tflite") # CONVERT tf Facenet MODEL TO tfLIte
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("FaceNet builded successfully in TFlite in" , round(time.time() -ST , 2),"seconds")
    return interpreter , input_details ,output_details
