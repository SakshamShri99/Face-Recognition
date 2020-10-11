import cv2
import yaml
import numpy as np
from os import listdir, mkdir
from os.path import isfile, join, isdir


def model_trainer(data_path, model_id):  # function for training the face recognition model

    face_list = [face for face in listdir(data_path) if isfile(join(data_path, face))]

    Training_Data, Labels = [], []

    for i, files in enumerate(face_list):
        image_path = data_path + face_list[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)

    model = cv2.face.LBPHFaceRecognizer_create()

    model.train(np.asarray(Training_Data), np.asarray(Labels))
    #mkdir("Database/Admin/Faces/" + str(model_id))
    model.write(data_path+'model/'+str(model_id))

    return model


def model_list_gen(person=""):
    dir_path = "Database/" + person + "/Faces/"
    dir_list = [(dir_path + dir + '/', int(dir)) for dir in listdir(dir_path) if isdir(join(dir_path, dir))]
    if not dir_list:
        if person == "Admin":
            raise FileNotFoundError("No Admin Found")
        else:
            raise FileNotFoundError("No Student Registered")
    model_list = []
    for dir in dir_list:
        model_list = model_list + [(model_trainer(dir[0], dir[1]), dir[1])]
    return model_list
