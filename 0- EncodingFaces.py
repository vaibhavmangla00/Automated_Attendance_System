''''
SECOND PART OF THE PROJECT
'''


import face_recognition
import numpy as np
import cv2
from os import listdir
import pickle

id_list = []


def faceEncodings(images):
    encodeList = []
    i = 0
    for img in images:
        i += 1
        encode = face_recognition.face_encodings(img)
        print("shape of encode is: ", np.shape(encode))
        if np.shape(encode) == (1, 128):
            id_list.append(i // 50)
            encodeList.append(encode[0])
        print("value of i is: ", i)
    return encodeList


def writeinword(encodelist):
    with open("face_encodings", "wb") as fp:  # Pickling
        pickle.dump(encodelist, fp)


if __name__ == '__main__':

    data_path = 'Database/'
    personNames = []
    images = []
    paths = []

    for name in listdir("Database"):
        for a_image in listdir(f"Database/{name}"):
            a_img = cv2.imread(f"Database/{name}/{a_image}")
            images.append(a_img)
        personNames.append(name)
        paths.append(f'Database/{name}')

    encoded_faces = faceEncodings(images)
    print(len(encoded_faces))
    with open("list_ids", "wb") as idlist_var:  # Pickling
        pickle.dump(id_list, idlist_var)
    writeinword(encoded_faces)
