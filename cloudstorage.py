def start():
    import pyrebase
    firebaseConfig = {
            "apiKey": "AIzaSyBh1ZAR2QUYnTJ1bUPbhINAMAkKfpny0CA",
            "authDomain": "computer-vision-a47ad.firebaseapp.com",
            "databaseURL": "https://computer-vision-a47ad-default-rtdb.firebaseio.com",
            "projectId": "computer-vision-a47ad",
            "storageBucket": "computer-vision-a47ad.appspot.com",
            "messagingSenderId": "146136556212",
            "appId": "1:146136556212:web:6a593c4930be9cde7cade1",
            "measurementId": "G-KCQ0KTWT43"

    }


    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    db = firebase.database()
    return storage ,db