'''
FIRST PART OF THE PROJECT
'''


import cv2
import numpy as np
import os

face_classifier = cv2.CascadeClassifier(
    "C:/Python310/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")


def face_extractor(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if faces == ():
        return None

    for(x, y, w, h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
count = 0

dir_num = 1
make_dir = True
while make_dir:
    if os.path.isdir(f'./Dataset{dir_num}/'):
        dir_num += 1
    else:
        os.mkdir(f'./Dataset{dir_num}')
        path = f'./Dataset{dir_num}/'
        make_dir = False


while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count += 1
        face = cv2.resize(face_extractor(frame), (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        file_name_path = f'{path}' + \
            str(count)+'.jpg'

        cv2.imwrite(file_name_path, face)

        cv2.putText(face, str(count), (50, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Face Cropper', face)
    else:
        print("Face not found")
        pass

    if cv2.waitKey(1) == 13 or count == 100:
        break

cv2.destroyAllWindows()
print('Samples Colletion Completed ')
