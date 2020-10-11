import Face_Detector
import Face_Capture
import Model_Generate
import os
import cv2
import pymongo

cap = cv2.VideoCapture(0)

dbConn = pymongo.MongoClient("mongodb+srv://sakshamshri:mongodb@facedetect.sh3oa.gcp.mongodb.net/Face_ID"
                                 "?retryWrites=true&w=majority")
db = dbConn['Face_Id']

def AddStudent():
    cap = cv2.VideoCapture(0)
    roll_no = int(input("Enter Roll No.\n"))
    student_name = input("Enter Student Name\n")
    branch = input("Enter Branch.\n")
    year = int(input("Enter Year.\n"))
    os.mkdir("Database/Student/Faces/" + str(roll_no))
    Face_Capture.face_capture(roll_no, "Student", cap)
    Model_Generate.model_trainer("Database/Student/Faces/",roll_no, 'Student')
    for x in range(100):
        pass
    collection = db['Student']
    row = {
        "Roll No": roll_no,
        "Student Name": student_name,
        "Branch": branch,
        "Year": year
    }
    collection.insert_one(row)
    print("Thank You")


def DeleteStudent():
    roll_no = int(input("Enter Roll No.\n"))
    collection = db['Student']
    my_db_query = {'Roll No': roll_no}
    x = collection.delete_one(my_db_query)
    if x.deleted_count == 1:
        print("Deleted !!")
    else:
        print("Roll no. does not exist !!")


def StudentDetail():
    roll_no = int(input("Enter Roll No.\n"))
    try:
        collection = db['Student']
        my_db_query = {'Roll No': roll_no}
        result_st = collection.find_one(my_db_query)
        print(result_st)
    except IndexError:
        print("Roll no. does not exist !!!")


def CheckAdmin(Id):
    collection = db['Admin']
    my_db_query = {'Admin ID': Id}
    result_st = collection.find_one(my_db_query)
    #print('Welcome ' + result_st['Admin Name'])

def AddAdmin():
    cap = cv2.VideoCapture(0)
    adminId = int(input("Admin ID\n"))
    collection = db["Admin"]
    admin_name = input("Enter Admin Name\n")
    post = input("Enter Post.\n")
    dep = input("Enter Department.\n")
    os.mkdir("Database/Admin/Faces/" + str(adminId))
    Face_Capture.face_capture(adminId, "Admin", cap)
    Model_Generate.model_trainer("Database/Admin/Faces/", adminId, 'Admin')
    row = {
        "Admin ID": adminId,
        "Admin Name": admin_name,
        "Post": post,
        "Department": dep
    }
    collection.insert_one(row)
    cap.release()
    cv2.destroyAllWindows()


def GetAdmin():
    adminId = int(input("Enter admin ID\n"))
    try:
        collection = db['Admin']
        my_db_query = {'Admin ID': adminId}
        result_st = collection.find_one(my_db_query)
        print(result_st)
    except IndexError:
        print("Admin ID does not exist !!!")


def admin():

    try:
        while True:
            present, adminId = Face_Detector.face_detect("Admin", cap)
            if present:  # code to display Admin details.
                CheckAdmin(adminId)
                break
            else:
                print('Admin Not Recognised')

            while True:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                image, face = Face_Detector.face_detector(frame)
                cv2.putText(image, "Please Look Into The Camera", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv2.imshow('Face Cropper', image)
                cv2.waitKey(1)
                if not face:
                    break
        cap.release()
        cv2.destroyAllWindows()

    except FileNotFoundError:
        if int(input("No Admin was found\nPress 1 to add Admin\n")) == 1:  # Adding Admin if not present.
            AddAdmin()
            exit()

    # choice = int(input("1.Add Student\n2.Delete Student\n3.See Student Details\n4.Add Admin\n5.See Admin Details\n"))
    #
    # if choice == 1:  # code to add details of new student in mongodb.
    #     AddStudent()
    #
    # if choice == 2:  # code to delete the student details from database.
    #     DeleteStudent()
    #
    # if choice == 3:  # code to show students details from mongoDb.
    #     StudentDetail()
    #
    # if choice == 4:  # code to add admin details in mongodb.
    #     AddAdmin()
    #
    # if choice == 5:  # code for data fetching and display from mongoDB
    #     GetAdmin()

