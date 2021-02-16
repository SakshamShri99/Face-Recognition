import Face_Detector
import cv2
from datetime import date
import pymongo
import PySimpleGUI as sg

def student():
    cap = cv2.VideoCapture(0)

    dbConn = pymongo.MongoClient("mongodb+srv://sakshamshri:sT4fxGTkGQWtJinU@FaceDetect.sh3oa.gcp.mongodb.net/FaceDetect"
                                 "?retryWrites=true&w=majority")
    db = dbConn['Attendance']
    try:
        while True:
            present, roll_no = Face_Detector.face_detect("Student", cap)
            if present:

                # code to increase the attendance by 1 and display student Name and Roll NO. #

                d = date.today()
                collection = db[str(roll_no)]
                row = {
                    d.isoformat(): "P"
                }

                collection.insert_one(row)
            else:
                sg.PopupTimed("Not recognized please contact administrator!!!", auto_close_duration=2)
            while True:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                image, face = Face_Detector.face_detector(frame)
                cv2.putText(image, "Please Look Into The Camera", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv2.imshow('Face Cropper', image)
                cv2.waitKey(1)
                if face != []:
                    break

    except TypeError:
        sg.Popup(("No student registered please contact administrator!!"))

    cv2.destroyAllWindows()

student()