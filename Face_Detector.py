import Model_Generate
import cv2
import time

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if faces is ():
        return img, []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = img[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))

    return img, roi


def face_detect(person, cap):  # Function to detect if current faces matches the record
    FNF, MNF, PR = 0, 0, 0
    model_list = Model_Generate.model_load(person)

    for model in model_list:
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            image, face = face_detector(frame)

            if face is not []:
                try:
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    result = model[0].predict(face)
                    cv2.imshow('Face Cropper', image)
                    cv2.waitKey(1)

                    if result[1] < 500:
                        confidence = ((1 - (result[1]) / 300) * 100)
                        display_string = str(int(confidence)) + '% Match'
                        cv2.putText(image, display_string, (250, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))

                        if confidence > 70:
                            PR += 1
                            cv2.imshow('Face Cropper', image)
                            cv2.waitKey(1)
                            if PR == 100:
                                cv2.putText(image, "Presence Registered", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1,
                                            (0, 255, 0))
                                cv2.imshow('Face Cropper', image)
                                cv2.waitKey(1)
                                time.sleep(2)
                                return True, model[1]

                        else:
                            MNF += 1
                            if MNF % 10 == 0 and len(model_list) * 10 > 50:
                                break
                            cv2.imshow('Face Cropper', image)
                            cv2.waitKey(1)
                            if MNF > len(model_list) * 10 and MNF > 50:
                                cv2.putText(image, "Match not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1,
                                            (0, 0, 255))
                                cv2.imshow('Face Cropper', image)
                                cv2.waitKey(1)
                                time.sleep(2)
                                return False, 0

                    else:
                        break

                except TypeError:
                    pass
            else:
                return False, 0
