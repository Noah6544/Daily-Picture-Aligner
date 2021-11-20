###IMPORTS
import os
import cv2 as cv
import numpy as np
import time
import mediapipe as mp
import random
###IMPORTS

###VARIABLES
images_path = "C:\\path to images\Images\\"
images_list = []


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
    transMat = np.float32([[1,0,x], [1,0,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)


for image in os.listdir(images_path):
    tenkfaces_list.append(images_path + image)

randomx = random.randint(-2,5)
randomy = random.randint(-2,5)
translated = move_image(image,100, 600)
cv.imshow("translated",translated)
cv.waitKey(0)
