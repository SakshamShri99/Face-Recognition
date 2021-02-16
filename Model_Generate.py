import cv2
import numpy as np
from os import listdir, mkdir
from os.path import isfile, join


def model_load(person=''):
    model = cv2.face.LBPHFaceRecognizer_create()
    model_list = []
    with open(person+'_model_list.txt', 'r') as file:
        for line, model_path_list in enumerate(file.read().splitlines()):
            model_id, model_path = model_path_list.split(',')
            print(model_path)
            model.read(model_path)
            model_list += [[model, model_id]]
    return model_list


def model_trainer(data_path, model_id, person=''):  # function for training the face recognition model

    model_path = data_path + str(model_id) + '/'

    face_list = [face for face in listdir(model_path) if isfile(join(model_path, face))]

    Training_Data, Labels = [], []

    for i, files in enumerate(face_list):
        image_path = model_path + face_list[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)

    model = cv2.face.LBPHFaceRecognizer_create()

    model.train(np.asarray(Training_Data), np.asarray(Labels))

    with open(person+'_model_list.txt', 'a') as file:
        mkdir(model_path+'model/')
        model.write(model_path+'model/'+str(model_id))
        file.write(model_id+','+model_path+'model/'+model_id+'\n')