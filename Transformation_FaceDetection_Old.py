###IMPORTS
import os
import numpy as np
import time
import mediapipe as mp
import cv2 as cv
import random
###IMPORTS


###VARIABLES
images_path = ""
images_list = []
translated_list = []
width, height = 640,360
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
###VARIABLES
left_eye_xy = ""
initialx = .495247483253479
initialy = .5778067111968994


x_ylist = []


def find_left_eye(img):

    Left_eye_mediapipe_file = open(_file.txt","w")
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7) as face_detection:
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        if not results.detections:
            pass
        annotated_image = img.copy()
        for detection in results.detections:
            # draws face/eye box/dots on image
            image = mp_drawing.draw_detection(annotated_image, detection)
            # shows images on screen.
            cv.imshow("sdf",annotated_image)
            cv.waitKey(1)
            # stores new annotated image in file path
            #cv2.imwrite(store_image_path + str(idx) + '.png', annotated_image)
            left_eye = mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP)
            Left_eye_mediapipe_file.write(str(left_eye))
            Left_eye_mediapipe_file.close()
            return left_eye




def find_eye(image):
    find_eye = eye_cascade.detectMultiScale(image, 1.3, minNeighbors=5)
    global left_pupil
    global right_pupi
    for (x, y, w, h) in find_eye:
        left_pupil = int(x + (h / 2))
        right_pupil = int(y + (w / 2))
        image = cv.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 1)
        image = cv.circle(image,(int(left_pupil),int(right_pupil)),3,(255,255,255),thickness=3)


def move_image(img, x, y):
    transMat = np.float32([[1,0,x],[1,0,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

def translate(img, x, y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)


#specifically this for loop gets all files and only keeps the ones that are jpg files and aren't curropted or 0 in size.
for file in os.listdir(images_path):
    #endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each file name size is different and the initial start is different. anyways this works currently
    if file.endswith("g") and os.path.getsize(images_path + file) > 0:
        images_list.append(images_path + file)
    else:
        pass


def List_formatting(file):
    global xlist
    global ylist
    xlist = []
    ylist = []
    left_eye_xy = file.read()
    # stripping the list of all extra values (x,y,whitespaaces, colons)    print(left_eye_xy)
    left_eye_xy = left_eye_xy.split("\n")
    if len(left_eye_xy) > 2:
        left_eye_xy.pop(2)
    else:
        pass
    for index, value in enumerate(left_eye_xy):

        if index == 0:
            for idx, char in enumerate(value):
                if idx == 1 or idx == 2 or idx == 0:
                    pass
                else:
                    xlist.append(char)
        elif index == 1:
            for idx, char in enumerate(value):
                if idx == 1 or idx == 2 or idx == 0:
                    pass
                else:
                    ylist.append(char)
            ylist.insert(0, ",")
    x_ylist = xlist + ylist
    ylist = []
    xlist = []
    list_split_index = 0
    # this loop will seperate x_ylist into just the 2 x/y lists we need.
    for inx, char in enumerate(x_ylist):
        if char == ",":
            # a variable that is later used to split the lists, we then append each character depending if it falls
            # bfore or after this variable.
            # if it falls after, its part of the y varible, if before, it is part of the x
            list_split_index = inx
            for indx, char in enumerate(x_ylist):
                if indx > list_split_index:
                    ylist.append(char)
                elif indx < list_split_index:
                    xlist.append(char)
    return xlist, ylist

def Find_Difference(ixlist,iylist,xlist,ylist):
    float(ixlist)
    float(iylist)
    float(xlist)
    float(ylist)

    difference_x = (float(ixlist) - float(xlist))
    difference_y = (float(iylist) - float(ylist))
    if difference_x < 0:
        difference_x = abs(difference_x)
    elif difference_x > 0:
        difference_x = difference_x * -1
    if difference_y < 0:
        difference_y = abs(difference_y)
    elif difference_y > 0:
        difference_y = difference_y * -1
    return difference_x, difference_y

for image in images_list:
    Left_eye_mediapipe_file = open("t","r")
    xlist = []
    ylist = []
    cv2image = cv.imread(image)
    cv2image = cv.resize(cv2image, (width,height))
    find_left_eye(cv2image)
    currnentlist = List_formatting(Left_eye_mediapipe_file)
    currentxlist = "".join(currnentlist[0])
    currentylist = "".join(currnentlist[1])
    translated = translate(cv2image, ((Find_Difference(initialx,initialy,currentxlist,currentylist))[0] *100 ),((Find_Difference(initialx,initialy,currentxlist,currentylist))[1] * 100))

    #translated_list.append(translated)
    cv.imshow("translated",translated)
    cv.waitKey(1)


#write the x,y coords to file
#close file
#open file again in read mode and read its contents to a list/str
#delete the "x:" and "y:" and any whitespaces: " "
#split the 2 numbers into a list with different indexes
