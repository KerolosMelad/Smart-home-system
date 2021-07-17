import firebase_admin
from firebase_admin import credentials, messaging
import os

cred = credentials.Certificate((os.getcwd()+"/"+"computer-vision-a47ad-firebase-adminsdk-4z4s5-d4ac5fcf52.json"))
firebase=firebase_admin.initialize_app(cred)




def sendPush(title, msg, registration_token, dataObject):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        #notification=messaging.Notification(
          #  title=title,
           # body=msg
        #)
    #,
        data={'imgnamex':dataObject},
        tokens=registration_token,
    )
    
    message2 = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        )
    ,
        data={'imgname':dataObject},
        tokens=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    response2 = messaging.send_multicast(message2)
    # Response is a message ID string.
    print('Successfully sent 2  messages:', response ,response2)
