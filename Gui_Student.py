import Face_Detector
import cv2
from datetime import date
import pymongo

def student():
    cap = cv2.VideoCapture(0)

    dbConn = pymongo.MongoClient("mongodb+srv://sakshamshri:mongodb@facedetect.sh3oa.gcp.mongodb.net/Face_ID?retryWrites"
                                 "=true&w=majority")
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
                print(str(roll_no) + " Present")
                print("Attendance taken!!!")

            else:
                print("Not Present\nPLease contact admin in case of any problem")

            while True:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                image, face = Face_Detector.face_detector(frame)
                cv2.putText(image, "Please Look Into The Camera", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv2.imshow('Face Cropper', image)
                cv2.waitKey(1)
                if face != []:
                    break

    except FileNotFoundError:
        return "No Student Registered\nPlease Contact Admin"

    cap.release()
    cv2.destroyAllWindows()
