from base64 import b64decode
import face_recognition as fr
import time
import os
import pickle

def login_check(email, image):
    face_match = 0
    header, encoded = image.split(",", 1)
    file_new = "updated"

    with open(file_new + ".png", "wb") as f:
        f.write(b64decode(encoded))
    
    try:
        try:
            got_image = fr.load_image_file("updated.png")
            existing_image = fr.load_image_file("old.png")
        except Exception as e:
            print(e.__cause__)
            return "Data does not exist!"
        got_image_facialfeatures = fr.face_encodings(got_image)[0]
        existing_image_facialfeatures = fr.face_encodings(existing_image)[0]
        results = fr.compare_faces([existing_image_facialfeatures], got_image_facialfeatures)
        if(results[0]):
            return "Successfully Logged in!"
        else:
            return "Failed to Log in!"
    except Exception as e:
        print(e.__cause__)
        return "Image not clear! Please try again!"