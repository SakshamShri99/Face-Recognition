import cv2
import pymongo
import gridfs

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def face_extracter(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if faces is ():
        return None

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cropped_face = img[y:y + h, x:x + w]

    return cropped_face


def face_capture(roll_no=0, person="", cap=None):  # Function for image capture of new student
    FNF, count = 150, 0

    while count < 100:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if face_extracter(frame) is not None:
            FNF = 150
            count += 1
            try:
                face = cv2.resize(face_extracter(frame), (200, 200), interpolation=cv2.INTER_AREA)
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                file_name_path = 'Database/' + person + '/Faces/' + str(roll_no) + '/' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)  # function to save images. we have to save it in mongoDB
            except:
                count -= 1

            cv2.putText(frame, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Face Cropper', frame)
            cv2.waitKey(1)
        else:
            FNF -= 1
            if FNF == 0:
                break
            cv2.putText(frame, "Please Look into the camera", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, "Exiting in " + str(FNF / 10), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow('Face Cropper', frame)
            cv2.waitKey(1)
            print("Face not Found")
    print("Face Captured!!")
