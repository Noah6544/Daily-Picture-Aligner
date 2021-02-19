import numpy as np
import cv2 as cv2
from PIL import Image
import PIL

face_cascade = cv2.CascadeClassifier("C:\\Users\\Noah\'s Marc P. 4648\\Desktop\ARBOK\\2021\\camera roll picture aligning automation (2021)\\github\\data\\haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("C:\\Users\\Noah\'s Marc P. 4648\\Desktop\\ARBOK\\2021\\camera roll picture aligning automation (2021)\\github\\data\\haarcascade_eye.xml")
img = cv2.imread("C:\\Users\\Noah\'s Marc P. 4648\\Desktop\\ARBOK\\2021\\camera roll picture aligning automation (2021)\\pictures\\obama.jpg")
face = face_cascade.detectMultiScale(img, 1.3, minNeighbors=5)
eye = eye_cascade.detectMultiScale(img, 1.3, minNeighbors=5)

print("Faces found: ", len(face))
print("the image height, width, and channel: ", img.shape)
print("the coordinates of each eye: ", eye)

#for loops which are looping through each iteration and adding rectangles to each eye and face
for (x,y,w,h) in eye:
    cv2.rectangle(img,(x,y), (x+w,y+h), (255, 255, 255),2)
for (x,y,w,h) in face:
    cv2.rectangle(img,(x,y), (x+w,y+h), (0, 0, 0),2)

#displays picture
cv2.imshow("file", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

