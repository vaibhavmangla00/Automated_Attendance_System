'''
THIRD PART OF THE PROJECT
'''


import xlsxwriter
import cv2
import numpy as np
from os import listdir
import face_recognition
from datetime import datetime
import pickle

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

attendance_array = []


def make_attendance_list(name):
    now = datetime.now()
    timeString = now.strftime('%H:%M:%S')
    dateString = now.strftime("%d/%m/%Y")
    attendance_array.append([name, timeString, dateString])

    with open('Attendance of Students', 'a') as individual:
        individual.write(f'{name},{timeString},{dateString}\n')


with open("face_encodings", "rb") as fp:   # Unpickling
    encodeListKnown = pickle.load(fp)
print('Encodings imported Successfully!!!')

cap = cv2.VideoCapture("./exitshort.mp4")

pTime = 0
while True:
    success, img = cap.read()
    try:
        # we are reduceing the size of image to speed up the process as its real time
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    except:
        break

    # realtime image size has been divided by 4 using 0.25
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS,)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # finding matches
    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(
            encodeListKnown, encodeFace, tolerance=0.6)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        # print(faceDis)

        with open("list_ids", "rb") as idlist_var:   # Unpickling
            idlist = pickle.load(idlist_var)
        matchIndex = np.argmin(faceDis)

        # print('matchIndex', matchIndex)

        if matches[matchIndex]:
            name = personNames[idlist[matchIndex]].upper()
            # print(name)
            make_attendance_list(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.rectangle(img, (x1, y2 + 35), (x2, y2), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 + 24),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Recognize", cv2.resize(img, (480, 720)))

    # press'esc' to close program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# release camera
cap.release()
cv2.destroyAllWindows()

print("Id, Time & Date for Detected Faces exported Successfully ")


'''
FOURT PART OF THE PROJECT
'''

namelist = {}

with open("Attendance of Students", "r") as ar:
    lines = ar.readlines()
    workbook = xlsxwriter.Workbook('Attendance_of_Students.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Name')
    worksheet.write(0, 1, 'Time')
    worksheet.write(0, 2, 'Date')
    i = 1
    for line in lines[10:]:
        name = line.split(',')[0]
        time = line.split(',')[1]
        date = line.split(',')[2]
        if name in lines[lines.index(line)-7] and name in lines[lines.index(line)-6] and name in lines[lines.index(line)-5] and name in lines[lines.index(line)-4] and name in lines[lines.index(line)-3] and name in lines[lines.index(line)-2] and name in lines[lines.index(line)-1]:
            if name not in namelist.keys():
                namelist[name] = time
                # Attendance_of_Students.csv must already exist with Name and Time as columns
                worksheet.write(i, 0, name)
                worksheet.write(i, 1, time)
                worksheet.write(i, 2, date)
                i += 1
    workbook.close()
