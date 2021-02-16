import Face_Detector
import Face_Capture
import Model_Generate
import os
import shutil
import cv2
import pymongo

cap = cv2.VideoCapture(0)

dbConn = pymongo.MongoClient("mongodb+srv://sakshamshri:sT4fxGTkGQWtJinU@facedetect.sh3oa.gcp.mongodb.net/Face-Id"
                             "?retryWrites=true&w=majority")

db = dbConn['Face_Id']


def AddStudent(details):
    cap = cv2.VideoCapture(0)
    os.mkdir("Database/Student/Faces/" + details[0])
    Face_Capture.face_capture(details[0], "Student", cap)
    Model_Generate.model_trainer("Database/Student/Faces/", details[0], 'Student')
    for x in range(100):
        pass

    collection = db['Student']
    row = {
        "Roll No": details[0],
        "Student Name": details[1],
        "Branch": details[2],
        "Year": details[3]
    }
    collection.insert_one(row)
    cap.release()
    cv2.destroyAllWindows()


def DeleteStudent(details):
    collection = db['Student']
    my_db_query = {"Roll No": details[0]}
    x = collection.delete_one(my_db_query)
    if x.deleted_count == 1:
        shutil.rmtree("Database/Student/Faces/" + details[0])
        mpath = []
        with open('Student_model_list.txt', 'r+') as file:
            for line, model_path_list in enumerate(file.read().splitlines()):
                model_id, model_path = model_path_list.split(',')
                mpath += [[model_id, model_path]]
                file.seek(0)
        with open('Student_model_list.txt', 'w') as file:
            for model in mpath:
                if model[0] != details[0]:
                    file.write(model[0] + ',' + model[1] + '\n')
        return True
    else:
        return False


def StudentDetail(details):
    collection = db['Student']
    my_db_query = {'Roll No': details[0]}
    return collection.find_one(my_db_query)


def CheckAdmin(details):
    collection = db['Admin']
    my_db_query = {'Admin ID': details[0]}
    return collection.find_one(my_db_query)


def AddAdmin(details):
    cap = cv2.VideoCapture(0)
    collection = db["Admin"]
    os.mkdir("Database/Admin/Faces/" + details[0])
    Face_Capture.face_capture(details[0], "Admin", cap)
    Model_Generate.model_trainer("Database/Admin/Faces/", details[0], 'Admin')
    row = {
        "Admin ID": details[0],
        "Admin Name": details[1],
        "Post": details[2],
        "Department": details[3]
    }
    collection.insert_one(row)
    cap.release()
    cv2.destroyAllWindows()


def DelAdmin(details):
    collection = db['Admin']
    my_db_query = {"Admin ID": details[0]}
    x = collection.delete_one(my_db_query)
    if x.deleted_count == 1:
        shutil.rmtree("Database/Admin/Faces/" + details[0])
        mpath = []
        with open('Admin_model_list.txt', 'r+') as file:
            for line, model_path_list in enumerate(file.read().splitlines()):
                model_id, model_path = model_path_list.split(',')
                mpath += [[model_id, model_path]]
        with open('Admin_model_list.txt', 'w') as file:
            for model in mpath:
                if model[0] != details[0]:
                    file.write(model[0] + ',' + model[1] + '\n')
        return True
    else:
        return False


def GetAdmin(details):
    try:
        collection = db['Admin']
        my_db_query = {'Admin ID': details[0]}
        return collection.find_one(my_db_query)
    except IndexError:
        print("Admin ID does not exist !!!")


def admin():
    try:
        while True:
            present, adminId = Face_Detector.face_detect("Admin", cap)
            if present:  # code to display Admin details.
                CheckAdmin(adminId)
                cap.release()
                cv2.destroyAllWindows()
                return True

            while True:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                image, face = Face_Detector.face_detector(frame)
                cv2.putText(image, "Please Look Into The Camera", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv2.imshow('Face Cropper', image)
                cv2.waitKey(1)
                if not face:
                    break

    except TypeError:
        cap.release()
        cv2.destroyAllWindows()
        return False
